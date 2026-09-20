"""Deterministic utilities; no network access."""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


class ReviewError(Exception):
    """A safe, user-facing error; never include provider response bodies or secrets."""


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=lambda s: (_ for _ in ()).throw(ValueError("Non-finite JSON number")),
        )
    except (OSError, ValueError, UnicodeError) as exc:
        raise ReviewError(f"Cannot read valid UTF-8 JSON: {path.name}") from exc


def save_json(path: Path, value: Any) -> None:
    save_text(path, json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def save_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(value)
    try:
        path.chmod(0o600)
    except OSError:
        pass


def finite_number(value: Any, low: float, high: float) -> bool:
    return (
        isinstance(value, (float, int))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and low <= value <= high
    )


def load_rubric() -> dict:
    return load_json(ROOT / "assets/rubric.json")
