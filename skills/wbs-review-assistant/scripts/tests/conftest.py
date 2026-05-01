"""pytest configuration for wbs-review-assistant tests."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

scripts_dir = Path(__file__).resolve().parent.parent

try:
    import openpyxl  # noqa: F401
    import pandas  # noqa: F401

    _HAS_DEPS = True
except ImportError:
    _HAS_DEPS = False
    for mod in [
        "openpyxl",
        "openpyxl.comments",
        "openpyxl.styles",
        "openpyxl.utils",
        "pandas",
    ]:
        if mod not in sys.modules:
            sys.modules[mod] = MagicMock()

sys.path.insert(0, str(scripts_dir))


def pytest_collection_modifyitems(items):
    if not _HAS_DEPS:
        import pytest

        skip_marker = pytest.mark.skip(reason="openpyxl/pandas not installed")
        for item in items:
            item.add_marker(skip_marker)
