"""Configuration management for Atsu Downloader."""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Literal

# Config file location - in the same directory as this file
CONFIG_FILE = Path(__file__).parent / "config.json"


@dataclass
class Config:
    """Application configuration with defaults."""
    
    # Download settings
    download_format: Literal["images", "pdf", "cbz"] = "images"
    keep_images: bool = True
    download_path: str = "./downloads"
    
    # Concurrency settings
    concurrent_chapters: int = 3
    concurrent_images: int = 5
    
    # Display settings
    max_display_chapters: int = 0  # 0 = show all
    
    # Retry settings
    max_retries: int = 3
    retry_delay: int = 2  # Base delay in seconds
    
    # Logging
    enable_logs: bool = False

    def save(self) -> None:
        """Save configuration to file."""
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from file, or return defaults."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
            except (json.JSONDecodeError, TypeError):
                pass
        return cls()


# Global config instance
_config: Config | None = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def save_config() -> None:
    """Save the current configuration."""
    get_config().save()


def reload_config() -> Config:
    """Reload configuration from file."""
    global _config
    _config = Config.load()
    return _config
