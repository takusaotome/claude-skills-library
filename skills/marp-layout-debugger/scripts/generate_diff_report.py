#!/usr/bin/env python3
"""
MARP Layout Diff Report Generator

Creates a side-by-side comparison showing original vs. fixed content
in Markdown format for easy review.

Usage:
    python3 generate_diff_report.py --original slides.md --fixed fixed_slides.md --output diff_report.md
"""

import argparse
import sys
from datetime import datetime, timezone
from difflib import SequenceMatcher, unified_diff
from pathlib import Path
from typing import NamedTuple


class DiffChunk(NamedTuple):
    """Represents a chunk of differences."""

    start_line: int
    original_lines: list[str]
    fixed_lines: list[str]
    category: str


class DiffReportGenerator:
    """Generates visual diff reports between original and fixed MARP files."""

    def __init__(self, original: str, fixed: str, original_name: str, fixed_name: str):
        self.original = original
        self.fixed = fixed
        self.original_name = original_name
        self.fixed_name = fixed_name
        self.original_lines = original.split("\n")
        self.fixed_lines = fixed.split("\n")

    def generate_report(self) -> str:
        """Generate the full diff report in Markdown format."""
        chunks = self._find_diff_chunks()
        stats = self._calculate_stats()

        lines = [
            "# MARP Layout Diff Report",
            "",
            f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "## Summary",
            "",
            f"- **Original file:** `{self.original_name}`",
            f"- **Fixed file:** `{self.fixed_name}`",
            f"- **Lines changed:** {stats['lines_changed']}",
            f"- **Lines added:** {stats['lines_added']}",
            f"- **Lines removed:** {stats['lines_removed']}",
            "",
        ]

        # Categorize changes
        categories = self._categorize_changes(chunks)
        if categories:
            lines.append("## Changes by Category")
            lines.append("")
            for category, count in categories.items():
                lines.append(f"- **{category}:** {count} changes")
            lines.append("")

        # Detailed diff
        lines.append("## Detailed Changes")
        lines.append("")

        if not chunks:
            lines.append("*No changes detected.*")
        else:
            for i, chunk in enumerate(chunks, 1):
                lines.extend(self._format_chunk(chunk, i))

        # Unified diff at the end
        lines.extend(["", "## Unified Diff", "", "```diff"])
        diff = unified_diff(
            self.original_lines, self.fixed_lines, fromfile=self.original_name, tofile=self.fixed_name, lineterm=""
        )
        lines.extend(list(diff))
        lines.extend(["```", ""])

        return "\n".join(lines)

    def _find_diff_chunks(self) -> list[DiffChunk]:
        """Find chunks of differences between the files."""
        chunks = []
        matcher = SequenceMatcher(None, self.original_lines, self.fixed_lines)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                continue

            original_chunk = self.original_lines[i1:i2]
            fixed_chunk = self.fixed_lines[j1:j2]

            # Determine category based on content
            category = self._detect_change_category(original_chunk, fixed_chunk)

            chunks.append(
                DiffChunk(start_line=i1 + 1, original_lines=original_chunk, fixed_lines=fixed_chunk, category=category)
            )

        return chunks

    def _detect_change_category(self, original: list[str], fixed: list[str]) -> str:
        """Detect the category of change based on content."""
        orig_text = "\n".join(original)
        fixed_text = "\n".join(fixed)

        # Whitespace changes
        if orig_text.strip() == fixed_text.strip():
            if "\t" in orig_text and "\t" not in fixed_text:
                return "Tabs to Spaces"
            if orig_text.rstrip() != orig_text:
                return "Trailing Whitespace"
            return "Whitespace"

        # Blank line changes
        if all(l.strip() == "" for l in original) or all(l.strip() == "" for l in fixed):
            return "Blank Lines"

        # List marker changes
        if any(l.lstrip().startswith(("*", "+")) for l in original):
            if any(l.lstrip().startswith("-") for l in fixed):
                return "List Markers"

        # Image sizing
        if "![" in orig_text and "w:" not in orig_text and "w:" in fixed_text:
            return "Image Sizing"

        # CSS fixes
        if "!important" in orig_text or "0px" in orig_text or "0em" in orig_text:
            return "CSS Optimization"

        # Indentation
        if len(orig_text) - len(orig_text.lstrip()) != len(fixed_text) - len(fixed_text.lstrip()):
            return "Indentation"

        return "Other"

    def _calculate_stats(self) -> dict:
        """Calculate diff statistics."""
        matcher = SequenceMatcher(None, self.original_lines, self.fixed_lines)

        lines_changed = 0
        lines_added = 0
        lines_removed = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "replace":
                lines_changed += max(i2 - i1, j2 - j1)
            elif tag == "insert":
                lines_added += j2 - j1
            elif tag == "delete":
                lines_removed += i2 - i1

        return {"lines_changed": lines_changed, "lines_added": lines_added, "lines_removed": lines_removed}

    def _categorize_changes(self, chunks: list[DiffChunk]) -> dict[str, int]:
        """Count changes by category."""
        categories: dict[str, int] = {}
        for chunk in chunks:
            categories[chunk.category] = categories.get(chunk.category, 0) + 1
        return categories

    def _format_chunk(self, chunk: DiffChunk, index: int) -> list[str]:
        """Format a single diff chunk for display."""
        lines = [f"### Change {index}: {chunk.category} (Line {chunk.start_line})", ""]

        # Side-by-side table for small changes
        if len(chunk.original_lines) <= 5 and len(chunk.fixed_lines) <= 5:
            lines.append("| Original | Fixed |")
            lines.append("|----------|-------|")

            max_rows = max(len(chunk.original_lines), len(chunk.fixed_lines))
            for i in range(max_rows):
                orig = chunk.original_lines[i] if i < len(chunk.original_lines) else ""
                fix = chunk.fixed_lines[i] if i < len(chunk.fixed_lines) else ""
                # Escape pipe characters and backticks for table
                orig_escaped = orig.replace("|", "\\|").replace("`", "\\`")
                fix_escaped = fix.replace("|", "\\|").replace("`", "\\`")
                # Truncate long lines
                if len(orig_escaped) > 50:
                    orig_escaped = orig_escaped[:47] + "..."
                if len(fix_escaped) > 50:
                    fix_escaped = fix_escaped[:47] + "..."
                lines.append(f"| `{orig_escaped}` | `{fix_escaped}` |")
        else:
            # Code block diff for larger changes
            lines.append("**Original:**")
            lines.append("```markdown")
            lines.extend(chunk.original_lines[:10])
            if len(chunk.original_lines) > 10:
                lines.append(f"... ({len(chunk.original_lines) - 10} more lines)")
            lines.append("```")
            lines.append("")
            lines.append("**Fixed:**")
            lines.append("```markdown")
            lines.extend(chunk.fixed_lines[:10])
            if len(chunk.fixed_lines) > 10:
                lines.append(f"... ({len(chunk.fixed_lines) - 10} more lines)")
            lines.append("```")

        lines.append("")
        return lines


def main():
    parser = argparse.ArgumentParser(description="Generate visual diff report for MARP layout fixes")
    parser.add_argument("--original", "-a", required=True, help="Original MARP markdown file")
    parser.add_argument("--fixed", "-b", required=True, help="Fixed MARP markdown file")
    parser.add_argument("--output", "-o", help="Output Markdown report file (default: stdout)")

    args = parser.parse_args()

    # Read files
    original_path = Path(args.original)
    fixed_path = Path(args.fixed)

    if not original_path.exists():
        print(f"Error: Original file not found: {args.original}", file=sys.stderr)
        sys.exit(1)

    if not fixed_path.exists():
        print(f"Error: Fixed file not found: {args.fixed}", file=sys.stderr)
        sys.exit(1)

    original = original_path.read_text(encoding="utf-8")
    fixed = fixed_path.read_text(encoding="utf-8")

    # Generate report
    generator = DiffReportGenerator(original, fixed, original_path.name, fixed_path.name)
    report = generator.generate_report()

    # Output
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(report)

    sys.exit(0)


if __name__ == "__main__":
    main()
