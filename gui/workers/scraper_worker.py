"""Scraper worker for async manga fetching."""

from PyQt6.QtCore import QThread, pyqtSignal

from scraper import MangaScraper
from models import MangaInfo


class ScraperWorker(QThread):
    """Worker thread for fetching manga info without blocking UI."""
    
    finished = pyqtSignal(object)  # MangaInfo or None
    error = pyqtSignal(str)
    
    def __init__(self, url: str, parent=None):
        super().__init__(parent)
        self.url = url
    
    def run(self):
        """Fetch manga info in background thread."""
        try:
            with MangaScraper() as scraper:
                manga = scraper.fetch_manga(self.url)
            
            if manga:
                self.finished.emit(manga)
            else:
                self.error.emit("Failed to fetch manga. Check the URL and try again.")
        except Exception as e:
            self.error.emit(str(e))
