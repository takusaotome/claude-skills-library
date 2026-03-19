"""
Tests for wbs_reviewer.py
"""

import json
from pathlib import Path

import pytest
from openpyxl import Workbook
from wbs_reviewer import WBSReviewer


@pytest.fixture
def sample_wbs_excel(tmp_path):
    """Create a sample WBS Excel file"""
    wb = Workbook()
    ws = wb.active

    # Add headers
    headers = ["WBS Code", "Task Name", "Effort (hours)", "Resource"]
    ws.append(headers)

    # Add sample tasks
    tasks = [
        ["1.0", "Project Initiation", 40, "PM"],
        ["1.1", "Kickoff Meeting (REQ-001)", 8, "PM"],
        ["1.2", "Requirements Gathering", 32, "BA"],
        ["2.0", "Design Phase", 80, "Architect"],
        ["2.1", "System Architecture (REQ-002)", 40, "Architect"],
        ["2.2", "Database Design", None, "DBA"],  # Missing effort
        ["3.0", "Development", 200, "Dev Team"],
        ["3.1", "Frontend Development (REQ-003)", 100, "Frontend Dev"],
    ]

    for task in tasks:
        ws.append(task)

    excel_path = tmp_path / "sample_wbs.xlsx"
    wb.save(excel_path)
    return excel_path


@pytest.fixture
def sample_requirements(tmp_path):
    """Create a sample requirements file"""
    content = """# Project Requirements

## Functional Requirements

- REQ-001: User authentication system
- REQ-002: System architecture design
- REQ-003: Frontend user interface
- REQ-004: Data export functionality (NOT IN WBS - should be flagged)

## Technology Stack

- Frontend: React
- Backend: Django
"""

    req_file = tmp_path / "requirements.md"
    req_file.write_text(content, encoding="utf-8")
    return req_file


@pytest.fixture
def sample_hearing_notes(tmp_path):
    """Create sample hearing notes"""
    content = """# Meeting Notes - 2025-11-15

## Decisions

- Decision: Use PostgreSQL instead of MySQL for JSON support
- Agreed: Implement two-factor authentication in phase 2
"""

    notes_file = tmp_path / "hearing_notes.md"
    notes_file.write_text(content, encoding="utf-8")
    return notes_file


@pytest.fixture
def review_checklist(tmp_path):
    """Create a minimal review checklist"""
    checklist = {
        "schema_version": "1.0",
        "categories": {
            "completeness": {
                "name": "Completeness",
                "criteria": [
                    {
                        "id": "COMP-001",
                        "name": "All requirements mapped",
                        "description": "Every requirement must map to WBS task",
                        "severity": "critical",
                        "check_type": "traceability",
                    }
                ],
            }
        },
        "severity_levels": {
            "critical": {"priority": 1, "color": "red"},
            "major": {"priority": 2, "color": "orange"},
            "minor": {"priority": 3, "color": "yellow"},
        },
    }

    import yaml

    checklist_file = tmp_path / "checklist.yaml"
    checklist_file.write_text(yaml.dump(checklist))
    return checklist_file


