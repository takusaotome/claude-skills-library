"""Tests for gap_analysis.py module."""

import csv
import json
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from gap_analysis import (
    HLS_CLAUSES,
    ClauseAssessment,
    GapAnalysisReport,
    ISOStandard,
    _score_label,
    generate_blank_template,
    generate_markdown_report,
    load_assessments_from_csv,
)


class TestClauseAssessment:
    """Tests for ClauseAssessment dataclass."""

    def test_create_assessment(self):
        """Test creating a clause assessment."""
        assessment = ClauseAssessment(
            clause_id="4.1",
            clause_title="Understanding the organization and its context",
            score=3,
            current_state="Partially documented",
            gap_description="No formal process",
            evidence_reviewed="Management meeting minutes",
            recommended_actions="Create context analysis procedure",
            priority="High",
            effort_weeks=2,
        )
        assert assessment.clause_id == "4.1"
        assert assessment.score == 3
        assert assessment.priority == "High"

    def test_to_dict(self):
        """Test converting assessment to dictionary."""
        assessment = ClauseAssessment(
            clause_id="5.1",
            clause_title="Leadership and commitment",
            score=4,
            current_state="Documented",
            gap_description="Minor gaps",
            evidence_reviewed="Policy document",
            recommended_actions="Update policy",
            priority="Medium",
            effort_weeks=1,
        )
        d = assessment.to_dict()
        assert d["clause_id"] == "5.1"
        assert d["score"] == 4
        assert isinstance(d, dict)


class TestGapAnalysisReport:
    """Tests for GapAnalysisReport dataclass."""

    @pytest.fixture
    def sample_assessments(self):
        """Create sample assessments for testing."""
        return [
            ClauseAssessment("4.1", "Context", 5, "", "", "", "", "Low", 0),
            ClauseAssessment("4.2", "Interested parties", 4, "", "", "", "", "Low", 1),
            ClauseAssessment("5.1", "Leadership", 3, "", "Gap", "", "Action", "High", 3),
            ClauseAssessment("6.1", "Risks", 2, "", "Major gap", "", "Action", "High", 4),
            ClauseAssessment("7.1", "Resources", 1, "", "Not compliant", "", "Action", "High", 6),
        ]

    def test_overall_maturity(self, sample_assessments):
        """Test maturity score calculation."""
        report = GapAnalysisReport(
            organization="Test Org",
            standard="ISO 9001:2015",
            assessor="Tester",
            assessment_date="2024-01-01",
            scope="Full",
            assessments=sample_assessments,
        )
        # (5+4+3+2+1) / 5 = 3.0
        assert report.overall_maturity == 3.0

    def test_overall_maturity_excludes_zero_scores(self):
        """Test that N/A (score=0) is excluded from maturity calculation."""
        assessments = [
            ClauseAssessment("4.1", "Context", 4, "", "", "", "", "Low", 0),
            ClauseAssessment("4.2", "Parties", 0, "", "", "", "", "Low", 0),  # N/A
            ClauseAssessment("5.1", "Leadership", 4, "", "", "", "", "Low", 0),
        ]
        report = GapAnalysisReport(
            organization="Test",
            standard="ISO 9001:2015",
            assessor="Tester",
            assessment_date="2024-01-01",
            scope="Full",
            assessments=assessments,
        )
        # Only applicable: (4+4) / 2 = 4.0
        assert report.overall_maturity == 4.0

    def test_compliance_summary(self, sample_assessments):
        """Test compliance summary counts."""
        report = GapAnalysisReport(
            organization="Test",
            standard="ISO 9001:2015",
            assessor="Tester",
            assessment_date="2024-01-01",
            scope="Full",
            assessments=sample_assessments,
        )
        summary = report.compliance_summary
        assert summary["fully_compliant"] == 1  # score 5
        assert summary["mostly_compliant"] == 1  # score 4
        assert summary["partially_compliant"] == 1  # score 3
        assert summary["minimally_compliant"] == 1  # score 2
        assert summary["not_compliant"] == 1  # score 1

    def test_high_priority_gaps(self, sample_assessments):
        """Test high priority gap filtering."""
        report = GapAnalysisReport(
            organization="Test",
            standard="ISO 9001:2015",
            assessor="Tester",
            assessment_date="2024-01-01",
            scope="Full",
            assessments=sample_assessments,
        )
        high_priority = report.high_priority_gaps
        # High priority with score < 4: 5.1 (3), 6.1 (2), 7.1 (1)
        assert len(high_priority) == 3

    def test_estimated_timeline(self):
        """Test timeline estimation based on maturity."""
        # High maturity = shorter timeline
        high_assessments = [
            ClauseAssessment("4.1", "Test", 5, "", "", "", "", "Low", 0),
            ClauseAssessment("5.1", "Test", 4, "", "", "", "", "Low", 0),
        ]
        report_high = GapAnalysisReport(
            organization="Test",
            standard="ISO 9001:2015",
            assessor="Tester",
            assessment_date="2024-01-01",
            scope="Full",
            assessments=high_assessments,
        )
        assert report_high.estimated_timeline_months == 6

        # Low maturity = longer timeline
        low_assessments = [
            ClauseAssessment("4.1", "Test", 1, "", "", "", "", "High", 0),
            ClauseAssessment("5.1", "Test", 1, "", "", "", "", "High", 0),
        ]
        report_low = GapAnalysisReport(
            organization="Test",
            standard="ISO 9001:2015",
            assessor="Tester",
            assessment_date="2024-01-01",
            scope="Full",
            assessments=low_assessments,
        )
        assert report_low.estimated_timeline_months == 18


