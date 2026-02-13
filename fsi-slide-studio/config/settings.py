"""Application settings for FSI Slide Studio."""

import logging
from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PROJECT_ROOT.parent
SKILLS_LIBRARY_PATH = Path(
    os.getenv("SKILLS_LIBRARY_PATH", str(REPO_ROOT / "skills"))
)
PRESENTATION_TEMPLATE_PATH = (
    SKILLS_LIBRARY_PATH
    / "fujisoft-presentation-creator"
    / "assets"
    / "FUJISOFT_America_Slide_Template.md"
)
SKILL_CATEGORIES_PATH = PROJECT_ROOT / "config" / "skill_categories.yaml"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(exist_ok=True)

# Model
DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")

# Anthropic API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "fsi-slide-studio.log"


def setup_logging():
    """Configure structured logging for the application."""
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


# App
APP_TITLE = "FSI Slide Studio"
APP_ICON = "🎨"
DEFAULT_LANGUAGE = "JP"
SUPPORTED_LANGUAGES = ["EN", "JP"]
