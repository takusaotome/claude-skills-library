"""
Tests for analyze_marp_layout.py

Tests cover:
- Whitespace issue detection (WS001-WS004)
- Bullet formatting issues (BL001-BL004)
- Overflow risk detection (OF001-OF003)
- CSS issue detection (CS002, CS004)
"""

import pytest
from analyze_marp_layout import MarpLayoutAnalyzer


class TestWhitespaceIssues:
    """Tests for whitespace-related issue detection."""

    def test_ws001_double_blank_lines(self):
        """WS001: Detect multiple consecutive blank lines."""
        content = """---
marp: true
---

# Title


Content here
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        ws001_issues = [i for i in report["issues"] if i["id"] == "WS001"]
        assert len(ws001_issues) >= 1
        assert ws001_issues[0]["category"] == "whitespace"
        assert ws001_issues[0]["auto_fixable"] is True

    def test_ws002_trailing_whitespace(self):
        """WS002: Detect trailing whitespace on lines."""
        content = "# Title with trailing   \nContent here"
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        ws002_issues = [i for i in report["issues"] if i["id"] == "WS002"]
        assert len(ws002_issues) >= 1
        assert ws002_issues[0]["severity"] == "low"
        assert ws002_issues[0]["auto_fixable"] is True

    def test_ws003_tabs_detected(self):
        """WS003: Detect tab characters in content."""
        content = "# Title\n\t- Item with tab indent"
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        ws003_issues = [i for i in report["issues"] if i["id"] == "WS003"]
        assert len(ws003_issues) >= 1
        assert ws003_issues[0]["severity"] == "medium"

    def test_ws004_missing_blank_before_header(self):
        """WS004: Detect header without preceding blank line."""
        content = """---
marp: true
---
Content here
# Next Section
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        ws004_issues = [i for i in report["issues"] if i["id"] == "WS004"]
        assert len(ws004_issues) >= 1

    def test_no_ws004_after_slide_separator(self):
        """WS004: Should not flag header directly after slide separator."""
        content = """---
marp: true
---

# First Slide

---

# Second Slide
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        # After --- separator, header is valid without blank
        ws004_issues = [i for i in report["issues"] if i["id"] == "WS004"]
        # Only the first occurrence should be flagged (after frontmatter)
        assert len(ws004_issues) <= 1


class TestBulletIssues:
    """Tests for bullet/list formatting issue detection."""

    def test_bl001_mixed_markers(self):
        """BL001: Detect mixed list markers in same list."""
        content = """
- First item
* Second item
- Third item
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        bl001_issues = [i for i in report["issues"] if i["id"] == "BL001"]
        assert len(bl001_issues) >= 1
        assert bl001_issues[0]["auto_fixable"] is True

    def test_bl003_no_space_after_marker(self):
        """BL003: Detect missing space after list marker."""
        content = """
-No space here
-Another one
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        bl003_issues = [i for i in report["issues"] if i["id"] == "BL003"]
        assert len(bl003_issues) >= 2
        assert bl003_issues[0]["severity"] == "high"

    def test_bl002_four_space_indent(self):
        """BL002: Detect 4-space indentation in nested lists."""
        content = """
- Parent item
    - Nested with 4 spaces
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        bl002_issues = [i for i in report["issues"] if i["id"] == "BL002"]
        assert len(bl002_issues) >= 1

    def test_valid_list_no_issues(self):
        """Valid list should not trigger BL issues."""
        content = """
- First item
- Second item
  - Nested correctly
- Third item
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        bl_issues = [i for i in report["issues"] if i["id"].startswith("BL")]
        assert len(bl_issues) == 0


class TestOverflowIssues:
    """Tests for content overflow risk detection."""

    def test_of001_long_code_line(self):
        """OF001: Detect code lines exceeding 80 characters."""
        content = """
