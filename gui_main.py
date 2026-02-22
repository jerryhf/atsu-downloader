#!/usr/bin/env python3
"""
Atsu Downloader GUI - Download manga from atsu.moe

Usage:
    python gui_main.py
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.app import run_app


if __name__ == "__main__":
    run_app()
