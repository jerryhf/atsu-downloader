#!/usr/bin/env python3
"""
Atsu Downloader - Download manga from atsu.moe

Usage:
    python main.py              # Interactive mode
    python main.py <url>        # Download specific manga
    python main.py <url> -c all # Download all chapters
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from cli import app


if __name__ == "__main__":
    app()
