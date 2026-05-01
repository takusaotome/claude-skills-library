"""Pytest configuration for qr-code-generator tests."""

import sys
from pathlib import Path
from unittest.mock import MagicMock

scripts_dir = Path(__file__).resolve().parents[1]

try:
    import qrcode  # noqa: F401
    from PIL import Image  # noqa: F401

    _HAS_DEPS = True
except ImportError:
    _HAS_DEPS = False
    sys.modules["qrcode"] = MagicMock()
    sys.modules["qrcode.constants"] = MagicMock()
    sys.modules["PIL"] = MagicMock()
    sys.modules["PIL.Image"] = MagicMock()

sys.path.insert(0, str(scripts_dir))


def pytest_collection_modifyitems(items):
    if not _HAS_DEPS:
        import pytest

        skip_marker = pytest.mark.skip(reason="qrcode/Pillow not installed")
        for item in items:
            item.add_marker(skip_marker)
