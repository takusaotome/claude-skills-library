"""
Tests for review_minutes.py - Meeting Minutes Reviewer
"""

import json
from pathlib import Path

import pytest
from review_minutes import Finding, MinutesReviewer, ReviewResult, format_markdown

# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def good_minutes(tmp_path) -> Path:
    """Create a well-formatted meeting minutes file."""
    content = """# Project Kickoff Meeting

**Date**: 2025-01-15
**Time**: 10:00 AM - 11:00 AM
**Location**: Conference Room A / Zoom

## Attendees

| Name | Role |
|------|------|
| John Smith | Project Manager |
| Sarah Chen | Tech Lead |
| Mike Johnson | Developer |

## Agenda

1. Project overview
2. Timeline discussion
3. Resource allocation
4. Risk assessment

## Discussion Summary

### Project Overview
John presented the project scope. Key deliverables include:
- New API endpoints
- Frontend redesign
- Performance improvements

### Timeline Discussion
Sarah proposed a 3-month timeline. The team agreed this was feasible.

## Decisions

### Decision 1: Use PostgreSQL for Database

**Context**: Need to select database for new microservice.

**Alternatives Considered**:
1. PostgreSQL - Strong JSON support
2. MySQL - Lower cost

**Rationale**: PostgreSQL chosen for JSON support and team expertise.

**Decided**: We will proceed with PostgreSQL.

## Action Items

- [ ] @John Smith: Create project charter document
      Due: 2025-01-20
      Context: Discussion item #1

- [ ] @Sarah Chen: Draft technical architecture document
      Due: 2025-01-22
      Context: Decision #1

- [ ] @Mike Johnson: Set up development environment with PostgreSQL
      Due: 2025-01-18
      Context: Decision #1

## Next Steps

- Follow-up meeting scheduled for 2025-01-22
- Architecture review milestone: 2025-01-25
"""
    minutes_file = tmp_path / "good_minutes.md"
    minutes_file.write_text(content)
    return minutes_file


@pytest.fixture
def poor_minutes(tmp_path) -> Path:
    """Create a poorly-formatted meeting minutes file with issues."""
    content = """# Meeting Notes

We had a meeting today.

## What We Discussed

- The project
- Some issues
- They will look into it soon

## Actions

- John to do something
- Fix the issue later
- Improve performance ASAP

## Decisions

We agreed to do some stuff.
"""
    minutes_file = tmp_path / "poor_minutes.md"
    minutes_file.write_text(content)
    return minutes_file


@pytest.fixture
def hearing_sheet(tmp_path) -> Path:
    """Create a hearing sheet for consistency testing."""
    content = """# Meeting Agenda

1. Project Overview
2. Timeline Discussion
3. Resource Allocation
4. Risk Assessment
5. Budget Review (Not discussed)
"""
    sheet_file = tmp_path / "hearing_sheet.md"
    sheet_file.write_text(content)
    return sheet_file


# ============================================================================
# Test Completeness Checking
# ============================================================================


class TestCompletenessCheck:
    """Tests for completeness dimension scoring."""

    def test_good_minutes_completeness_high_score(self, good_minutes):
        """Well-formatted minutes should score high on completeness."""
        reviewer = MinutesReviewer(good_minutes)
        reviewer.load_documents()
        score = reviewer.check_completeness()

        assert score >= 80, f"Expected score >= 80, got {score}"

    def test_poor_minutes_completeness_low_score(self, poor_minutes):
        """Poorly-formatted minutes should score low on completeness."""
        reviewer = MinutesReviewer(poor_minutes)
        reviewer.load_documents()
        score = reviewer.check_completeness()

        assert score < 70, f"Expected score < 70, got {score}"

    def test_missing_sections_generate_findings(self, poor_minutes):
        """Missing sections should generate findings."""
        reviewer = MinutesReviewer(poor_minutes)
        reviewer.load_documents()
        reviewer.check_completeness()

        completeness_findings = [f for f in reviewer.findings if f.dimension == "completeness"]
        assert len(completeness_findings) > 0, "Expected findings for missing sections"

    def test_detects_missing_date(self, tmp_path):
        """Should detect missing meeting date."""
        content = """# Meeting Notes

## Attendees
- John Smith

## Discussion
We talked about the project.
"""
        minutes_file = tmp_path / "no_date.md"
        minutes_file.write_text(content)

        reviewer = MinutesReviewer(minutes_file)
        reviewer.load_documents()
        reviewer.check_completeness()

        date_findings = [f for f in reviewer.findings if "date" in f.issue.lower()]
        assert len(date_findings) > 0, "Should detect missing date"


