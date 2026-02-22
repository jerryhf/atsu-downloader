"""Settings frame - configuration interface."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSpinBox, QCheckBox, QGroupBox,
    QFileDialog, QMessageBox, QFormLayout
)
from PyQt6.QtCore import Qt

from config import get_config, save_config
from gui.theme import COLORS


class SettingsFrame(QWidget):
    """Settings interface for configuring the downloader."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the settings interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Header
        header = QLabel("⚙️ Settings")
        header.setObjectName("title")
        layout.addWidget(header)
        
        subtitle = QLabel("Configure download preferences and behavior")
        subtitle.setObjectName("subtitle")
        layout.addWidget(subtitle)
        
        layout.addSpacing(16)
        
        # Download Settings Group
        download_group = QGroupBox("Download Settings")
        download_layout = QFormLayout(download_group)
        download_layout.setSpacing(16)
        
        # Download Format
        self.format_combo = QComboBox()
        self.format_combo.addItems(["images", "pdf", "cbz"])
        self.format_combo.setFixedHeight(40)
        download_layout.addRow("Download Format:", self.format_combo)
        
        # Keep Images
        self.keep_images_check = QCheckBox("Keep images after PDF/CBZ conversion")
        self.keep_images_check.setFixedHeight(40)
        download_layout.addRow("", self.keep_images_check)
        
        # Download Path
        path_layout = QHBoxLayout()
        path_layout.setSpacing(8)
        self.path_input = QLineEdit()
        self.path_input.setFixedHeight(40)
        path_layout.addWidget(self.path_input)
        
        browse_btn = QPushButton("Browse")
        browse_btn.setObjectName("secondary")
        browse_btn.setFixedHeight(40)
        browse_btn.setFixedWidth(120)
        browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(browse_btn)
        
        download_layout.addRow("Download Path:", path_layout)
        
        layout.addWidget(download_group)
        
        # Concurrency Settings Group
        concurrency_group = QGroupBox("Concurrency Settings")
        concurrency_layout = QFormLayout(concurrency_group)
        concurrency_layout.setSpacing(16)
        
        # Concurrent Chapters
        self.concurrent_chapters_spin = QSpinBox()
        self.concurrent_chapters_spin.setRange(1, 10)
        self.concurrent_chapters_spin.setFixedWidth(100)
        concurrency_layout.addRow("Concurrent Chapters:", self.concurrent_chapters_spin)
        
        # Concurrent Images
        self.concurrent_images_spin = QSpinBox()
        self.concurrent_images_spin.setRange(1, 20)
        self.concurrent_images_spin.setFixedWidth(100)
        concurrency_layout.addRow("Concurrent Images:", self.concurrent_images_spin)
        
        layout.addWidget(concurrency_group)
        
        # Retry Settings Group
        retry_group = QGroupBox("Retry Settings")
        retry_layout = QFormLayout(retry_group)
        retry_layout.setSpacing(16)
        
        # Max Retries
        self.max_retries_spin = QSpinBox()
        self.max_retries_spin.setRange(1, 10)
        self.max_retries_spin.setFixedWidth(100)
        retry_layout.addRow("Max Retries:", self.max_retries_spin)
        
        # Retry Delay
        self.retry_delay_spin = QSpinBox()
        self.retry_delay_spin.setRange(1, 30)
        self.retry_delay_spin.setSuffix(" seconds")
        self.retry_delay_spin.setFixedWidth(120)
        retry_layout.addRow("Base Retry Delay:", self.retry_delay_spin)
        
        layout.addWidget(retry_group)
        
        # Other Settings Group
        other_group = QGroupBox("Other Settings")
        other_layout = QFormLayout(other_group)
        other_layout.setSpacing(16)
        
        # Enable Logs
        self.enable_logs_check = QCheckBox("Enable detailed logging")
        other_layout.addRow("", self.enable_logs_check)
        
        layout.addWidget(other_group)
        
        # Save Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setObjectName("secondary")
        reset_btn.clicked.connect(self.reset_defaults)
        btn_layout.addWidget(reset_btn)
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(save_btn)
        
        layout.addLayout(btn_layout)
        
        layout.addStretch()
    
    def browse_path(self):
        """Open folder browser dialog."""
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Download Directory",
            self.path_input.text()
        )
        if path:
            self.path_input.setText(path)
    
    def load_settings(self):
        """Load current settings into UI."""
        config = get_config()
        
        # Download settings
        index = self.format_combo.findText(config.download_format)
        if index >= 0:
            self.format_combo.setCurrentIndex(index)
        
        self.keep_images_check.setChecked(config.keep_images)
        self.path_input.setText(config.download_path)
        
        # Concurrency settings
        self.concurrent_chapters_spin.setValue(config.concurrent_chapters)
        self.concurrent_images_spin.setValue(config.concurrent_images)
        
        # Retry settings
        self.max_retries_spin.setValue(config.max_retries)
        self.retry_delay_spin.setValue(config.retry_delay)
        
        # Other settings
        self.enable_logs_check.setChecked(config.enable_logs)
    
    def save_settings(self):
        """Save settings to config file."""
        config = get_config()
        
        # Download settings
        config.download_format = self.format_combo.currentText()
        config.keep_images = self.keep_images_check.isChecked()
        config.download_path = self.path_input.text()
        
        # Concurrency settings
        config.concurrent_chapters = self.concurrent_chapters_spin.value()
        config.concurrent_images = self.concurrent_images_spin.value()
        
        # Retry settings
        config.max_retries = self.max_retries_spin.value()
        config.retry_delay = self.retry_delay_spin.value()
        
        # Other settings
        config.enable_logs = self.enable_logs_check.isChecked()
        
        save_config()
        
        QMessageBox.information(self, "Success", "Settings saved successfully!")
    
    def reset_defaults(self):
        """Reset settings to defaults."""
        from config import Config
        
        reply = QMessageBox.question(
            self, 
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Create default config
            default = Config()
            
            # Update UI
            index = self.format_combo.findText(default.download_format)
            if index >= 0:
                self.format_combo.setCurrentIndex(index)
            
            self.keep_images_check.setChecked(default.keep_images)
            self.path_input.setText(default.download_path)
            self.concurrent_chapters_spin.setValue(default.concurrent_chapters)
            self.concurrent_images_spin.setValue(default.concurrent_images)
            self.max_retries_spin.setValue(default.max_retries)
            self.retry_delay_spin.setValue(default.retry_delay)
            self.enable_logs_check.setChecked(default.enable_logs)
