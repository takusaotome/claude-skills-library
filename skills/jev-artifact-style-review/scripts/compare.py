#!/usr/bin/env python3
"""Compare two reviews; never authorize artifact release from a style score alone."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jev_review.common import ReviewError, load_json, save_json, save_text
from jev_review.compare import compare_reports


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compare Jev editorial reviews and flag preservation risks.")
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.out.exists():
            raise ReviewError("Comparison output already exists; choose a new filename.")
        result = compare_reports(load_json(args.before), load_json(args.after))
        save_json(args.out, result)
        print(f"{result['direction']}; delta={result['delta_after_minus_before']}; release_approval=false")
        return 0
    except (ReviewError, KeyError, TypeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