# ============================================================================
# Test Action Items Checking
# ============================================================================


class TestActionItemsCheck:
    """Tests for action items dimension scoring."""

    def test_good_action_items_high_score(self, good_minutes):
        """Well-formatted action items should score high."""
        reviewer = MinutesReviewer(good_minutes)
        reviewer.load_documents()
        score = reviewer.check_action_items()

        assert score >= 80, f"Expected score >= 80, got {score}"

    def test_detects_missing_owner(self, tmp_path):
        """Should detect action items missing owner."""
        content = """# Meeting

## Action Items

- Complete the documentation by 2025-01-20
- Review the code changes
"""
        minutes_file = tmp_path / "no_owner.md"
        minutes_file.write_text(content)

        reviewer = MinutesReviewer(minutes_file)
        reviewer.load_documents()
        reviewer.check_action_items()

        owner_findings = [f for f in reviewer.findings if "owner" in f.issue.lower()]
        assert len(owner_findings) > 0, "Should detect missing owner"

    def test_detects_missing_deadline(self, tmp_path):
        """Should detect action items missing deadline."""
        content = """# Meeting

## Action Items

- [ ] @John Smith: Complete the documentation
- [ ] @Sarah Chen: Review the architecture
"""
        minutes_file = tmp_path / "no_deadline.md"
        minutes_file.write_text(content)

        reviewer = MinutesReviewer(minutes_file)
        reviewer.load_documents()
        reviewer.check_action_items()

        deadline_findings = [f for f in reviewer.findings if "deadline" in f.issue.lower()]
        assert len(deadline_findings) >= 2, "Should detect missing deadlines"

    def test_no_action_items_critical_finding(self, tmp_path):
        """Missing action items section should generate critical finding."""
        content = """# Meeting

## Discussion
We talked about things.

## Decisions
We decided something.
"""
        minutes_file = tmp_path / "no_actions.md"
        minutes_file.write_text(content)

        reviewer = MinutesReviewer(minutes_file)
        reviewer.load_documents()
        score = reviewer.check_action_items()

        assert score == 0, "Score should be 0 with no action items"
        critical_findings = [f for f in reviewer.findings if f.severity == "critical" and f.dimension == "action_items"]
        assert len(critical_findings) > 0, "Should have critical finding for missing actions"


# ============================================================================
# Test Decisions Checking
# ============================================================================


class TestDecisionsCheck:
    """Tests for decisions dimension scoring."""

    def test_good_decisions_high_score(self, good_minutes):
        """Well-documented decisions should score high."""
        reviewer = MinutesReviewer(good_minutes)
        reviewer.load_documents()
        score = reviewer.check_decisions()

        assert score >= 70, f"Expected score >= 70, got {score}"

    def test_detects_implicit_decisions(self, tmp_path):
        """Should detect decisions without proper documentation."""
        content = """# Meeting

## Discussion
We talked about the database choice.

## Decisions
Use PostgreSQL.
"""
        minutes_file = tmp_path / "implicit_decision.md"
        minutes_file.write_text(content)

        reviewer = MinutesReviewer(minutes_file)
        reviewer.load_documents()
        reviewer.check_decisions()

        # Should find issues with context or rationale
        decision_findings = [f for f in reviewer.findings if f.dimension == "decisions"]
        assert len(decision_findings) > 0, "Should detect poorly documented decision"

    def test_no_decisions_critical_finding(self, tmp_path):
        """Missing decisions section should generate critical finding."""
        content = """# Meeting

## Discussion
We talked about things but made no decisions.

## Action Items
- [ ] @John: Do something by 2025-01-20
"""
        minutes_file = tmp_path / "no_decisions.md"
        minutes_file.write_text(content)

        reviewer = MinutesReviewer(minutes_file)
        reviewer.load_documents()
        score = reviewer.check_decisions()

        assert score == 0, "Score should be 0 with no decisions"


# ============================================================================
# Test Clarity Checking
# ============================================================================