```python
def very_long_function_name_that_keeps_going_and_going_until_it_exceeds_eighty_characters():
    pass
```
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        of001_issues = [i for i in report["issues"] if i["id"] == "OF001"]
        assert len(of001_issues) >= 1
        assert of001_issues[0]["severity"] == "high"
        assert of001_issues[0]["auto_fixable"] is False

    def test_of002_unsized_image(self):
        """OF002: Detect images without size constraints."""
        content = """
![alt text](image.png)
![another image](photo.jpg)
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        of002_issues = [i for i in report["issues"] if i["id"] == "OF002"]
        assert len(of002_issues) >= 2
        assert of002_issues[0]["auto_fixable"] is True

    def test_sized_image_no_issue(self):
        """Sized image should not trigger OF002."""
        content = """
![w:800](image.png)
![h:400 alt](photo.jpg)
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        of002_issues = [i for i in report["issues"] if i["id"] == "OF002"]
        assert len(of002_issues) == 0

    def test_of003_wide_table(self):
        """OF003: Detect tables with many columns."""
        content = """
| Col1 | Col2 | Col3 | Col4 | Col5 | Col6 | Col7 |
|------|------|------|------|------|------|------|
| a    | b    | c    | d    | e    | f    | g    |
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        of003_issues = [i for i in report["issues"] if i["id"] == "OF003"]
        assert len(of003_issues) >= 1


class TestCSSIssues:
    """Tests for CSS-related issue detection."""

    def test_cs002_important_detected(self):
        """CS002: Detect !important usage."""
        content = """
<style>
h1 {
    color: blue !important;
}
</style>
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        cs002_issues = [i for i in report["issues"] if i["id"] == "CS002"]
        assert len(cs002_issues) >= 1
        assert cs002_issues[0]["severity"] == "medium"

    def test_cs004_zero_with_unit(self):
        """CS004: Detect zero values with unnecessary units."""
        content = """
<style>
.box {
    margin: 0px;
    padding: 0em;
}
</style>
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        cs004_issues = [i for i in report["issues"] if i["id"] == "CS004"]
        assert len(cs004_issues) >= 1
        assert cs004_issues[0]["auto_fixable"] is True


class TestReportStructure:
    """Tests for report output structure and metadata."""

    def test_report_schema_version(self):
        """Report should include schema version."""
        content = "# Simple slide"
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        assert report["schema_version"] == "1.0"

    def test_report_filename(self):
        """Report should include source filename."""
        content = "# Simple slide"
        analyzer = MarpLayoutAnalyzer(content, "my_slides.md")
        report = analyzer.analyze()

        assert report["file"] == "my_slides.md"

    def test_report_timestamp(self):
        """Report should include ISO timestamp."""
        content = "# Simple slide"
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        assert "timestamp" in report
        assert "T" in report["timestamp"]  # ISO format

    def test_report_issue_counts(self):
        """Report should correctly count issues."""
        content = """
-No space
* Mixed marker
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        assert report["total_issues"] == report["auto_fixable_count"] + report["manual_review_count"]

    def test_report_category_breakdown(self):
        """Report should categorize issues correctly."""
        content = """
# Title
-No space
trailing space
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        assert "issues_by_category" in report
        assert isinstance(report["issues_by_category"], dict)

    def test_css_analysis_present(self):
        """Report should include CSS analysis section."""
        content = """
<style>
h1 { color: blue; }
</style>
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        assert "css_analysis" in report
        assert "total_rules" in report["css_analysis"]


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_empty_content(self):
        """Empty content should not crash."""
        content = ""
        analyzer = MarpLayoutAnalyzer(content, "empty.md")
        report = analyzer.analyze()

        assert report["total_issues"] == 0

    def test_frontmatter_only(self):
        """File with only frontmatter should work."""
        content = """---
marp: true
theme: default
---
"""
        analyzer = MarpLayoutAnalyzer(content, "minimal.md")
        report = analyzer.analyze()

        # Should complete without error
        assert "total_issues" in report

    def test_code_block_boundary(self):
        """Code blocks should be properly tracked."""
        content = """
```python
# This is code
def foo():
    pass
```

Regular content here
```
More code
```
"""
        analyzer = MarpLayoutAnalyzer(content, "test.md")
        report = analyzer.analyze()

        # Should complete without error
        assert "total_issues" in report
