"""Download manager for orchestrating chapter downloads."""

import logging
import re
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from api.client import AtsuClient
from config import get_config
from converters import convert_to_pdf, convert_to_cbz
from models import Chapter, DownloadResult, MangaInfo

from .images import ImageDownloader

logger = logging.getLogger(__name__)


def parse_chapter_selection(selection: str, total_chapters: int) -> List[int]:
    """Parse chapter selection string into list of indices.
    
    Supports:
    - "all" or "a": All chapters
    - "5": Single chapter (by number)
    - "1-10": Range of chapters
    - "1,3,5-7": Mixed selection
    
    Returns:
        List of 0-based chapter indices
    """
    selection = selection.strip().lower()
    
    if selection in ("all", "a"):
        return list(range(total_chapters))
    
    indices = set()
    parts = selection.replace(" ", "").split(",")
    
    for part in parts:
        if "-" in part:
            # Range: "1-10"
            match = re.match(r"(\d+)-(\d+)", part)
            if match:
                start, end = int(match.group(1)), int(match.group(2))
                # Convert to 0-based indices
                for i in range(start - 1, min(end, total_chapters)):
                    if 0 <= i < total_chapters:
                        indices.add(i)
        else:
            # Single: "5"
            try:
                num = int(part)
                idx = num - 1  # Convert to 0-based
                if 0 <= idx < total_chapters:
                    indices.add(idx)
            except ValueError:
                continue
    
    return sorted(indices)


def sanitize_filename(name: str) -> str:
    """Sanitize string for use as filename."""
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Replace multiple spaces with single space
    name = re.sub(r'\s+', ' ', name)
    return name.strip()[:200]  # Limit length


class DownloadManager:
    """Orchestrates downloading of manga chapters."""

    def __init__(self, client: Optional[AtsuClient] = None):
        self.client = client or AtsuClient()
        self._owns_client = client is None
        self.image_downloader = ImageDownloader(self.client)

    def download_chapter(
        self,
        manga: MangaInfo,
        chapter: Chapter,
        base_dir: Path,
        progress_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> DownloadResult:
        """Download a single chapter.
        
        Args:
            manga: MangaInfo object
            chapter: Chapter to download
            base_dir: Base download directory
            progress_callback: Optional callback(status, completed, total)
            
        Returns:
            DownloadResult with success status and output path
        """
        config = get_config()
        
        # Create chapter directory
        manga_dir = base_dir / sanitize_filename(manga.title)
        
        # Format chapter number properly (handle decimals)
        if chapter.number == int(chapter.number):
            chapter_num = str(int(chapter.number))
        else:
            chapter_num = str(chapter.number)
        
        chapter_name = f"chapter {chapter_num}"
        chapter_dir = manga_dir / sanitize_filename(chapter_name)
        
        try:
            # Fetch chapter pages
            logger.info(f"Fetching pages for {chapter.title}")
            pages = self.client.get_chapter_pages(manga.id, chapter.id)
            
            if not pages:
                return DownloadResult(
                    success=False,
                    chapter=chapter,
                    output_path=str(chapter_dir),
                    error="No pages found in chapter"
                )
            
            # Download images
            def image_progress(completed: int, total: int):
                if progress_callback:
                    progress_callback(f"Downloading {chapter.title}", completed, total)
            
            successful, errors = self.image_downloader.download_chapter_images(
                pages, chapter_dir, image_progress
            )
            
            if successful == 0:
                return DownloadResult(
                    success=False,
                    chapter=chapter,
                    output_path=str(chapter_dir),
                    error=f"Failed to download any images: {errors}"
                )
            
            # Convert format if needed
            output_path = str(chapter_dir)
            
            if config.download_format == "pdf":
                pdf_path = chapter_dir.with_suffix(".pdf")
                convert_to_pdf(chapter_dir, pdf_path)
                output_path = str(pdf_path)
                
                if not config.keep_images:
                    shutil.rmtree(chapter_dir)
                    
            elif config.download_format == "cbz":
                cbz_path = chapter_dir.with_suffix(".cbz")
                convert_to_cbz(chapter_dir, cbz_path, manga, chapter)
                output_path = str(cbz_path)
                
                if not config.keep_images:
                    shutil.rmtree(chapter_dir)
            
            return DownloadResult(
                success=True,
                chapter=chapter,
                output_path=output_path,
                images_downloaded=successful
            )
            
        except Exception as e:
            logger.exception(f"Failed to download chapter: {e}")
            return DownloadResult(
                success=False,
                chapter=chapter,
                output_path=str(chapter_dir),
                error=str(e)
            )

    def download_chapters(
        self,
        manga: MangaInfo,
        chapter_indices: List[int],
        progress_callback: Optional[Callable[[str, int, int, int, int], None]] = None
    ) -> List[DownloadResult]:
        """Download multiple chapters concurrently.
        
        Args:
            manga: MangaInfo object
            chapter_indices: 0-based indices of chapters to download
            progress_callback: Optional callback(chapter_title, chapter_num, total_chapters, images_done, total_images)
            
        Returns:
            List of DownloadResult objects
        """
        config = get_config()
        base_dir = Path(config.download_path)
        concurrent_chapters = config.concurrent_chapters
        
        chapters = [manga.chapters[i] for i in chapter_indices if i < len(manga.chapters)]
        total_chapters = len(chapters)
        
        results: List[DownloadResult] = []
        completed_chapters = 0
        
        def download_task(chapter: Chapter) -> DownloadResult:
            nonlocal completed_chapters
            
            def chapter_progress(status: str, images_done: int, total_images: int):
                if progress_callback:
                    progress_callback(
                        status,
                        completed_chapters + 1,
                        total_chapters,
                        images_done,
                        total_images
                    )
            
            result = self.download_chapter(manga, chapter, base_dir, chapter_progress)
            completed_chapters += 1
            return result
        
        with ThreadPoolExecutor(max_workers=concurrent_chapters) as executor:
            futures = {executor.submit(download_task, ch): ch for ch in chapters}
            
            for future in as_completed(futures):
                results.append(future.result())
        
        return results

    def close(self):
        """Close resources."""
        self.image_downloader.close()
        if self._owns_client:
            self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
