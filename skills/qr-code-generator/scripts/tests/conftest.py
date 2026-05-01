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
    """Mark only THIS skill's tests as skipped when deps are missing.

    The earlier version applied the skip marker to every collected item,
    which caused the marker to leak into unrelated skills' suites whenever
    pytest was invoked with multiple `skills/.../tests` paths in the same
    session. Constrain the marker to items whose file lives under this
    qr-code-generator tests directory so cross-skill runs are unaffected.
    """
    if _HAS_DEPS:
        return

    import pytest

    own_tests_dir = Path(__file__).resolve().parent
    skip_marker = pytest.mark.skip(reason="qrcode/Pillow not installed")
    for item in items:
        try:
            item_path = Path(item.path)
        except AttributeError:
            # Older pytest exposes .fspath instead of .path
            item_path = Path(str(item.fspath))
        try:
            item_path.relative_to(own_tests_dir)
        except ValueError:
            continue  # not part of this skill's suite — leave it alone
        item.add_marker(skip_marker)
