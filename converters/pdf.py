"""PDF converter for manga chapters."""

import logging
from pathlib import Path
from typing import List

from PIL import Image

logger = logging.getLogger(__name__)


def get_sorted_images(images_dir: Path) -> List[Path]:
    """Get sorted list of image files in directory."""
    extensions = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
    images = [
        f for f in images_dir.iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    ]
    return sorted(images, key=lambda x: x.name)


def convert_to_pdf(images_dir: Path, output_path: Path) -> bool:
    """Convert images in directory to PDF.
    
    Args:
        images_dir: Directory containing images
        output_path: Output PDF file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        images = get_sorted_images(images_dir)
        
        if not images:
            logger.warning(f"No images found in {images_dir}")
            return False
        
        logger.info(f"Converting {len(images)} images to PDF")
        
        # Load first image
        first_image = Image.open(images[0])
        if first_image.mode in ("RGBA", "P"):
            first_image = first_image.convert("RGB")
        
        # Load remaining images
        other_images: List[Image.Image] = []
        for img_path in images[1:]:
            img = Image.open(img_path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            other_images.append(img)
        
        # Save as PDF
        output_path.parent.mkdir(parents=True, exist_ok=True)
        first_image.save(
            output_path,
            "PDF",
            save_all=True,
            append_images=other_images,
            resolution=100.0
        )
        
        # Close images
        first_image.close()
        for img in other_images:
            img.close()
        
        logger.info(f"PDF saved: {output_path}")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to convert to PDF: {e}")
        return False
