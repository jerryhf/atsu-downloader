"""CBZ converter for manga chapters."""

import logging
import zipfile
from pathlib import Path
from typing import Optional

from models import MangaInfo, Chapter
from .comicinfo import generate_comicinfo

logger = logging.getLogger(__name__)


def convert_to_cbz(
    images_dir: Path,
    output_path: Path,
    manga: Optional[MangaInfo] = None,
    chapter: Optional[Chapter] = None
) -> bool:
    """Convert images in directory to CBZ archive.
    
    Args:
        images_dir: Directory containing images
        output_path: Output CBZ file path
        manga: Optional MangaInfo for ComicInfo.xml
        chapter: Optional Chapter for ComicInfo.xml
        
    Returns:
        True if successful, False otherwise
    """
    try:
        extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
        images = sorted([
            f for f in images_dir.iterdir()
            if f.is_file() and f.suffix.lower() in extensions
        ], key=lambda x: x.name)
        
        if not images:
            logger.warning(f"No images found in {images_dir}")
            return False
        
        logger.info(f"Creating CBZ with {len(images)} images")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_STORED) as cbz:
            # Add images
            for img_path in images:
                cbz.write(img_path, img_path.name)
            
            # Add ComicInfo.xml if we have metadata
            if manga and chapter:
                comicinfo = generate_comicinfo(manga, chapter)
                cbz.writestr("ComicInfo.xml", comicinfo)
        
        logger.info(f"CBZ saved: {output_path}")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to create CBZ: {e}")
        return False
