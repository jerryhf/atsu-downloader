"""Theme and styling for the Atsu Downloader GUI."""

# Color Palette - Modern Dark Theme
COLORS = {
    "bg_dark": "#0d1117",
    "bg_card": "#161b22",
    "bg_input": "#21262d",
    "border": "#30363d",
    "text_primary": "#f0f6fc",
    "text_secondary": "#8b949e",
    "accent": "#58a6ff",
    "accent_hover": "#79c0ff",
    "success": "#3fb950",
    "error": "#f85149",
    "warning": "#d29922",
}

# Stylesheet for PyQt6
STYLESHEET = f"""
QMainWindow {{
    background-color: {COLORS['bg_dark']};
}}

QWidget {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 13px;
}}

QLabel {{
    color: {COLORS['text_primary']};
    background-color: transparent;
}}

QLabel#title {{
    font-size: 24px;
    font-weight: bold;
    color: {COLORS['accent']};
}}

QLabel#subtitle {{
    font-size: 14px;
    color: {COLORS['text_secondary']};
}}

QLineEdit {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 10px 14px;
    color: {COLORS['text_primary']};
    font-size: 14px;
}}

QLineEdit:focus {{
    border-color: {COLORS['accent']};
}}

QPushButton {{
    background-color: {COLORS['accent']};
    color: {COLORS['bg_dark']};
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 13px;
}}

QPushButton:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['accent']};
}}

QPushButton:disabled {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_secondary']};
}}

QPushButton#secondary {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
}}

QPushButton#secondary:hover {{
    background-color: {COLORS['border']};
}}

QPushButton#success {{
    background-color: {COLORS['success']};
}}

QComboBox {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text_primary']};
}}

QComboBox:hover {{
    border-color: {COLORS['accent']};
}}

QComboBox::drop-down {{
    border: none;
    width: 30px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS['text_secondary']};
    margin-right: 10px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    selection-background-color: {COLORS['accent']};
    selection-color: {COLORS['bg_dark']};
}}

QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 8px 12px;
    color: {COLORS['text_primary']};
}}

QCheckBox {{
    spacing: 8px;
    color: {COLORS['text_primary']};
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 1px solid {COLORS['border']};
    background-color: {COLORS['bg_input']};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QListWidget {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px;
    outline: none;
}}

QListWidget::item {{
    padding: 8px 12px;
    border-radius: 4px;
    margin: 2px 0;
}}

QListWidget::item:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['bg_dark']};
}}

QListWidget::item:hover {{
    background-color: {COLORS['bg_input']};
}}

QProgressBar {{
    background-color: {COLORS['bg_input']};
    border: none;
    border-radius: 6px;
    height: 12px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 6px;
}}

QScrollBar:vertical {{
    background-color: {COLORS['bg_dark']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS['border']};
    border-radius: 6px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS['text_secondary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    background-color: {COLORS['bg_card']};
}}

QTabBar::tab {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text_secondary']};
    padding: 12px 24px;
    margin-right: 4px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['accent']};
    font-weight: bold;
}}

QTabBar::tab:hover {{
    color: {COLORS['text_primary']};
}}

QGroupBox {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
    color: {COLORS['accent']};
}}

QTextEdit {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px;
    color: {COLORS['text_primary']};
    font-family: 'Consolas', 'Courier New', monospace;
}}
"""
