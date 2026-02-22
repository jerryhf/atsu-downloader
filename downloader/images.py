"""Image downloader with concurrent downloads and retry logic."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from api.client import AtsuClient
from config import get_config
from models import Page

logger = logging.getLogger(__name__)


class ImageDownloader:
    """Downloads chapter images with concurrency and retry support."""

    def __init__(self, client: Optional[AtsuClient] = None):
        self.client = client or AtsuClient()
        self._owns_client = client is None

    def download_image_with_retry(
        self,
        page: Page,
        output_path: Path
    ) -> Tuple[bool, str]:
        """Download a single image with retry logic.
        
        Returns:
            Tuple of (success, error_message)
        """
        config = get_config()
        max_retries = config.max_retries
        base_delay = config.retry_delay
        
        for attempt in range(max_retries):
            try:
                image_data = self.client.download_image(page.image)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_data)
                logger.debug(f"Downloaded: {output_path.name}")
                return True, ""
            except Exception as e:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"Image download failed (attempt {attempt + 1}/{max_retries}), "
                        f"retrying in {delay}s: {e}"
                    )
                    time.sleep(delay)
                else:
                    error_msg = f"Failed to download {page.image}: {e}"
                    logger.error(error_msg)
                    return False, error_msg
        
        return False, "Max retries exceeded"

    def download_chapter_images(
        self,
        pages: List[Page],
        output_dir: Path,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> Tuple[int, List[str]]:
        """Download all chapter images concurrently.
        
        Args:
            pages: List of Page objects to download
            output_dir: Directory to save images
            progress_callback: Optional callback(completed, total) for progress updates
            
        Returns:
            Tuple of (successful_count, list_of_errors)
        """
        config = get_config()
        concurrent = config.concurrent_images
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        successful = 0
        errors: List[str] = []
        total = len(pages)
        
        def download_task(page: Page) -> Tuple[bool, str]:
            # Determine extension from image path
            ext = Path(page.image).suffix or ".webp"
            # Use zero-padded numbering for proper sorting
            filename = f"{page.number:04d}{ext}"
            output_path = output_dir / filename
            return self.download_image_with_retry(page, output_path)
        
        with ThreadPoolExecutor(max_workers=concurrent) as executor:
            futures = {executor.submit(download_task, page): page for page in pages}
            
            for future in as_completed(futures):
                success, error = future.result()
                if success:
                    successful += 1
                else:
                    errors.append(error)
                
                if progress_callback:
                    progress_callback(successful + len(errors), total)
        
        logger.info(f"Downloaded {successful}/{total} images")
        return successful, errors

    def close(self):
        """Close resources."""
        if self._owns_client:
            self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
