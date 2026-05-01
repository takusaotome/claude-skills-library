#!/usr/bin/env python3
"""
MARP Layout Analyzer

Analyzes MARP markdown files for common layout issues including:
- Whitespace problems (WS001-WS004)
- Alignment issues (AL001-AL004)
- Bullet formatting (BL001-BL004)
- Overflow risks (OF001-OF004)
- CSS issues (CS001-CS004)

Usage:
    python3 analyze_marp_layout.py --input slides.md --output report.json
"""

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class Issue:
    """Represents a detected layout issue."""

    id: str
    category: str
    severity: str
    line: int
    column: int
    description: str
    suggestion: str
    auto_fixable: bool
    context: str = ""


@dataclass
class CSSAnalysis:
    """CSS-specific analysis results."""

    total_rules: int = 0
    redundant_rules: int = 0
    specificity_warnings: int = 0


class MarpLayoutAnalyzer:
    """Analyzes MARP files for layout issues."""

    # Issue severity levels
    SEVERITY_LOW = "low"
    SEVERITY_MEDIUM = "medium"
    SEVERITY_HIGH = "high"

    # Code block line length threshold
    CODE_LINE_MAX_LENGTH = 80

    # Table column threshold
    TABLE_MAX_COLUMNS = 5
    TABLE_CELL_MAX_LENGTH = 30

    def __init__(self, content: str, filename: str = "slides.md"):
        self.content = content
        self.filename = filename
        self.lines = content.split("\n")
        self.issues: list[Issue] = []
        self.css_analysis = CSSAnalysis()

    def analyze(self) -> dict:
        """Run all analysis checks and return results."""
        self._check_whitespace_issues()
        self._check_bullet_issues()
        self._check_overflow_issues()
        self._check_css_issues()
        self._check_alignment_issues()

        # Count issues by category
        issues_by_category: dict[str, int] = {}
        for issue in self.issues:
            issues_by_category[issue.category] = issues_by_category.get(issue.category, 0) + 1

        auto_fixable_count = sum(1 for issue in self.issues if issue.auto_fixable)

        return {
            "schema_version": "1.0",
            "file": self.filename,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_issues": len(self.issues),
            "auto_fixable_count": auto_fixable_count,
            "manual_review_count": len(self.issues) - auto_fixable_count,
            "issues_by_category": issues_by_category,
            "issues": [asdict(issue) for issue in self.issues],
            "css_analysis": asdict(self.css_analysis),
        }

    def _add_issue(
        self,
        id: str,
        category: str,
        severity: str,
        line: int,
        column: int,
        description: str,
        suggestion: str,
        auto_fixable: bool,
        context: str = "",
    ) -> None:
        """Add a new issue to the list."""
        self.issues.append(
            Issue(
                id=id,
                category=category,
                severity=severity,
                line=line,
                column=column,
                description=description,
                suggestion=suggestion,
                auto_fixable=auto_fixable,
                context=context,
            )
        )

    def _check_whitespace_issues(self) -> None:
        """Check for whitespace-related issues."""
        # WS001: Double or more blank lines
        blank_count = 0
        for i, line in enumerate(self.lines):
            if line.strip() == "":
                blank_count += 1
                if blank_count >= 2:
                    self._add_issue(
                        id="WS001",
                        category="whitespace",
                        severity=self.SEVERITY_LOW,
                        line=i + 1,
                        column=0,
                        description="Multiple consecutive blank lines create excessive gaps",
                        suggestion="Reduce to a single blank line",
                        auto_fixable=True,
                        context=f"Lines {i - blank_count + 2}-{i + 1} are blank",
                    )
            else:
                blank_count = 0

        # WS002: Trailing whitespace
        for i, line in enumerate(self.lines):
            if line != line.rstrip():
                trailing = len(line) - len(line.rstrip())
                self._add_issue(
                    id="WS002",
                    category="whitespace",
                    severity=self.SEVERITY_LOW,
                    line=i + 1,
                    column=len(line.rstrip()),
                    description=f"Trailing whitespace ({trailing} characters)",
                    suggestion="Remove trailing whitespace",
                    auto_fixable=True,
                    context=repr(line[-trailing:]),
                )

        # WS003: Mixed tabs and spaces
        for i, line in enumerate(self.lines):
            if "\t" in line:
                self._add_issue(
                    id="WS003",
                    category="whitespace",
                    severity=self.SEVERITY_MEDIUM,
                    line=i + 1,
                    column=line.index("\t"),
                    description="Tab character found (inconsistent with space indentation)",
                    suggestion="Convert tabs to spaces (2 spaces per tab)",
                    auto_fixable=True,
                    context=repr(line[:20]),
                )

        # WS004: Missing blank line before headers
        for i, line in enumerate(self.lines):
            if i > 0 and line.startswith("#") and self.lines[i - 1].strip() != "":
                # Check if previous line is not a slide separator
                if self.lines[i - 1].strip() != "---":
                    self._add_issue(
                        id="WS004",
                        category="whitespace",
                        severity=self.SEVERITY_LOW,
                        line=i + 1,
                        column=0,
                        description="Header without preceding blank line",
                        suggestion="Add blank line before header for readability",
                        auto_fixable=True,
                        context=f"Previous line: {self.lines[i - 1][:30]}",
                    )

    def _check_bullet_issues(self) -> None:
        """Check for bullet/list formatting issues."""
        in_list = False
        list_marker = None

        for i, line in enumerate(self.lines):
            stripped = line.lstrip()

            # BL003: Missing space after marker
            if re.match(r"^[-*+][^\s]", stripped):
                self._add_issue(
                    id="BL003",
                    category="bullets",
                    severity=self.SEVERITY_HIGH,
                    line=i + 1,
                    column=len(line) - len(stripped) + 1,
                    description="List marker without following space (won't render as list)",
                    suggestion="Add space after the list marker",
                    auto_fixable=True,
                    context=stripped[:20],
                )

            # Check for list items
            list_match = re.match(r"^([-*+])\s", stripped)
            if list_match:
                current_marker = list_match.group(1)

                if in_list and list_marker and current_marker != list_marker:
                    # BL001: Mixed list markers
                    self._add_issue(
                        id="BL001",
                        category="bullets",
                        severity=self.SEVERITY_LOW,
                        line=i + 1,
                        column=len(line) - len(stripped),
                        description=f"Mixed list markers ('{current_marker}' vs '{list_marker}')",
                        suggestion=f"Use consistent marker '{list_marker}' throughout",
                        auto_fixable=True,
                        context=stripped[:20],
                    )

                in_list = True
                if list_marker is None:
                    list_marker = current_marker

                # BL002: 4-space indent (should be 2)
                indent = len(line) - len(stripped)
                if indent > 0 and indent % 4 == 0 and indent % 2 == 0:
                    # Check if it's likely 4-space nesting
                    if indent >= 4:
                        self._add_issue(
                            id="BL002",
                            category="bullets",
                            severity=self.SEVERITY_MEDIUM,
                            line=i + 1,
                            column=0,
                            description=f"4-space indentation detected ({indent} spaces)",
                            suggestion="Use 2-space indentation for nested lists",
                            auto_fixable=True,
                            context=f"Indent: {indent} spaces",
                        )
            elif stripped == "":
                # Reset list tracking on blank line
                in_list = False
                list_marker = None

    def _check_overflow_issues(self) -> None:
        """Check for content overflow risks."""
        in_code_block = False
        code_block_start = 0

        for i, line in enumerate(self.lines):
            # Track code blocks
            if line.strip().startswith("```"):
                if in_code_block:
                    in_code_block = False
                else:
                    in_code_block = True
                    code_block_start = i
                continue

            # OF001: Long code lines
            if in_code_block and len(line) > self.CODE_LINE_MAX_LENGTH:
                self._add_issue(
                    id="OF001",
                    category="overflow",
                    severity=self.SEVERITY_HIGH,
                    line=i + 1,
                    column=self.CODE_LINE_MAX_LENGTH,
                    description=f"Code line exceeds {self.CODE_LINE_MAX_LENGTH} characters ({len(line)} chars)",
                    suggestion="Break into multiple lines or reduce font size",
                    auto_fixable=False,
                    context=line[:50] + "...",
                )

            # OF002: Unsized images
            img_match = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            if img_match:
                alt_text = img_match.group(1)
                if not re.search(r"[wh]:\d+", alt_text):
                    self._add_issue(
                        id="OF002",
                        category="overflow",
                        severity=self.SEVERITY_MEDIUM,
                        line=i + 1,
                        column=img_match.start(),
                        description="Image without size constraint may overflow",
                        suggestion="Add width/height: ![w:800](image.png)",
                        auto_fixable=True,
                        context=img_match.group(0)[:40],
                    )

            # OF003: Wide tables
            if "|" in line and line.count("|") > self.TABLE_MAX_COLUMNS + 1:
                self._add_issue(
                    id="OF003",
                    category="overflow",
                    severity=self.SEVERITY_MEDIUM,
                    line=i + 1,
                    column=0,
                    description=f"Table has many columns ({line.count('|') - 1} columns)",
                    suggestion="Consider reducing columns or using smaller font",
                    auto_fixable=False,
                    context=f"{line.count('|') - 1} columns",
                )

    def _check_css_issues(self) -> None:
        """Check for CSS-related issues in style blocks."""
        in_style = False
        style_content = []
        style_start = 0

        for i, line in enumerate(self.lines):
            if "<style" in line.lower():
                in_style = True
                style_start = i
                continue
            if "</style>" in line.lower():
                in_style = False
                self._analyze_css_block("\n".join(style_content), style_start)
                style_content = []
                continue
            if in_style:
                style_content.append(line)

        # Also check for inline style attributes
        for i, line in enumerate(self.lines):
            if "!important" in line:
                self._add_issue(
                    id="CS002",
                    category="css",
                    severity=self.SEVERITY_MEDIUM,
                    line=i + 1,
                    column=line.index("!important"),
                    description="!important usage can cause cascade problems",
                    suggestion="Increase selector specificity instead",
                    auto_fixable=False,
                    context=line.strip()[:40],
                )

    def _analyze_css_block(self, css: str, start_line: int) -> None:
        """Analyze a CSS block for issues."""
        # Count rules (simple approximation)
        rules = re.findall(r"\{[^}]+\}", css)
        self.css_analysis.total_rules = len(rules)

        # CS003: Check for !important
        important_count = css.count("!important")
        if important_count > 0:
            self.css_analysis.specificity_warnings = important_count

        # CS004: Check for 0px, 0em, etc.
        zero_units = re.findall(r":\s*0(px|em|rem|%)", css)
        for match in zero_units:
            # Find line number within CSS block
            self._add_issue(
                id="CS004",
                category="css",
                severity=self.SEVERITY_LOW,
                line=start_line + 1,
                column=0,
                description=f"Zero value with unnecessary unit (0{match})",
                suggestion="Use just '0' without unit",
                auto_fixable=True,
                context=f"0{match} -> 0",
            )

    def _check_alignment_issues(self) -> None:
        """Check for alignment/layout issues in CSS."""
        for i, line in enumerate(self.lines):
            # AL001: margin-right in flex children (common anti-pattern)
            if re.search(r"margin-right\s*:", line) and "flex" not in self.content[: i * 50]:
                self._add_issue(
                    id="AL001",
                    category="alignment",
                    severity=self.SEVERITY_MEDIUM,
                    line=i + 1,
                    column=line.index("margin"),
                    description="margin-right in flex child (consider using gap instead)",
                    suggestion="Use gap property on flex parent",
                    auto_fixable=False,
                    context=line.strip()[:40],
                )

            # AL002: Fixed width with flex
            if re.search(r"width\s*:\s*\d+px", line):
                # Check if flex is nearby
                context_start = max(0, i - 5)
                context = "\n".join(self.lines[context_start : i + 5])
                if "flex:" in context or "flex-" in context:
                    self._add_issue(
                        id="AL002",
                        category="alignment",
                        severity=self.SEVERITY_MEDIUM,
                        line=i + 1,
                        column=0,
                        description="Fixed pixel width may conflict with flex layout",
                        suggestion="Use flex-basis instead of width",
                        auto_fixable=False,
                        context=line.strip()[:40],
                    )


