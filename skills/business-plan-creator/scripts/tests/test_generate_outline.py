"""Tests for generate_outline.py"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).parent.parent / "generate_outline.py"


class TestGenerateOutline:
    """Tests for the outline generator script."""

    def test_generates_markdown_file(self, tmp_path: Path) -> None:
        """Test that the script generates a markdown outline file."""
        output_file = tmp_path / "outline.md"

        result = subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "investor_pitch",
                "--industry",
                "saas",
                "--language",
                "ja",
                "--company",
                "TestCorp",
                "--output",
                str(output_file),
            ],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"Script failed: {result.stderr}"
        assert output_file.exists()
        content = output_file.read_text()
        assert "TestCorp" in content
        assert "saas" in content

    def test_full_template_for_investor_pitch(self, tmp_path: Path) -> None:
        """Test that investor pitch uses full template with all sections."""
        output_file = tmp_path / "outline.md"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "investor_pitch",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        content = output_file.read_text()
        # Full template should have 12 sections
        assert "1. Executive Summary" in content
        assert "12. Appendix" in content

    def test_short_template_for_internal_proposal(self, tmp_path: Path) -> None:
        """Test that internal proposal uses short template."""
        output_file = tmp_path / "outline.md"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "internal_proposal",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        content = output_file.read_text()
        # Short template should have 7 sections
        assert "1. Proposal Summary" in content
        assert "7. Risks and Mitigations" in content
        # Should NOT have full template sections
        assert "12. Appendix" not in content

    def test_short_template_for_draft(self, tmp_path: Path) -> None:
        """Test that draft uses short template."""
        output_file = tmp_path / "outline.md"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "draft",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        content = output_file.read_text()
        assert "1. Proposal Summary" in content

    def test_english_labels(self, tmp_path: Path) -> None:
        """Test English language labels."""
        output_file = tmp_path / "outline.md"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "bank_loan",
                "--language",
                "en",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        content = output_file.read_text()
        assert "Bank Loan Application" in content
        assert "Language: en" in content

    def test_japanese_labels(self, tmp_path: Path) -> None:
        """Test Japanese language labels."""
        output_file = tmp_path / "outline.md"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "bank_loan",
                "--language",
                "ja",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        content = output_file.read_text()
        assert "銀行融資申請" in content

    def test_custom_horizon_years(self, tmp_path: Path) -> None:
        """Test custom planning horizon."""
        output_file = tmp_path / "outline.md"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "investor_pitch",
                "--horizon-years",
                "5",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        content = output_file.read_text()
        assert "Planning Horizon: 5 years" in content

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """Test that the script creates parent directories if needed."""
        output_file = tmp_path / "nested" / "dir" / "outline.md"

        subprocess.run(
            [
                "python3",
                str(SCRIPT_PATH),
                "--purpose",
                "draft",
                "--output",
                str(output_file),
            ],
            check=True,
        )

        assert output_file.exists()

    def test_missing_required_args_fails(self) -> None:
        """Test that missing required arguments cause failure."""
        result = subprocess.run(
            ["python3", str(SCRIPT_PATH)],
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0

    def test_all_purpose_types(self, tmp_path: Path) -> None:
        """Test that all purpose types work."""
        purposes = [
            "investor_pitch",
            "bank_loan",
            "internal_proposal",
            "draft",
            "public_agency",
        ]

        for purpose in purposes:
            output_file = tmp_path / f"{purpose}.md"
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT_PATH),
                    "--purpose",
                    purpose,
                    "--output",
                    str(output_file),
                ],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"Failed for purpose {purpose}: {result.stderr}"
            assert output_file.exists()
