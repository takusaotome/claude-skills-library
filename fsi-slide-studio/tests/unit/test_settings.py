"""Tests for config/settings.py."""

import logging
from pathlib import Path

from config.settings import (
    PROJECT_ROOT,
    REPO_ROOT,
    SKILLS_LIBRARY_PATH,
    DEFAULT_MODEL,
    APP_TITLE,
    SUPPORTED_LANGUAGES,
    OUTPUT_DIR,
    LOG_DIR,
    setup_logging,
)


class TestPaths:
    def test_project_root_is_directory(self):
        assert PROJECT_ROOT.is_dir()

    def test_repo_root_is_parent_of_project_root(self):
        assert REPO_ROOT == PROJECT_ROOT.parent

    def test_skills_library_path_is_directory(self):
        assert SKILLS_LIBRARY_PATH.is_dir()

    def test_output_dir_exists(self):
        assert OUTPUT_DIR.is_dir()

    def test_log_dir_exists(self):
        assert LOG_DIR.is_dir()


class TestDefaults:
    def test_default_model_is_string(self):
        assert isinstance(DEFAULT_MODEL, str)
        assert len(DEFAULT_MODEL) > 0

    def test_app_title(self):
        assert APP_TITLE == "FSI Slide Studio"

    def test_supported_languages(self):
        assert "EN" in SUPPORTED_LANGUAGES
        assert "JP" in SUPPORTED_LANGUAGES


class TestLogging:
    def test_setup_logging_adds_handlers(self):
        setup_logging()
        root = logging.getLogger()
        assert any(
            isinstance(h, (logging.FileHandler, logging.StreamHandler))
            for h in root.handlers
        )