class TestTemplateGeneration:
    """Tests for template generation."""

    def test_generate_blank_template(self):
        """Test blank CSV template generation."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            output_path = Path(f.name)

        try:
            generate_blank_template("ISO 9001:2015", output_path)
            assert output_path.exists()

            # Verify CSV structure
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            # Should have all HLS subclauses
            expected_count = sum(len(info["subclauses"]) for info in HLS_CLAUSES.values())
            assert len(rows) == expected_count

            # Verify headers
            assert "clause_id" in rows[0]
            assert "score" in rows[0]
            assert "priority" in rows[0]
        finally:
            output_path.unlink(missing_ok=True)


class TestCSVLoading:
    """Tests for CSV loading."""

    def test_load_assessments_from_csv(self):
        """Test loading assessments from CSV file."""
        csv_content = """clause_id,clause_title,score,current_state,gap_description,evidence_reviewed,recommended_actions,priority,effort_weeks
4.1,Understanding context,4,Documented,Minor gaps,Policy doc,Review,Medium,2
5.1,Leadership,3,Partial,Significant gap,Minutes,Implement,High,4
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            csv_path = Path(f.name)

        try:
            assessments = load_assessments_from_csv(csv_path)
            assert len(assessments) == 2
            assert assessments[0].clause_id == "4.1"
            assert assessments[0].score == 4
            assert assessments[1].priority == "High"
        finally:
            csv_path.unlink(missing_ok=True)

    def test_load_skips_empty_scores(self):
        """Test that rows without scores are skipped."""
        csv_content = """clause_id,clause_title,score,current_state,gap_description,evidence_reviewed,recommended_actions,priority,effort_weeks
4.1,Understanding context,4,Documented,,,,,2
5.1,Leadership,,Partial,,,,,
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(csv_content)
            csv_path = Path(f.name)

        try:
            assessments = load_assessments_from_csv(csv_path)
            assert len(assessments) == 1  # Only row with score
        finally:
            csv_path.unlink(missing_ok=True)


class TestMarkdownReport:
    """Tests for markdown report generation."""

    def test_generate_markdown_report(self):
        """Test markdown report generation."""
        assessments = [
            ClauseAssessment(
                "4.1", "Understanding context", 3, "Partial", "Gap exists", "Minutes", "Create procedure", "High", 2
            ),
        ]
        report = GapAnalysisReport(
            organization="ACME Corp",
            standard="ISO 27001:2022",
            assessor="John Smith",
            assessment_date="2024-01-15",
            scope="IT Department",
            assessments=assessments,
        )
        md = generate_markdown_report(report)

        assert "# ISO 27001:2022 Gap Analysis Report" in md
        assert "ACME Corp" in md
        assert "John Smith" in md
        assert "IT Department" in md
        assert "4.1" in md
        assert "Understanding context" in md

    def test_report_contains_maturity_score(self):
        """Test that report includes maturity score."""
        assessments = [
            ClauseAssessment("4.1", "Test", 4, "", "", "", "", "Low", 0),
            ClauseAssessment("5.1", "Test", 4, "", "", "", "", "Low", 0),
        ]
        report = GapAnalysisReport(
            organization="Test",
            standard="ISO 9001:2015",
            assessor="Tester",
            assessment_date="2024-01-01",
            scope="Full",
            assessments=assessments,
        )
        md = generate_markdown_report(report)
        assert "4.00/5.0" in md


class TestScoreLabel:
    """Tests for score label function."""

    def test_all_score_labels(self):
        """Test all score label mappings."""
        assert _score_label(5) == "Fully Compliant"
        assert _score_label(4) == "Mostly Compliant"
        assert _score_label(3) == "Partially Compliant"
        assert _score_label(2) == "Minimally Compliant"
        assert _score_label(1) == "Not Compliant"
        assert _score_label(0) == "Not Applicable"
        assert _score_label(-1) == "Unknown"


class TestISOStandard:
    """Tests for ISOStandard enum."""

    def test_standard_values(self):
        """Test ISO standard enum values."""
        assert ISOStandard.ISO_9001.value == "ISO 9001:2015"
        assert ISOStandard.ISO_27001.value == "ISO 27001:2022"
        assert ISOStandard.ISO_22301.value == "ISO 22301:2019"
        assert ISOStandard.ISO_45001.value == "ISO 45001:2018"
        assert ISOStandard.ISO_14001.value == "ISO 14001:2015"


class TestHLSClauses:
    """Tests for HLS clause structure."""

    def test_hls_has_all_main_clauses(self):
        """Test that HLS contains clauses 4-10."""
        expected_clauses = ["4", "5", "6", "7", "8", "9", "10"]
        for clause in expected_clauses:
            assert clause in HLS_CLAUSES

    def test_each_clause_has_subclauses(self):
        """Test that each main clause has subclauses."""
        for clause_num, clause_info in HLS_CLAUSES.items():
            assert "title" in clause_info
            assert "subclauses" in clause_info
            assert len(clause_info["subclauses"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