def main():
    parser = argparse.ArgumentParser(description="Analyze MARP markdown files for layout issues")
    parser.add_argument("--input", "-i", required=True, help="Input MARP markdown file")
    parser.add_argument("--output", "-o", help="Output JSON report file (default: stdout)")
    parser.add_argument("--format", choices=["json", "summary"], default="json", help="Output format (default: json)")

    args = parser.parse_args()

    # Read input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    content = input_path.read_text(encoding="utf-8")

    # Run analysis
    analyzer = MarpLayoutAnalyzer(content, input_path.name)
    report = analyzer.analyze()

    # Output results
    if args.format == "json":
        output = json.dumps(report, indent=2)
    else:
        output = format_summary(report)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(output)

    # Exit with error code if issues found
    sys.exit(1 if report["total_issues"] > 0 else 0)


def format_summary(report: dict) -> str:
    """Format report as human-readable summary."""
    lines = [
        f"# MARP Layout Analysis: {report['file']}",
        "",
        f"**Total Issues:** {report['total_issues']}",
        f"- Auto-fixable: {report['auto_fixable_count']}",
        f"- Manual review: {report['manual_review_count']}",
        "",
        "## Issues by Category",
        "",
    ]

    for category, count in report["issues_by_category"].items():
        lines.append(f"- **{category}**: {count}")

    lines.extend(["", "## Issue Details", ""])

    for issue in report["issues"]:
        lines.append(f"### {issue['id']}: {issue['description']}")
        lines.append(f"- **Line:** {issue['line']}")
        lines.append(f"- **Severity:** {issue['severity']}")
        lines.append(f"- **Suggestion:** {issue['suggestion']}")
        lines.append(f"- **Auto-fixable:** {'Yes' if issue['auto_fixable'] else 'No'}")
        lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    main()
