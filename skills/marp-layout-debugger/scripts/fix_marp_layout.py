#!/usr/bin/env python3
"""
MARP Layout Fixer

Applies automated fixes for MARP layout issues identified by the analyzer.
Only applies fixes that are marked as auto_fixable to ensure safety.

Usage:
    python3 fix_marp_layout.py --input slides.md --report analysis.json --output fixed.md
    python3 fix_marp_layout.py --input slides.md --report analysis.json --output fixed.md --auto-only
    python3 fix_marp_layout.py --input slides.md --report analysis.json --dry-run
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class Fix:
    """Represents a fix to be applied."""

    issue_id: str
    line: int
    original: str
    fixed: str
    description: str


class MarpLayoutFixer:
    """Applies fixes to MARP files based on analysis report."""

    def __init__(self, content: str, report: dict):
        self.original_content = content
        self.lines = content.split("\n")
        self.report = report
        self.fixes_applied: list[Fix] = []

    def apply_fixes(self, auto_only: bool = True) -> str:
        """Apply fixes and return corrected content."""
        issues = self.report.get("issues", [])

        # Filter to auto-fixable if requested
        if auto_only:
            issues = [i for i in issues if i.get("auto_fixable", False)]

        # Sort by line number descending to avoid offset issues
        issues = sorted(issues, key=lambda x: x.get("line", 0), reverse=True)

        for issue in issues:
            self._apply_fix(issue)

        # Post-process: collapse multiple blank lines
        self._collapse_blank_lines()

        return "\n".join(self.lines)

    def _apply_fix(self, issue: dict) -> None:
        """Apply a single fix based on issue type."""
        issue_id = issue.get("id", "")
        line_num = issue.get("line", 0) - 1  # Convert to 0-indexed

        if line_num < 0 or line_num >= len(self.lines):
            return

        original = self.lines[line_num]
        fixed = original

        if issue_id == "WS001":
            # Double blank lines - mark for later collapse
            pass  # Handled in post-process

        elif issue_id == "WS002":
            # Trailing whitespace
            fixed = original.rstrip()

        elif issue_id == "WS003":
            # Tabs to spaces
            fixed = original.replace("\t", "  ")

        elif issue_id == "WS004":
            # Missing blank line before header
            self.lines.insert(line_num, "")
            self.fixes_applied.append(
                Fix(
                    issue_id=issue_id,
                    line=line_num + 1,
                    original="(no blank line)",
                    fixed="(blank line inserted)",
                    description="Added blank line before header",
                )
            )
            return

        elif issue_id == "BL001":
            # Mixed list markers - normalize to dash
            fixed = re.sub(r"^(\s*)[*+](\s)", r"\1-\2", original)

        elif issue_id == "BL002":
            # 4-space to 2-space indent
            match = re.match(r"^(\s+)", original)
            if match:
                indent = match.group(1)
                new_indent = "  " * (len(indent) // 4 * 2)
                if len(indent) % 4 == 2:
                    new_indent += "  "
                fixed = new_indent + original.lstrip()

        elif issue_id == "BL003":
            # Missing space after marker
            fixed = re.sub(r"^(\s*[-*+])([^\s])", r"\1 \2", original)

        elif issue_id == "OF002":
            # Unsized image - add default width
            fixed = re.sub(
                r"!\[([^\]]*)\]\(([^)]+)\)",
                lambda m: (
                    f"![w:800 {m.group(1)}]({m.group(2)})"
                    if "w:" not in m.group(1) and "h:" not in m.group(1)
                    else m.group(0)
                ),
                original,
            )

        elif issue_id == "CS004":
            # Zero with unit
            fixed = re.sub(r":\s*0(px|em|rem|%)", ": 0", original)

        if fixed != original:
            self.lines[line_num] = fixed
            self.fixes_applied.append(
                Fix(
                    issue_id=issue_id,
                    line=line_num + 1,
                    original=original,
                    fixed=fixed,
                    description=issue.get("suggestion", "Applied fix"),
                )
            )

    def _collapse_blank_lines(self) -> None:
        """Collapse multiple consecutive blank lines into single blank lines."""
        new_lines = []
        prev_blank = False

        for line in self.lines:
            is_blank = line.strip() == ""
            if is_blank and prev_blank:
                continue  # Skip consecutive blank
            new_lines.append(line)
            prev_blank = is_blank

        if len(new_lines) != len(self.lines):
            self.fixes_applied.append(
                Fix(
                    issue_id="WS001",
                    line=0,
                    original=f"{len(self.lines)} lines",
                    fixed=f"{len(new_lines)} lines",
                    description="Collapsed multiple blank lines",
                )
            )

        self.lines = new_lines

    def get_fix_summary(self) -> dict:
        """Return summary of fixes applied."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_fixes": len(self.fixes_applied),
            "fixes": [
                {"issue_id": f.issue_id, "line": f.line, "description": f.description} for f in self.fixes_applied
            ],
        }


def main():
    parser = argparse.ArgumentParser(description="Apply automated fixes to MARP layout issues")
    parser.add_argument("--input", "-i", required=True, help="Input MARP markdown file")
    parser.add_argument("--report", "-r", required=True, help="Analysis report JSON file from analyze_marp_layout.py")
    parser.add_argument("--output", "-o", help="Output fixed markdown file (default: stdout)")
    parser.add_argument(
        "--auto-only", action="store_true", default=True, help="Only apply auto-fixable issues (default: True)"
    )
    parser.add_argument("--all", action="store_true", help="Attempt to fix all issues (may require manual review)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without making changes")
    parser.add_argument("--backup", action="store_true", help="Create backup of original file")

    args = parser.parse_args()

    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Read report file
    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Error: Report file not found: {args.report}", file=sys.stderr)
        sys.exit(1)

    content = input_path.read_text(encoding="utf-8")
    report = json.loads(report_path.read_text(encoding="utf-8"))

    # Create backup if requested
    if args.backup and args.output:
        backup_path = input_path.with_suffix(f".{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")
        backup_path.write_text(content, encoding="utf-8")
        print(f"Backup created: {backup_path}", file=sys.stderr)

    # Apply fixes
    auto_only = not args.all
    fixer = MarpLayoutFixer(content, report)

    if args.dry_run:
        # Dry run - just show what would be fixed
        fixer.apply_fixes(auto_only=auto_only)
        summary = fixer.get_fix_summary()
        print("# Dry Run - Fixes that would be applied:", file=sys.stderr)
        print(f"Total fixes: {summary['total_fixes']}", file=sys.stderr)
        for fix in summary["fixes"]:
            print(f"  - Line {fix['line']}: [{fix['issue_id']}] {fix['description']}", file=sys.stderr)
        sys.exit(0)

    fixed_content = fixer.apply_fixes(auto_only=auto_only)
    summary = fixer.get_fix_summary()

    # Output results
    if args.output:
        Path(args.output).write_text(fixed_content, encoding="utf-8")
        print(f"Fixed file written to: {args.output}", file=sys.stderr)
    else:
        print(fixed_content)

    # Print summary
    print("\n# Fix Summary", file=sys.stderr)
    print(f"Total fixes applied: {summary['total_fixes']}", file=sys.stderr)
    for fix in summary["fixes"]:
        print(f"  - Line {fix['line']}: [{fix['issue_id']}] {fix['description']}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
