"""Pytest configuration for qr-code-generator tests."""

import sys
from pathlib import Path

# Add the scripts directory to the Python path
scripts_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(scripts_dir))
