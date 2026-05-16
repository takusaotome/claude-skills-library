"""Tests for patent_search_helper.py."""

import sys
from pathlib import Path

import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from patent_search_helper import (
    SearchConfig,
    build_boolean_query,
    expand_keywords,
    generate_google_patents_url,
    generate_report,
    parse_cpc_codes,
    parse_keywords,
)


class TestParseKeywords:
    """Tests for parse_keywords function."""

    def test_parse_single_keyword(self) -> None:
        """Parse single keyword."""
        result = parse_keywords("neural network")
        assert result == ["neural network"]

    def test_parse_multiple_keywords(self) -> None:
        """Parse comma-separated keywords."""
        result = parse_keywords("neural network, image segmentation, CNN")
        assert result == ["neural network", "image segmentation", "CNN"]

    def test_parse_empty_string(self) -> None:
        """Return empty list for empty string."""
        result = parse_keywords("")
        assert result == []

    def test_parse_with_extra_whitespace(self) -> None:
        """Handle extra whitespace."""
        result = parse_keywords("  keyword1  ,  keyword2  ")
        assert result == ["keyword1", "keyword2"]

    def test_parse_with_empty_segments(self) -> None:
        """Skip empty segments."""
        result = parse_keywords("keyword1,,keyword2,")
        assert result == ["keyword1", "keyword2"]


class TestParseCpcCodes:
    """Tests for parse_cpc_codes function."""

    def test_parse_valid_cpc_code(self) -> None:
        """Parse valid CPC code."""
        result = parse_cpc_codes("G06N3/08")
        assert result == ["G06N3/08"]

    def test_parse_multiple_cpc_codes(self) -> None:
        """Parse multiple CPC codes."""
        result = parse_cpc_codes("G06N3/08,G06V10/82")
        assert result == ["G06N3/08", "G06V10/82"]

    def test_parse_lowercase_cpc_code(self) -> None:
        """Uppercase lowercase codes."""
        result = parse_cpc_codes("g06n3/08")
        assert result == ["G06N3/08"]

    def test_parse_invalid_cpc_code(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Warn on invalid CPC code format."""
        result = parse_cpc_codes("INVALID")
        assert result == []
        captured = capsys.readouterr()
        assert "Warning" in captured.err

    def test_parse_empty_string(self) -> None:
        """Return empty list for empty string."""
        result = parse_cpc_codes("")
        assert result == []

    def test_parse_mixed_valid_invalid(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Include valid codes, warn on invalid."""
        result = parse_cpc_codes("G06N3/08,INVALID,H01M4/00")
        assert result == ["G06N3/08", "H01M4/00"]
        captured = capsys.readouterr()
        assert "Warning" in captured.err


class TestExpandKeywords:
    """Tests for expand_keywords function."""

    def test_expand_known_keyword(self) -> None:
        """Expand keyword with known expansions."""
        result = expand_keywords(["neural network"])
        assert "neural network" in result
        assert "neural network" in result["neural network"]
        assert "deep learning" in result["neural network"]

    def test_expand_unknown_keyword(self) -> None:
        """Return original for unknown keyword."""
        result = expand_keywords(["unknown_term"])
        assert result == {"unknown_term": ["unknown_term"]}

    def test_expand_case_insensitive(self) -> None:
        """Handle case variations."""
        result = expand_keywords(["Neural Network"])
        assert "Neural Network" in result

    def test_expand_multiple_keywords(self) -> None:
        """Expand multiple keywords."""
        result = expand_keywords(["cnn", "real-time"])
        assert "cnn" in result
        assert "real-time" in result


class TestBuildBooleanQuery:
    """Tests for build_boolean_query function."""

    def test_query_with_keywords_only(self) -> None:
        """Build query with keywords only."""
        config = SearchConfig(keywords=["neural network"])
        result = build_boolean_query(config)
        assert "neural network" in result.lower()
        assert "OR" in result

    def test_query_with_cpc_codes(self) -> None:
        """Build query with CPC codes."""
        config = SearchConfig(cpc_codes=["G06N3/08"])
        result = build_boolean_query(config)
        assert "CPC/G06N3/08" in result

    def test_query_with_keywords_and_cpc(self) -> None:
        """Build query with both keywords and CPC."""
        config = SearchConfig(keywords=["image"], cpc_codes=["G06N3/08"])
        result = build_boolean_query(config)
        assert "AND" in result
        assert "CPC/G06N3/08" in result

    def test_query_empty_config(self) -> None:
        """Handle empty configuration."""
        config = SearchConfig()
        result = build_boolean_query(config)
        assert "no query specified" in result


class TestGenerateGooglePatentsUrl:
    """Tests for generate_google_patents_url function."""

    def test_url_with_keywords(self) -> None:
        """Generate URL with keywords."""
        config = SearchConfig(keywords=["neural network"])
        result = generate_google_patents_url(config)
        assert "patents.google.com" in result
        assert "neural+network" in result or "q=" in result

    def test_url_includes_type_filter(self) -> None:
        """URL includes patent type filter."""
        config = SearchConfig(keywords=["test"])
        result = generate_google_patents_url(config)
        assert "type=PATENT" in result


class TestGenerateReport:
    """Tests for generate_report function."""

    def test_report_contains_required_sections(self) -> None:
        """Report includes all required sections."""
        config = SearchConfig(keywords=["neural network"], cpc_codes=["G06N3/08"])
        report = generate_report(config)

        required_sections = [
            "# Prior Art Search Report",
            "## Report Information",
            "## Search Configuration",
            "## Search Queries",
            "## Key References",
            "## Feature Comparison Matrix",
            "## Preliminary Assessment",
            "## Recommendations",
        ]

        for section in required_sections:
            assert section in report, f"Missing section: {section}"

    def test_report_includes_keywords(self) -> None:
        """Report includes provided keywords."""
        config = SearchConfig(keywords=["unique_keyword_123"])
        report = generate_report(config)
        assert "unique_keyword_123" in report

    def test_report_includes_cpc_codes(self) -> None:
        """Report includes CPC codes."""
        config = SearchConfig(cpc_codes=["G06N3/08"])
        report = generate_report(config)
        assert "G06N3/08" in report

    def test_report_includes_google_url(self) -> None:
        """Report includes Google Patents URL."""
        config = SearchConfig(keywords=["test"])
        report = generate_report(config)
        assert "patents.google.com" in report

    def test_report_saves_to_file(self, tmp_path: Path) -> None:
        """Report saves to file when path provided."""
        config = SearchConfig(keywords=["test"])
        output_path = tmp_path / "report.md"

        generate_report(config, output_path)

        assert output_path.exists()
        content = output_path.read_text()
        assert "# Prior Art Search Report" in content


class TestSearchConfig:
    """Tests for SearchConfig dataclass."""

    def test_default_values(self) -> None:
        """SearchConfig has expected defaults."""
        config = SearchConfig()
        assert config.keywords == []
        assert config.cpc_codes == []
        assert "US" in config.jurisdictions
        assert config.date_range is None

    def test_custom_values(self) -> None:
        """SearchConfig accepts custom values."""
        config = SearchConfig(
            keywords=["test"],
            cpc_codes=["G06N3/08"],
            jurisdictions=["US", "JP"],
        )
        assert config.keywords == ["test"]
        assert config.cpc_codes == ["G06N3/08"]
        assert config.jurisdictions == ["US", "JP"]
