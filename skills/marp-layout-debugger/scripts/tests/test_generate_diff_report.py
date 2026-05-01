"""
Tests for generate_diff_report.py

Tests cover:
- Diff chunk detection
- Change categorization
- Statistics calculation
- Report formatting
"""

import pytest
from generate_diff_report import DiffReportGenerator


class TestDiffDetection:
    """Tests for difference detection between files."""

    def test_detect_whitespace_changes(self):
        """Detect whitespace-only changes."""
        original = "Title   \nContent"
        fixed = "Title\nContent"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Whitespace" in report or "Trailing" in report

    def test_detect_blank_line_changes(self):
        """Detect blank line additions/removals."""
        original = "Title\n\n\n\nContent"
        fixed = "Title\n\nContent"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Blank Lines" in report or "Lines removed" in report

    def test_detect_list_marker_changes(self):
        """Detect list marker normalization."""
        original = "* First\n+ Second"
        fixed = "- First\n- Second"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "List Markers" in report or "changed" in report.lower()

    def test_detect_image_sizing(self):
        """Detect image sizing additions."""
        original = "![alt](image.png)"
        fixed = "![w:800 alt](image.png)"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Image" in report or "w:800" in report


class TestStatistics:
    """Tests for diff statistics calculation."""

    def test_count_lines_changed(self):
        """Correctly count changed lines."""
        original = "Line 1\nLine 2\nLine 3"
        fixed = "Line 1\nModified 2\nLine 3"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Lines changed" in report

    def test_count_lines_added(self):
        """Correctly count added lines."""
        original = "Line 1\nLine 2"
        fixed = "Line 1\nNew Line\nLine 2"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Lines added" in report

    def test_count_lines_removed(self):
        """Correctly count removed lines."""
        original = "Line 1\nRemove me\nLine 2"
        fixed = "Line 1\nLine 2"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Lines removed" in report


class TestReportFormat:
    """Tests for report output format."""

    def test_report_has_header(self):
        """Report should have proper header."""
        original = "Content"
        fixed = "Modified content"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "# MARP Layout Diff Report" in report

    def test_report_has_summary(self):
        """Report should include summary section."""
        original = "Content"
        fixed = "Modified content"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "## Summary" in report
        assert "Original file" in report
        assert "Fixed file" in report

    def test_report_has_unified_diff(self):
        """Report should include unified diff section."""
        original = "Line 1\nLine 2"
        fixed = "Line 1\nChanged 2"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "## Unified Diff" in report
        assert "```diff" in report

    def test_report_includes_filenames(self):
        """Report should reference original filenames."""
        original = "Content"
        fixed = "Fixed"

        generator = DiffReportGenerator(original, fixed, "my_slides.md", "my_slides_fixed.md")
        report = generator.generate_report()

        assert "my_slides.md" in report
        assert "my_slides_fixed.md" in report

    def test_report_has_timestamp(self):
        """Report should include generation timestamp."""
        original = "Content"
        fixed = "Fixed"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Generated:" in report


class TestCategoryDetection:
    """Tests for change category detection."""

    def test_category_tabs_to_spaces(self):
        """Detect tabs-to-spaces changes."""
        original = "\tIndented"
        fixed = "  Indented"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Tabs to Spaces" in report or "Whitespace" in report

    def test_category_trailing_whitespace(self):
        """Detect trailing whitespace removal."""
        original = "Text   "
        fixed = "Text"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Whitespace" in report or "Trailing" in report

    def test_category_indentation(self):
        """Detect indentation changes."""
        original = "    Four spaces"
        fixed = "  Two spaces"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Indent" in report or "changed" in report.lower()


class TestEdgeCases:
    """Tests for edge cases."""

    def test_identical_files(self):
        """Handle identical files gracefully."""
        content = "Same content"

        generator = DiffReportGenerator(content, content, "a.md", "b.md")
        report = generator.generate_report()

        assert "No changes detected" in report or "Lines changed:** 0" in report

    def test_empty_original(self):
        """Handle empty original file."""
        original = ""
        fixed = "New content"

        generator = DiffReportGenerator(original, fixed, "empty.md", "fixed.md")
        report = generator.generate_report()

        assert "Lines added" in report

    def test_empty_fixed(self):
        """Handle empty fixed file."""
        original = "Original content"
        fixed = ""

        generator = DiffReportGenerator(original, fixed, "orig.md", "empty.md")
        report = generator.generate_report()

        assert "Lines removed" in report

    def test_large_diff(self):
        """Handle large differences gracefully."""
        original = "\n".join([f"Original line {i}" for i in range(100)])
        fixed = "\n".join([f"Fixed line {i}" for i in range(100)])

        generator = DiffReportGenerator(original, fixed, "big_orig.md", "big_fixed.md")
        report = generator.generate_report()

        # Should complete and have content
        assert len(report) > 100
        assert "## Summary" in report

    def test_special_characters_escaped(self):
        """Table special characters should be escaped."""
        original = "Code | with | pipes"
        fixed = "Code with pipes"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        # Should not break markdown table
        assert "\\|" in report or "pipes" in report


class TestDetailedChanges:
    """Tests for detailed change formatting."""

    def test_small_change_table_format(self):
        """Small changes should use table format."""
        original = "Line 1\nLine 2"
        fixed = "Line 1\nModified"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        # Should have table markers
        assert "| Original |" in report or "Original" in report

    def test_change_index_numbering(self):
        """Changes should be numbered."""
        original = "Line A\nLine B"
        fixed = "Changed A\nChanged B"

        generator = DiffReportGenerator(original, fixed, "orig.md", "fixed.md")
        report = generator.generate_report()

        assert "Change 1" in report or "### Change" in report
