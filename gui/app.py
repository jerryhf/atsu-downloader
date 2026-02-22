"""Main application window for Atsu Downloader GUI."""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTabWidget, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from gui.theme import STYLESHEET, COLORS
from gui.frames import DownloadFrame, SettingsFrame


class AtsuApp(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atsu Downloader")
        self.setMinimumSize(900, 700)
        self.resize(1000, 750)
        
        # Apply stylesheet
        self.setStyleSheet(STYLESHEET)
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main window UI."""
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLORS['bg_card']}; padding: 16px;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        title = QLabel("ATSU DOWNLOADER")
        title.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {COLORS['accent']};
            letter-spacing: 2px;
        """)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Download manga from atsu.moe with ease")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px;")
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        
        # Download tab
        self.download_frame = DownloadFrame()
        self.tabs.addTab(self.download_frame, "📥 Download")
        
        # Settings tab
        self.settings_frame = SettingsFrame()
        self.tabs.addTab(self.settings_frame, "⚙️ Settings")
        
        layout.addWidget(self.tabs)


def run_app():
    """Run the application."""
    import sys
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = AtsuApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