class TestWBSReviewer:
    """Test cases for WBSReviewer"""

    def test_initialize_reviewer(self, sample_wbs_excel, sample_requirements):
        """Test reviewer initialization"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        assert reviewer.wbs_path.exists()
        assert reviewer.requirements_path.exists()
        assert reviewer.wbs_df is not None
        assert len(reviewer.requirements_data["requirements"]) >= 4

    def test_find_missing_requirements(self, sample_wbs_excel, sample_requirements):
        """Test detection of unmapped requirements"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        results = reviewer.review()

        # REQ-004 should be flagged as missing (not in WBS)
        missing_reqs = [f for f in results["findings"] if "REQ-004" in f.get("requirement_ref", "")]
        assert len(missing_reqs) > 0

        # Check traceability matrix
        req_004_trace = next((t for t in results["traceability_matrix"] if t["requirement_id"] == "REQ-004"), None)
        assert req_004_trace is not None
        assert req_004_trace["coverage_status"] == "missing"

    def test_find_covered_requirements(self, sample_wbs_excel, sample_requirements):
        """Test detection of properly mapped requirements"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        results = reviewer.review()

        # REQ-001, REQ-002, REQ-003 should be covered
        covered_reqs = [t for t in results["traceability_matrix"] if t["coverage_status"] == "covered"]
        assert len(covered_reqs) >= 3

        # Check specific requirement
        req_001_trace = next((t for t in results["traceability_matrix"] if t["requirement_id"] == "REQ-001"), None)
        assert req_001_trace is not None
        assert req_001_trace["coverage_status"] == "covered"
        assert len(req_001_trace["mapped_tasks"]) > 0

    def test_detect_missing_effort(self, sample_wbs_excel, sample_requirements):
        """Test detection of missing effort estimates"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        results = reviewer.review()

        # Task 2.2 "Database Design" has no effort - should be flagged
        missing_effort_findings = [f for f in results["findings"] if f["category"] == "missing_effort"]
        assert len(missing_effort_findings) > 0

    def test_calculate_readiness_score(self, sample_wbs_excel, sample_requirements):
        """Test readiness score calculation"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        results = reviewer.review()
        summary = results["summary"]

        # Check readiness score exists and is reasonable
        assert "readiness_score" in summary
        assert 0 <= summary["readiness_score"] <= 100

        # Check status determination
        assert "status" in summary
        assert summary["status"] in ["Ready for baseline", "Needs revision", "Significant gaps", "Incomplete"]

    def test_severity_counts(self, sample_wbs_excel, sample_requirements):
        """Test that findings are categorized by severity"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        results = reviewer.review()
        summary = results["summary"]

        # Check severity counts
        assert "critical_count" in summary
        assert "major_count" in summary
        assert "minor_count" in summary

        total_findings = summary["critical_count"] + summary["major_count"] + summary["minor_count"]
        assert total_findings == len(results["findings"])

    def test_export_json(self, sample_wbs_excel, sample_requirements, tmp_path):
        """Test JSON export functionality"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        reviewer.review()
        output_paths = reviewer.export_results(str(tmp_path / "output"))

        # Check JSON file created
        json_path = Path(output_paths["json_path"])
        assert json_path.exists()

        # Check JSON content
        json_data = json.loads(json_path.read_text())
        assert "schema_version" in json_data
        assert "findings" in json_data
        assert "traceability_matrix" in json_data
        assert "summary" in json_data

    def test_export_markdown(self, sample_wbs_excel, sample_requirements, tmp_path):
        """Test Markdown export functionality"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        reviewer.review()
        output_paths = reviewer.export_results(str(tmp_path / "output"))

        # Check Markdown file created
        md_path = Path(output_paths["markdown_path"])
        assert md_path.exists()

        # Check Markdown content
        md_content = md_path.read_text()
        assert "# WBS Review Summary" in md_content
        assert "Executive Summary" in md_content
        assert "Requirements Coverage Analysis" in md_content

    def test_export_annotated_excel(self, sample_wbs_excel, sample_requirements, tmp_path):
        """Test annotated Excel export"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        reviewer.review()
        output_paths = reviewer.export_results(str(tmp_path / "output"))

        # Check annotated Excel created
        excel_path = Path(output_paths["excel_path"])
        assert excel_path.exists()
        assert excel_path.suffix == ".xlsx"

    def test_hearing_notes_integration(self, sample_wbs_excel, sample_requirements, sample_hearing_notes):
        """Test hearing notes are checked against WBS"""
        reviewer = WBSReviewer(
            wbs_path=str(sample_wbs_excel),
            requirements_path=str(sample_requirements),
            hearing_sheet_path=str(sample_hearing_notes),
        )

        results = reviewer.review()

        # Should have parsed hearing notes
        assert len(reviewer.hearing_notes) > 0

        # May have findings related to hearing notes
        hearing_findings = [f for f in results["findings"] if f["category"] == "hearing_decision_missing"]
        # Note: Findings depend on whether WBS mentions PostgreSQL/authentication

    def test_missing_task_suggestions(self, sample_wbs_excel, sample_requirements):
        """Test that missing task candidates are generated"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        results = reviewer.review()

        # Should have missing task suggestions
        assert "missing_tasks" in results
        assert len(results["missing_tasks"]) > 0

        # Check structure of missing tasks
        for task in results["missing_tasks"]:
            assert "source" in task
            assert "suggested_task" in task
            assert "priority" in task

    def test_custom_checklist(self, sample_wbs_excel, sample_requirements, review_checklist):
        """Test using custom review checklist"""
        reviewer = WBSReviewer(
            wbs_path=str(sample_wbs_excel),
            requirements_path=str(sample_requirements),
            checklist_path=str(review_checklist),
        )

        assert reviewer.checklist is not None
        assert "categories" in reviewer.checklist

    def test_wbs_column_detection(self, sample_wbs_excel, sample_requirements):
        """Test that WBS columns are correctly detected"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        # Check columns detected
        assert reviewer.wbs_code_col is not None
        assert reviewer.task_name_col is not None
        # effort_col and resource_col may be None if not found

    def test_is_leaf_task(self, sample_wbs_excel, sample_requirements):
        """Test leaf task detection"""
        reviewer = WBSReviewer(wbs_path=str(sample_wbs_excel), requirements_path=str(sample_requirements))

        # 1.1 is a leaf (no children)
        assert reviewer._is_leaf_task("1.1") is True

        # 1.0 is not a leaf (has 1.1, 1.2 children)
        assert reviewer._is_leaf_task("1.0") is False
