"""Data models for the Atsu Downloader."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Page:
    """Represents a single page/image in a chapter."""
    id: str
    image: str
    number: int
    width: int = 0
    height: int = 0
    aspect_ratio: float = 0.0

    @property
    def full_url(self) -> str:
        """Get the full image URL."""
        return f"https://atsu.moe{self.image}"


@dataclass
class Chapter:
    """Represents a manga chapter."""
    id: str
    title: str
    number: float
    index: int
    page_count: int
    pages: List[Page] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Chapter":
        """Create a Chapter from API response dict."""
        return cls(
            id=data["id"],
            title=data["title"],
            number=float(data["number"]),
            index=data["index"],
            page_count=data.get("pageCount", 0)
        )


@dataclass
class MangaInfo:
    """Represents manga information and chapters."""
    id: str
    title: str
    manga_type: str
    chapters: List[Chapter] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "MangaInfo":
        """Create MangaInfo from API response dict."""
        chapters: List[Chapter] = []
        seen_chapter_ids = set()
        seen_chapter_keys = set()

        def normalize_number(value: float) -> str:
            if value == int(value):
                return str(int(value))
            return f"{value:.6f}".rstrip("0").rstrip(".")

        for ch in data.get("chapters", []):
            chapter_id = ch.get("id")
            if chapter_id in seen_chapter_ids:
                continue

            chapter = Chapter.from_dict(ch)
            chapter_key = (
                normalize_number(chapter.number),
                chapter.title.strip().lower(),
            )

            if chapter_key in seen_chapter_keys:
                continue

            seen_chapter_ids.add(chapter_id)
            seen_chapter_keys.add(chapter_key)
            chapters.append(chapter)

        return cls(
            id=data["id"],
            title=data["title"],
            manga_type=data.get("type", "Unknown"),
            chapters=chapters
        )


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    chapter: Chapter
    output_path: str
    error: Optional[str] = None
    images_downloaded: int = 0
