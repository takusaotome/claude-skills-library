"""Tests for init_procurement module."""

from datetime import datetime
from pathlib import Path

import pytest
from init_procurement import (
    create_project_structure,
    init_procurement_project,
)
from procurement_models import ProcurementProject, ProcurementStatus


class TestCreateProjectStructure:
    """Tests for directory structure creation."""

    def test_creates_all_directories(self, tmp_path):
        """Test that all required directories are created."""
        output_dir = tmp_path / "test_project"

        create_project_structure(output_dir)

        assert (output_dir / "rfq").is_dir()
        assert (output_dir / "quotes").is_dir()
        assert (output_dir / "estimates").is_dir()
        assert (output_dir / "communications").is_dir()

    def test_idempotent_creation(self, tmp_path):
        """Test that creating structure multiple times is safe."""
        output_dir = tmp_path / "test_project"

        create_project_structure(output_dir)
        # Create a file in one of the directories
        (output_dir / "rfq" / "test.md").write_text("test content")

        # Run again
        create_project_structure(output_dir)

        # Directory should still exist with content
        assert (output_dir / "rfq" / "test.md").exists()


class TestInitProcurementProject:
    """Tests for project initialization."""

    def test_basic_initialization(self, tmp_path):
        """Test basic project initialization."""
        output_dir = tmp_path / "erp_project"

        project = init_procurement_project(
            project_name="ERP Modernization",
            client="Acme Corp",
            output_dir=output_dir,
        )

        assert project.name == "ERP Modernization"
        assert project.client == "Acme Corp"
        assert project.status == ProcurementStatus.INITIALIZED
        assert len(project.timeline) == 1  # Initialization event

    def test_creates_config_file(self, tmp_path):
        """Test that procurement.yaml is created."""
        output_dir = tmp_path / "test_project"

        init_procurement_project(
            project_name="Test Project",
            client="Test Client",
            output_dir=output_dir,
        )

        config_path = output_dir / "procurement.yaml"
        assert config_path.exists()

    def test_config_file_loadable(self, tmp_path):
        """Test that created config file can be loaded."""
        output_dir = tmp_path / "test_project"

        original = init_procurement_project(
            project_name="Test Project",
            client="Test Client",
            output_dir=output_dir,
            description="Test description",
        )

        config_path = output_dir / "procurement.yaml"
        loaded = ProcurementProject.load(config_path)

        assert loaded.name == original.name
        assert loaded.client == original.client
        assert loaded.description == "Test description"

    def test_with_description(self, tmp_path):
        """Test initialization with description."""
        output_dir = tmp_path / "test_project"

        project = init_procurement_project(
            project_name="CRM Implementation",
            client="Big Corp",
            output_dir=output_dir,
            description="Replace legacy CRM with Salesforce",
        )

        assert project.description == "Replace legacy CRM with Salesforce"

    def test_timeline_event_added(self, tmp_path):
        """Test that initialization event is added to timeline."""
        output_dir = tmp_path / "test_project"

        project = init_procurement_project(
            project_name="Test Project",
            client="Test Client",
            output_dir=output_dir,
        )

        assert len(project.timeline) == 1
        assert "initialized" in project.timeline[0].event.lower()
        assert "Test Client" in project.timeline[0].details
