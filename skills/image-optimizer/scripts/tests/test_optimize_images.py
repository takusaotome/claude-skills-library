"""
Tests for optimize_images.py module.
"""

from dataclasses import asdict
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from analyze_image import ImageInfo, ImageTypeDetection
from optimize_images import (
    OptimizationResult,
    check_avifenc,
    check_cwebp,
    determine_output_format,
    generate_markdown_report,
)


class TestToolAvailability:
    """Tests for external tool availability checks."""

    @patch("optimize_images.subprocess.run")
    def test_cwebp_available(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        assert check_cwebp() is True

    @patch("optimize_images.subprocess.run")
    def test_cwebp_not_available(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        assert check_cwebp() is False

    @patch("optimize_images.subprocess.run")
    def test_avifenc_available(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        assert check_avifenc() is True

    @patch("optimize_images.subprocess.run")
    def test_avifenc_not_available(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        assert check_avifenc() is False


class TestDetermineOutputFormat:
    """Tests for output format determination."""

    def test_explicit_format_jpeg(self):
        info = ImageInfo(
            path="/test/img.png",
            filename="img.png",
            width=100,
            height=100,
            format="PNG",
            color_space="sRGB",
            depth=8,
            size_bytes=10000,
            has_transparency=False,
            unique_colors=1000,
        )
        detection = ImageTypeDetection(
            detected_type="photo", confidence=0.9, edge_density=0.1, color_variance=0.8, solid_region_ratio=0.1
        )

        result = determine_output_format(info, detection, "jpeg", True, True)
        assert result == "jpeg"

    def test_auto_photo_with_cwebp(self):
        info = ImageInfo(
            path="/test/photo.jpg",
            filename="photo.jpg",
            width=1920,
            height=1080,
            format="JPEG",
            color_space="sRGB",
            depth=8,
            size_bytes=500000,
            has_transparency=False,
            unique_colors=500000,
        )
        detection = ImageTypeDetection(
            detected_type="photo", confidence=0.9, edge_density=0.08, color_variance=0.8, solid_region_ratio=0.1
        )

        result = determine_output_format(info, detection, "auto", True, False)
        assert result == "webp"

    def test_auto_diagram(self):
        info = ImageInfo(
            path="/test/diagram.png",
            filename="diagram.png",
            width=800,
            height=600,
            format="PNG",
            color_space="sRGB",
            depth=8,
            size_bytes=50000,
            has_transparency=False,
            unique_colors=50,
        )
        detection = ImageTypeDetection(
            detected_type="diagram", confidence=0.85, edge_density=0.35, color_variance=0.01, solid_region_ratio=0.8
        )

        result = determine_output_format(info, detection, "auto", True, True)
        assert result == "png"

    def test_auto_screenshot_with_transparency(self):
        info = ImageInfo(
            path="/test/screenshot.png",
            filename="screenshot.png",
            width=1920,
            height=1080,
            format="PNG",
            color_space="sRGB",
            depth=8,
            size_bytes=200000,
            has_transparency=True,
            unique_colors=30000,
        )
        detection = ImageTypeDetection(
            detected_type="screenshot", confidence=0.8, edge_density=0.25, color_variance=0.3, solid_region_ratio=0.5
        )

        result = determine_output_format(info, detection, "auto", False, False)
        assert result == "png"  # PNG for transparency without cwebp


class TestOptimizationResult:
    """Tests for OptimizationResult dataclass."""

    def test_successful_result(self):
        result = OptimizationResult(
            input_path="/input/image.jpg",
            output_path="/output/image.webp",
            original_size_bytes=1000000,
            optimized_size_bytes=200000,
            reduction_percent=80.0,
            output_format="webp",
            quality_used=82,
            dimensions={"width": 1920, "height": 1080},
            success=True,
        )

        assert result.success is True
        assert result.error_message is None
        assert result.reduction_percent == 80.0

    def test_failed_result(self):
        result = OptimizationResult(
            input_path="/input/corrupted.jpg",
            output_path="",
            original_size_bytes=0,
            optimized_size_bytes=0,
            reduction_percent=0,
            output_format="",
            quality_used=0,
            dimensions={},
            success=False,
            error_message="Failed to read image",
        )

        assert result.success is False
        assert result.error_message == "Failed to read image"

    def test_result_to_dict(self):
        result = OptimizationResult(
            input_path="/input/image.jpg",
            output_path="/output/image.webp",
            original_size_bytes=1000000,
            optimized_size_bytes=200000,
            reduction_percent=80.0,
            output_format="webp",
            quality_used=82,
            dimensions={"width": 1920, "height": 1080},
            success=True,
        )

        result_dict = asdict(result)

        assert result_dict["input_path"] == "/input/image.jpg"
        assert result_dict["success"] is True
        assert "dimensions" in result_dict


class TestGenerateMarkdownReport:
    """Tests for markdown report generation."""

    def test_report_with_successful_results(self, tmp_path):
        results = [
            OptimizationResult(
                input_path="/input/image1.jpg",
                output_path="/output/image1.webp",
                original_size_bytes=1000000,
                optimized_size_bytes=200000,
                reduction_percent=80.0,
                output_format="webp",
                quality_used=82,
                dimensions={"width": 1920, "height": 1080},
                success=True,
            ),
            OptimizationResult(
                input_path="/input/image2.png",
                output_path="/output/image2.webp",
                original_size_bytes=500000,
                optimized_size_bytes=100000,
                reduction_percent=80.0,
                output_format="webp",
                quality_used=85,
                dimensions={"width": 800, "height": 600},
                success=True,
            ),
        ]

        report_path = tmp_path / "report.md"
        generate_markdown_report(results, 5.5, report_path)

        assert report_path.exists()
        content = report_path.read_text()

        assert "# Image Optimization Report" in content
        assert "Images Processed | 2" in content
        assert "Failed | 0" in content
        assert "image1.jpg" in content
        assert "image2.png" in content

    def test_report_with_failed_results(self, tmp_path):
        results = [
            OptimizationResult(
                input_path="/input/good.jpg",
                output_path="/output/good.webp",
                original_size_bytes=1000000,
                optimized_size_bytes=200000,
                reduction_percent=80.0,
                output_format="webp",
                quality_used=82,
                dimensions={"width": 1920, "height": 1080},
                success=True,
            ),
            OptimizationResult(
                input_path="/input/bad.jpg",
                output_path="",
                original_size_bytes=0,
                optimized_size_bytes=0,
                reduction_percent=0,
                output_format="",
                quality_used=0,
                dimensions={},
                success=False,
                error_message="Corrupted file",
            ),
        ]

        report_path = tmp_path / "report.md"
        generate_markdown_report(results, 3.2, report_path)

        content = report_path.read_text()

        assert "Images Processed | 1" in content
        assert "Failed | 1" in content
        assert "## Failed Images" in content
        assert "bad.jpg" in content
        assert "Corrupted file" in content

    def test_report_processing_time(self, tmp_path):
        results = [
            OptimizationResult(
                input_path="/input/image.jpg",
                output_path="/output/image.webp",
                original_size_bytes=1000000,
                optimized_size_bytes=200000,
                reduction_percent=80.0,
                output_format="webp",
                quality_used=82,
                dimensions={"width": 1920, "height": 1080},
                success=True,
            )
        ]

        report_path = tmp_path / "report.md"
        generate_markdown_report(results, 12.345, report_path)

        content = report_path.read_text()

        assert "Processing Time | 12.3s" in content
