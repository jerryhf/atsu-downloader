"""ComicInfo.xml generator for CBZ files."""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Optional

from models import MangaInfo, Chapter


def generate_comicinfo(
    manga: MangaInfo,
    chapter: Chapter,
    writer: Optional[str] = None,
    genre: Optional[str] = None
) -> str:
    """Generate ComicInfo.xml content for CBZ metadata.
    
    Args:
        manga: MangaInfo object
        chapter: Chapter object
        writer: Optional writer/author name
        genre: Optional genre string
        
    Returns:
        XML string for ComicInfo.xml
    """
    root = ET.Element("ComicInfo")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    
    # Title and Series
    ET.SubElement(root, "Title").text = chapter.title
    ET.SubElement(root, "Series").text = manga.title
    
    # Chapter number
    if chapter.number == int(chapter.number):
        ET.SubElement(root, "Number").text = str(int(chapter.number))
    else:
        ET.SubElement(root, "Number").text = str(chapter.number)
    
    # Total chapters (count)
    ET.SubElement(root, "Count").text = str(len(manga.chapters))
    
    # Page count
    ET.SubElement(root, "PageCount").text = str(chapter.page_count)
    
    # Manga type (format)
    ET.SubElement(root, "Format").text = manga.manga_type
    
    # Manga indicator
    ET.SubElement(root, "Manga").text = "YesAndRightToLeft" if manga.manga_type == "Manga" else "No"
    
    # Optional fields
    if writer:
        ET.SubElement(root, "Writer").text = writer
    
    if genre:
        ET.SubElement(root, "Genre").text = genre
    
    # Notes/Source
    ET.SubElement(root, "Notes").text = f"Downloaded from atsu.moe using Atsu Downloader"
    ET.SubElement(root, "Web").text = f"https://atsu.moe/manga/{manga.id}"
    
    # Pretty print
    xml_str = ET.tostring(root, encoding="unicode")
    dom = minidom.parseString(xml_str)
    return dom.toprettyxml(indent="  ", encoding=None)
