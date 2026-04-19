"""
Tests for generate_roadmap.py
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from generate_roadmap import (
    PHASE_TEMPLATES,
    SERVICE_COMPLEXITY,
    calculate_complexity_factor,
    generate_milestones,
    generate_roadmap,
    generate_timeline,
)


class TestCalculateComplexityFactor:
    """Tests for complexity factor calculation."""

    def test_single_low_complexity_service(self):
        """Should return low factor for single simple service."""
        services = [{"service_id": "cs-001"}]  # Low complexity
        factor = calculate_complexity_factor(services)
        assert factor < 1.2

    def test_multiple_high_complexity_services(self):
        """Should return higher factor for complex services."""
        services = [
            {"service_id": "hr-001"},  # High
            {"service_id": "hr-004"},  # High
            {"service_id": "fin-001"},  # Medium
        ]
        factor = calculate_complexity_factor(services)
        assert factor > 1.0

    def test_many_services_increase_factor(self):
        """More services should increase complexity factor."""
        few = calculate_complexity_factor([{"service_id": "fin-001"}])
        many = calculate_complexity_factor(
            [
                {"service_id": "fin-001"},
                {"service_id": "fin-002"},
                {"service_id": "fin-003"},
                {"service_id": "fin-004"},
                {"service_id": "hr-001"},
            ]
        )
        assert many > few

    def test_empty_services_list(self):
        """Should handle empty services list."""
        factor = calculate_complexity_factor([])
        assert factor >= 0


class TestGenerateTimeline:
    """Tests for timeline generation."""

    def test_generates_all_phases(self):
        """Should generate all requested phases."""
        phases = ["discovery", "pilot", "rollout", "optimization"]
        timeline = generate_timeline("2025-04-01", phases)
        assert len(timeline) == 4
        phase_keys = [p["phase_key"] for p in timeline]
        assert phase_keys == phases

    def test_dates_are_sequential(self):
        """Phase end dates should match next phase start dates."""
        timeline = generate_timeline("2025-04-01", ["discovery", "pilot"])
        discovery_end = datetime.strptime(timeline[0]["end_date"], "%Y-%m-%d")
        pilot_start = datetime.strptime(timeline[1]["start_date"], "%Y-%m-%d")
        assert discovery_end == pilot_start

    def test_complexity_extends_duration(self):
        """Higher complexity should extend phase durations."""
        normal = generate_timeline("2025-04-01", ["discovery"], 1.0)
        extended = generate_timeline("2025-04-01", ["discovery"], 1.5)
        assert extended[0]["duration_weeks"] > normal[0]["duration_weeks"]

    def test_includes_bilingual_names(self):
        """Should include both English and Japanese phase names."""
        timeline = generate_timeline("2025-04-01", ["discovery"])
        phase = timeline[0]
        assert "phase_name" in phase
        assert "phase_name_ja" in phase
        assert phase["phase_name_ja"] != ""

    def test_includes_activities(self):
        """Should include activities within each phase."""
        timeline = generate_timeline("2025-04-01", ["discovery"])
        phase = timeline[0]
        assert "activities" in phase
        assert len(phase["activities"]) > 0
        activity = phase["activities"][0]
        assert "name" in activity
        assert "start_date" in activity
        assert "end_date" in activity


class TestGenerateMilestones:
    """Tests for milestone generation."""

    def test_generates_milestones_from_timeline(self):
        """Should generate milestones for each phase."""
        timeline = generate_timeline("2025-04-01", ["discovery", "pilot", "rollout", "optimization"])
        milestones = generate_milestones(timeline)
        assert len(milestones) == 4

    def test_milestones_have_bilingual_names(self):
        """Should include both English and Japanese milestone names."""
        timeline = generate_timeline("2025-04-01", ["pilot"])
        milestones = generate_milestones(timeline)
        milestone = milestones[0]
        assert "name" in milestone
        assert "name_ja" in milestone

    def test_milestone_dates_match_phase_end(self):
        """Milestone dates should match phase end dates."""
        timeline = generate_timeline("2025-04-01", ["discovery"])
        milestones = generate_milestones(timeline)
        assert milestones[0]["date"] == timeline[0]["end_date"]


class TestGenerateRoadmap:
    """Tests for full roadmap generation."""

    def test_generates_valid_roadmap(self):
        """Should generate valid roadmap structure."""
        roadmap = generate_roadmap(start_date="2025-04-01")
        assert "schema_version" in roadmap
        assert "project_start" in roadmap
        assert "project_end" in roadmap
        assert "phases" in roadmap
        assert "milestones" in roadmap

    def test_uses_services_for_complexity(self, tmp_path):
        """Should use services to calculate complexity."""
        services_data = {
            "selected_services": [
                {"service_id": "hr-001"},
                {"service_id": "hr-004"},
            ]
        }
        services_file = tmp_path / "services.json"
        with open(services_file, "w") as f:
            json.dump(services_data, f)

        roadmap = generate_roadmap(services_file=str(services_file), start_date="2025-04-01")
        assert roadmap["complexity_factor"] > 1.0

    def test_saves_to_file(self, tmp_path):
        """Should save roadmap to file when path provided."""
        output_file = tmp_path / "roadmap.json"
        generate_roadmap(start_date="2025-04-01", output_path=str(output_file))
        assert output_file.exists()
        with open(output_file) as f:
            saved = json.load(f)
        assert saved["project_start"] == "2025-04-01"

    def test_default_start_date(self):
        """Should use default start date if not provided."""
        roadmap = generate_roadmap()
        assert "project_start" in roadmap
        # Default should be ~2 weeks from now
        start = datetime.strptime(roadmap["project_start"], "%Y-%m-%d")
        assert start > datetime.now()

    def test_includes_assumptions(self):
        """Should include assumptions in both languages."""
        roadmap = generate_roadmap(start_date="2025-04-01")
        assert "assumptions" in roadmap
        assert "assumptions_ja" in roadmap
        assert len(roadmap["assumptions"]) > 0
        assert len(roadmap["assumptions_ja"]) > 0
