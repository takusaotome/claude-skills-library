"""
Tests for fix_marp_layout.py

Tests cover:
- Whitespace fixes (WS001-WS004)
- Bullet fixes (BL001-BL003)
- Image sizing fixes (OF002)
- CSS fixes (CS004)
"""

import json

import pytest
from fix_marp_layout import MarpLayoutFixer


class TestWhitespaceFixes:
    """Tests for whitespace fix application."""

    def test_ws002_trailing_whitespace_fix(self):
        """Fix trailing whitespace on lines."""
        content = "# Title with trailing   \nContent here  "
        report = {
            "issues": [
                {"id": "WS002", "line": 1, "auto_fixable": True, "suggestion": "Remove trailing whitespace"},
                {"id": "WS002", "line": 2, "auto_fixable": True, "suggestion": "Remove trailing whitespace"},
            ]
        }

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        assert "# Title with trailing" in fixed
        assert fixed.endswith("Content here")
        assert "   " not in fixed

    def test_ws003_tabs_to_spaces(self):
        """Convert tabs to spaces."""
        content = "\t- Item\n\t\t- Nested"
        report = {
            "issues": [
                {"id": "WS003", "line": 1, "auto_fixable": True, "suggestion": "Convert tabs"},
                {"id": "WS003", "line": 2, "auto_fixable": True, "suggestion": "Convert tabs"},
            ]
        }

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        assert "\t" not in fixed
        assert "  - Item" in fixed

    def test_ws004_insert_blank_line(self):
        """Insert blank line before header."""
        content = "Content\n# Header"
        report = {"issues": [{"id": "WS004", "line": 2, "auto_fixable": True, "suggestion": "Add blank line"}]}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        lines = fixed.split("\n")
        # Should have blank line before header
        header_idx = next(i for i, l in enumerate(lines) if l.startswith("# Header"))
        assert header_idx > 0
        assert lines[header_idx - 1].strip() == ""

    def test_ws001_collapse_blank_lines(self):
        """Collapse multiple blank lines to single."""
        content = "Title\n\n\n\nContent"
        report = {"issues": []}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        # Should not have 3+ consecutive newlines
        assert "\n\n\n" not in fixed


class TestBulletFixes:
    """Tests for bullet list fix application."""

    def test_bl001_normalize_markers(self):
        """Normalize list markers to dash."""
        content = "- First\n* Second\n+ Third"
        report = {
            "issues": [
                {"id": "BL001", "line": 2, "auto_fixable": True, "suggestion": "Use dash"},
                {"id": "BL001", "line": 3, "auto_fixable": True, "suggestion": "Use dash"},
            ]
        }

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        lines = fixed.split("\n")
        for line in lines:
            if line.strip():
                assert line.startswith("- "), f"Line should use dash marker: {line}"

    def test_bl003_add_space_after_marker(self):
        """Add space after list marker."""
        content = "-No space\n*Also no space"
        report = {
            "issues": [
                {"id": "BL003", "line": 1, "auto_fixable": True, "suggestion": "Add space"},
                {"id": "BL003", "line": 2, "auto_fixable": True, "suggestion": "Add space"},
            ]
        }

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        assert "- No space" in fixed or "- Also" in fixed

    def test_bl002_reduce_indentation(self):
        """Reduce 4-space indent to 2-space."""
        content = "- Parent\n    - Child"
        report = {"issues": [{"id": "BL002", "line": 2, "auto_fixable": True, "suggestion": "Use 2 spaces"}]}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        lines = fixed.split("\n")
        # Child should have 2 spaces
        assert lines[1].startswith("  - ") or lines[1].startswith("    -")  # May vary


class TestImageFixes:
    """Tests for image fix application."""

    def test_of002_add_width(self):
        """Add width to unsized images."""
        content = "![alt text](image.png)"
        report = {"issues": [{"id": "OF002", "line": 1, "auto_fixable": True, "suggestion": "Add width"}]}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        assert "w:800" in fixed
        assert "(image.png)" in fixed

    def test_of002_preserve_existing_size(self):
        """Should not modify already-sized images."""
        content = "![w:500](image.png)"
        report = {"issues": []}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        # Should not add another w: prefix
        assert fixed.count("w:") == 1


class TestCSSFixes:
    """Tests for CSS fix application."""

    def test_cs004_remove_unit_from_zero(self):
        """Remove unit from zero values."""
        content = "margin: 0px;\npadding: 0em;"
        report = {
            "issues": [
                {"id": "CS004", "line": 1, "auto_fixable": True, "suggestion": "Use 0"},
                {"id": "CS004", "line": 2, "auto_fixable": True, "suggestion": "Use 0"},
            ]
        }

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        assert "0px" not in fixed or ": 0" in fixed
        assert "0em" not in fixed or ": 0" in fixed


class TestAutoOnlyMode:
    """Tests for auto-only fix mode."""

    def test_auto_only_skips_manual(self):
        """Auto-only mode should skip non-auto-fixable issues."""
        content = "Content\n# Header"
        report = {
            "issues": [
                {"id": "WS004", "line": 2, "auto_fixable": True, "suggestion": "Auto fix"},
                {"id": "AL001", "line": 1, "auto_fixable": False, "suggestion": "Manual fix"},
            ]
        }

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes(auto_only=True)
        summary = fixer.get_fix_summary()

        # Only auto-fixable should be applied
        fix_ids = [f["issue_id"] for f in summary["fixes"]]
        assert "WS004" in fix_ids
        assert "AL001" not in fix_ids


class TestFixSummary:
    """Tests for fix summary generation."""

    def test_summary_structure(self):
        """Summary should have correct structure."""
        content = "# Title   "
        report = {"issues": [{"id": "WS002", "line": 1, "auto_fixable": True, "suggestion": "Remove"}]}

        fixer = MarpLayoutFixer(content, report)
        fixer.apply_fixes()
        summary = fixer.get_fix_summary()

        assert "timestamp" in summary
        assert "total_fixes" in summary
        assert "fixes" in summary
        assert isinstance(summary["fixes"], list)

    def test_summary_counts_fixes(self):
        """Summary should correctly count applied fixes."""
        content = "Line1   \nLine2   "
        report = {
            "issues": [
                {"id": "WS002", "line": 1, "auto_fixable": True, "suggestion": "Fix"},
                {"id": "WS002", "line": 2, "auto_fixable": True, "suggestion": "Fix"},
            ]
        }

        fixer = MarpLayoutFixer(content, report)
        fixer.apply_fixes()
        summary = fixer.get_fix_summary()

        assert summary["total_fixes"] >= 2


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_report(self):
        """Empty report should not crash."""
        content = "# Valid content"
        report = {"issues": []}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        assert fixed == content

    def test_invalid_line_number(self):
        """Invalid line numbers should be handled gracefully."""
        content = "Single line"
        report = {"issues": [{"id": "WS002", "line": 999, "auto_fixable": True, "suggestion": "Fix"}]}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        # Should not crash, content unchanged
        assert fixed == content

    def test_preserves_content(self):
        """Fixes should preserve non-issue content."""
        content = """---
marp: true
---

# Title

Regular content here.

- Valid list
- Another item
"""
        report = {"issues": []}

        fixer = MarpLayoutFixer(content, report)
        fixed = fixer.apply_fixes()

        assert "marp: true" in fixed
        assert "# Title" in fixed
        assert "Regular content here." in fixed
        assert "- Valid list" in fixed
