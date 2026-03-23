"""
Tests for analyze_coverage.py
"""

import pytest
from analyze_coverage import CoverageAnalyzer


class TestRequirementsCoverage:
    """Tests for requirements coverage analysis."""

    def test_all_requirements_linked(self):
        """Test coverage when all requirements have tasks."""
        artifacts = {
            "requirements": [
                {"id": "REQ-001", "description": "Requirement 1"},
                {"id": "REQ-002", "description": "Requirement 2"},
            ],
            "wbs_tasks": [],
            "meetings": [],
            "decisions": [],
        }
        links = [
            {
                "source_type": "requirement",
                "source_id": "REQ-001",
                "target_type": "wbs_task",
                "target_id": "WBS-001",
                "link_type": "implemented_by",
                "confidence": 0.8,
            },
            {
                "source_type": "requirement",
                "source_id": "REQ-002",
                "target_type": "wbs_task",
                "target_id": "WBS-002",
                "link_type": "implemented_by",
                "confidence": 0.9,
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_requirements_coverage()

        assert result["total"] == 2
        assert result["with_tasks"] == 2
        assert result["without_tasks"] == 0
        assert result["coverage_percent"] == 100.0
        assert len(result["gaps"]) == 0

    def test_some_requirements_orphaned(self):
        """Test coverage when some requirements lack tasks."""
        artifacts = {
            "requirements": [
                {"id": "REQ-001", "description": "Linked requirement"},
                {"id": "REQ-002", "description": "Orphaned requirement"},
            ],
            "wbs_tasks": [],
            "meetings": [],
            "decisions": [],
        }
        links = [
            {
                "source_type": "requirement",
                "source_id": "REQ-001",
                "target_type": "wbs_task",
                "target_id": "WBS-001",
                "link_type": "implemented_by",
                "confidence": 0.8,
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_requirements_coverage()

        assert result["total"] == 2
        assert result["with_tasks"] == 1
        assert result["without_tasks"] == 1
        assert result["coverage_percent"] == 50.0
        assert len(result["gaps"]) == 1
        assert result["gaps"][0]["id"] == "REQ-002"

    def test_no_requirements(self):
        """Test coverage with no requirements."""
        artifacts = {
            "requirements": [],
            "wbs_tasks": [],
            "meetings": [],
            "decisions": [],
        }
        analyzer = CoverageAnalyzer(artifacts, [])
        result = analyzer.analyze_requirements_coverage()

        assert result["total"] == 0
        assert result["coverage_percent"] == 0.0


class TestTaskTraceability:
    """Tests for task traceability analysis."""

    def test_all_tasks_traceable(self):
        """Test when all tasks trace to requirements."""
        artifacts = {
            "requirements": [],
            "wbs_tasks": [
                {"id": "WBS-001", "name": "Task 1"},
                {"id": "WBS-002", "name": "Task 2"},
            ],
            "meetings": [],
            "decisions": [],
        }
        links = [
            {
                "source_type": "requirement",
                "source_id": "REQ-001",
                "target_type": "wbs_task",
                "target_id": "WBS-001",
                "link_type": "implemented_by",
                "confidence": 0.8,
            },
            {
                "source_type": "requirement",
                "source_id": "REQ-002",
                "target_type": "wbs_task",
                "target_id": "WBS-002",
                "link_type": "implemented_by",
                "confidence": 0.9,
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_task_traceability()

        assert result["total"] == 2
        assert result["with_requirements"] == 2
        assert result["traceability_percent"] == 100.0

    def test_orphaned_tasks(self):
        """Test detection of orphaned tasks."""
        artifacts = {
            "requirements": [],
            "wbs_tasks": [
                {"id": "WBS-001", "name": "Linked Task"},
                {"id": "WBS-002", "name": "Orphan Task"},
            ],
            "meetings": [],
            "decisions": [],
        }
        links = [
            {
                "source_type": "requirement",
                "source_id": "REQ-001",
                "target_type": "wbs_task",
                "target_id": "WBS-001",
                "link_type": "implemented_by",
                "confidence": 0.8,
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_task_traceability()

        assert result["without_requirements"] == 1
        assert len(result["gaps"]) == 1
        assert result["gaps"][0]["id"] == "WBS-002"


class TestActionItemResolution:
    """Tests for action item resolution analysis."""

    def test_all_action_items_mapped(self):
        """Test when all action items map to tasks."""
        artifacts = {
            "requirements": [],
            "wbs_tasks": [],
            "meetings": [
                {
                    "id": "MTG-001",
                    "date": "2024-01-15",
                    "action_items": [
                        {"id": "AI-001", "description": "Action 1"},
                        {"id": "AI-002", "description": "Action 2"},
                    ],
                    "decisions": [],
                }
            ],
            "decisions": [],
        }
        links = [
            {
                "source_type": "action_item",
                "source_id": "AI-001",
                "target_type": "wbs_task",
                "target_id": "WBS-001",
                "link_type": "implements",
                "confidence": 0.8,
            },
            {
                "source_type": "action_item",
                "source_id": "AI-002",
                "target_type": "wbs_task",
                "target_id": "WBS-002",
                "link_type": "implements",
                "confidence": 0.7,
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_action_item_resolution()

        assert result["total"] == 2
        assert result["mapped_to_tasks"] == 2
        assert result["resolution_percent"] == 100.0

    def test_unmapped_action_items(self):
        """Test detection of unmapped action items."""
        artifacts = {
            "requirements": [],
            "wbs_tasks": [],
            "meetings": [
                {
                    "id": "MTG-001",
                    "date": "2024-01-15",
                    "action_items": [
                        {"id": "AI-001", "description": "Mapped action"},
                        {"id": "AI-002", "description": "Unmapped action", "owner": "Alice"},
                    ],
                    "decisions": [],
                }
            ],
            "decisions": [],
        }
        links = [
            {
                "source_type": "action_item",
                "source_id": "AI-001",
                "target_type": "wbs_task",
                "target_id": "WBS-001",
                "link_type": "implements",
                "confidence": 0.8,
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_action_item_resolution()

        assert result["unmapped"] == 1
        assert len(result["gaps"]) == 1
        assert result["gaps"][0]["id"] == "AI-002"
        assert result["gaps"][0]["meeting_id"] == "MTG-001"


class TestLinkQuality:
    """Tests for link quality analysis."""

    def test_high_confidence_links(self):
        """Test categorization of high confidence links."""
        artifacts = {"requirements": [], "wbs_tasks": [], "meetings": [], "decisions": []}
        links = [
            {
                "source_type": "req",
                "source_id": "1",
                "target_type": "task",
                "target_id": "1",
                "link_type": "implements",
                "confidence": 0.95,
                "match_reason": "exact",
            },
            {
                "source_type": "req",
                "source_id": "2",
                "target_type": "task",
                "target_id": "2",
                "link_type": "implements",
                "confidence": 0.85,
                "match_reason": "keyword",
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_link_quality()

        assert result["total_links"] == 2
        assert result["high_confidence"] == 2
        assert result["low_confidence"] == 0

    def test_low_confidence_flagged(self):
        """Test that low confidence links are flagged."""
        artifacts = {"requirements": [], "wbs_tasks": [], "meetings": [], "decisions": []}
        links = [
            {
                "source_type": "req",
                "source_id": "1",
                "target_type": "task",
                "target_id": "1",
                "link_type": "implements",
                "confidence": 0.45,
                "match_reason": "weak",
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_link_quality()

        assert result["low_confidence"] == 1
        assert len(result["low_confidence_links"]) == 1

    def test_average_confidence(self):
        """Test average confidence calculation."""
        artifacts = {"requirements": [], "wbs_tasks": [], "meetings": [], "decisions": []}
        links = [
            {
                "source_type": "req",
                "source_id": "1",
                "target_type": "task",
                "target_id": "1",
                "link_type": "implements",
                "confidence": 0.80,
                "match_reason": "test",
            },
            {
                "source_type": "req",
                "source_id": "2",
                "target_type": "task",
                "target_id": "2",
                "link_type": "implements",
                "confidence": 0.60,
                "match_reason": "test",
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.analyze_link_quality()

        assert result["average_confidence"] == 0.70


class TestOverallHealth:
    """Tests for overall health score calculation."""

    def test_healthy_project(self):
        """Test health score for well-linked project."""
        artifacts = {
            "requirements": [{"id": "REQ-001", "description": "Test"}],
            "wbs_tasks": [{"id": "WBS-001", "name": "Test"}],
            "meetings": [],
            "decisions": [],
        }
        links = [
            {
                "source_type": "requirement",
                "source_id": "REQ-001",
                "target_type": "wbs_task",
                "target_id": "WBS-001",
                "link_type": "implemented_by",
                "confidence": 0.90,
                "match_reason": "test",
            },
        ]
        analyzer = CoverageAnalyzer(artifacts, links)
        result = analyzer.calculate_overall_health()

        assert result["overall_score"] > 50
        assert result["status"] in ["healthy", "needs_attention"]

    def test_critical_project(self):
        """Test health score for poorly linked project."""
        artifacts = {
            "requirements": [
                {"id": "REQ-001", "description": "Test 1"},
                {"id": "REQ-002", "description": "Test 2"},
                {"id": "REQ-003", "description": "Test 3"},
            ],
            "wbs_tasks": [],
            "meetings": [],
            "decisions": [],
        }
        analyzer = CoverageAnalyzer(artifacts, [])
        result = analyzer.calculate_overall_health()

        assert result["overall_score"] < 60
        assert result["status"] == "critical"


class TestReportGeneration:
    """Tests for full report generation."""

    def test_generate_report_structure(self):
        """Test that generated report has expected structure."""
        artifacts = {
            "requirements": [{"id": "REQ-001", "description": "Test"}],
            "wbs_tasks": [{"id": "WBS-001", "name": "Test"}],
            "meetings": [
                {
                    "id": "MTG-001",
                    "action_items": [{"id": "AI-001", "description": "Test"}],
                    "decisions": [{"id": "DEC-001", "description": "Test"}],
                }
            ],
            "decisions": [],
        }
        analyzer = CoverageAnalyzer(artifacts, [])
        report = analyzer.generate_report()

        assert "schema_version" in report
        assert "analysis_date" in report
        assert "overall_health" in report
        assert "requirements_coverage" in report
        assert "task_traceability" in report
        assert "decision_documentation" in report
        assert "action_item_resolution" in report
        assert "link_quality" in report

    def test_report_has_gaps_info(self):
        """Test that report includes gap information."""
        artifacts = {
            "requirements": [{"id": "REQ-001", "description": "Orphan"}],
            "wbs_tasks": [],
            "meetings": [],
            "decisions": [],
        }
        analyzer = CoverageAnalyzer(artifacts, [])
        report = analyzer.generate_report()

        gaps = report["requirements_coverage"]["gaps"]
        assert len(gaps) == 1
        assert gaps[0]["id"] == "REQ-001"