class TestClarityCheck:
    """Tests for clarity dimension scoring."""

    def test_clear_language_high_score(self, good_minutes):
        """Clear language should score high."""
        reviewer = MinutesReviewer(good_minutes)
        reviewer.load_documents()
        score = reviewer.check_clarity()

        assert score >= 80, f"Expected score >= 80, got {score}"

    def test_detects_vague_language(self, tmp_path):
        """Should detect vague language patterns."""
        content = """# Meeting

## Discussion
The team will look into the issue soon. They should improve performance later.
We agreed to follow up ASAP.

## Action Items
- John to do something
"""
        minutes_file = tmp_path / "vague_language.md"
        minutes_file.write_text(content)

        reviewer = MinutesReviewer(minutes_file)
        reviewer.load_documents()
        score = reviewer.check_clarity()

        assert score < 80, f"Expected score < 80 with vague language, got {score}"

        vague_findings = [f for f in reviewer.findings if "vague" in f.issue.lower()]
        assert len(vague_findings) > 0, "Should detect vague language"


# ============================================================================
# Test Consistency Checking
# ============================================================================


class TestConsistencyCheck:
    """Tests for consistency dimension scoring."""

    def test_consistency_without_source(self, good_minutes):
        """Without source material, should give neutral score."""
        reviewer = MinutesReviewer(good_minutes)
        reviewer.load_documents()
        score = reviewer.check_consistency()

        assert score == 80, f"Expected neutral score of 80, got {score}"

    def test_consistency_with_matching_source(self, good_minutes, hearing_sheet):
        """Minutes matching source should score well."""
        reviewer = MinutesReviewer(good_minutes, hearing_sheet)
        reviewer.load_documents()
        score = reviewer.check_consistency()

        assert score >= 70, f"Expected score >= 70, got {score}"


# ============================================================================
# Test Full Review Integration
# ============================================================================


class TestFullReview:
    """Integration tests for complete review process."""

    def test_review_returns_result(self, good_minutes):
        """Review should return ReviewResult object."""
        reviewer = MinutesReviewer(good_minutes)
        result = reviewer.review()

        assert isinstance(result, ReviewResult)
        assert result.schema_version == "1.0"
        assert result.overall_score > 0
        assert len(result.dimension_scores) == 5

    def test_review_calculates_overall_score(self, good_minutes):
        """Overall score should be weighted average of dimensions."""
        reviewer = MinutesReviewer(good_minutes)
        result = reviewer.review()

        # Verify overall score is reasonable
        assert 0 <= result.overall_score <= 100

        # Verify all dimensions scored
        for dim in ["completeness", "action_items", "decisions", "consistency", "clarity"]:
            assert dim in result.dimension_scores

    def test_review_includes_summary(self, poor_minutes):
        """Review should include summary counts."""
        reviewer = MinutesReviewer(poor_minutes)
        result = reviewer.review()

        assert "critical_count" in result.summary
        assert "warning_count" in result.summary
        assert "suggestion_count" in result.summary

    def test_poor_minutes_lower_score_than_good(self, good_minutes, poor_minutes):
        """Poor minutes should score lower than good minutes."""
        good_reviewer = MinutesReviewer(good_minutes)
        good_result = good_reviewer.review()

        poor_reviewer = MinutesReviewer(poor_minutes)
        poor_result = poor_reviewer.review()

        assert good_result.overall_score > poor_result.overall_score, (
            f"Good score ({good_result.overall_score}) should be higher than poor ({poor_result.overall_score})"
        )


# ============================================================================
# Test Output Formatting
# ============================================================================


class TestOutputFormatting:
    """Tests for output formatting functions."""

    def test_format_markdown_produces_valid_output(self, good_minutes):
        """Markdown formatter should produce valid output."""
        reviewer = MinutesReviewer(good_minutes)
        result = reviewer.review()

        markdown = format_markdown(result)

        assert "# Meeting Minutes Review Report" in markdown
        assert "Overall Score:" in markdown
        assert "Dimension" in markdown

    def test_json_output_is_valid(self, good_minutes):
        """Result should be serializable to valid JSON."""
        reviewer = MinutesReviewer(good_minutes)
        result = reviewer.review()

        from dataclasses import asdict

        json_str = json.dumps(asdict(result))
        parsed = json.loads(json_str)

        assert "overall_score" in parsed
        assert "dimension_scores" in parsed
        assert "findings" in parsed
