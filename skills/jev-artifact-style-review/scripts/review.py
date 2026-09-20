#!/usr/bin/env python3
"""Usage: review.py draft.md --language ja --profile email --dry-run --out runs/check"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jev_review.client import JevClient
from jev_review.common import ReviewError, load_json, load_rubric, save_json, save_text
from jev_review.extract import extract
from jev_review.pipeline import build_plan, execute
from jev_review.questions import validate_context
from jev_review.reporting import make_handoff, render_report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Japanese-first, bilingual editorial style review. NOT an AI authorship detector."
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--context", type=Path)
    parser.add_argument("--language", choices=["ja", "en", "mixed", "auto"], default="ja")
    parser.add_argument("--report-language", choices=["ja", "en"])
    parser.add_argument(
        "--profile", choices=["email", "chat", "report", "proposal", "technical", "slides", "formal"], default="email"
    )
    parser.add_argument("--model", default="jev-1.13.0")
    parser.add_argument(
        "--out", type=Path, required=True, help="New or empty output directory; existing results are never overwritten."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Local extraction and request preview only; no Jev score."
    )
    parser.add_argument(
        "--allow-remote",
        action="store_true",
        help="Explicitly authorize sending extracted prose and brief to TypeSafe.",
    )
    parser.add_argument("--chunk-chars", type=int, default=2600)
    parser.add_argument("--max-chunks", type=int, default=128)
    parser.add_argument("--max-requests", type=int, default=150)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args(argv)
    created = False
    try:
        if not args.input.is_file():
            raise ReviewError("Input file does not exist.")
        if args.out.exists() and (not args.out.is_dir() or any(args.out.iterdir())):
            raise ReviewError("Output directory must be new or empty; existing evaluations are not overwritten.")
        if not args.dry_run and not args.allow_remote:
            raise ReviewError(
                "Use --dry-run for a local preview, or explicitly authorize TypeSafe sending with --allow-remote."
            )
        context = validate_context(load_json(args.context) if args.context else {})
        document = extract(args.input, context.get("locked_sections", []))
        language = args.language if args.language != "auto" else document["detected_language"]
        if language == "unknown":
            raise ReviewError("Unable to determine language. Specify --language ja or en.")
        rubric = load_rubric()
        plan = build_plan(
            document,
            context,
            rubric,
            profile=args.profile,
            language=language,
            model=args.model,
            chunk_chars=args.chunk_chars,
            max_chunks=args.max_chunks,
            top_k=args.top_k,
            max_requests=args.max_requests,
            workers=args.workers,
        )
        # Validate key before creating local artifacts for a live run.
        client = None if args.dry_run else JevClient(allow_remote=args.allow_remote, max_requests=args.max_requests)
        args.out.mkdir(parents=True, exist_ok=True)
        created = True
        try:
            args.out.chmod(0o700)
        except OSError:
            pass
        save_json(args.out / "extracted.json", document)
        save_json(args.out / "context.json", context)
        public_plan = {k: v for k, v in plan.items() if k not in {"dimensions", "chunks", "payloads"}}
        public_plan["mode"] = "dry_run" if args.dry_run else "live_planned"
        public_plan["warning"] = "Contains private text in other output files. Do not commit this directory."
        save_json(args.out / "plan.json", public_plan)
        if args.dry_run:
            save_json(args.out / "request_preview.json", plan["payloads"])
            print(
                f"DRY RUN ONLY: {len(plan['chunks'])} fragments; at most {plan['planned_calls_upper_bound']} logical API calls. No Jev scores produced."
            )
            return 0
        report = execute(document, context, rubric, plan, client)
        save_json(args.out / "review.json", report)
        save_text(
            args.out / "review.md", render_report(report, args.report_language or ("en" if language == "en" else "ja"))
        )
        save_json(args.out / "writer_handoff.json", make_handoff(report, context))
        save_json(args.out / "run_status.json", {"status": "completed", "release_approval": False})
        print(
            f"Review written to {args.out}; status={report['status']}; style_index={report['summary']['style_index_0_to_100']}. Not an authorship probability."
        )
        return 0
    except ReviewError as exc:
        if created:
            save_json(args.out / "run_status.json", {"status": "failed", "release_approval": False, "error": str(exc)})
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        # Avoid leaking provider data in tracebacks. A maintainer can reproduce locally with synthetic inputs.
        if created:
            save_json(
                args.out / "run_status.json",
                {"status": "failed", "release_approval": False, "error_type": type(exc).__name__},
            )
        print(f"ERROR: Review failed ({type(exc).__name__}); no approval produced.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
