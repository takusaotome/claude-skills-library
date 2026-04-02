"""
Tests for analyze_image.py module.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from analyze_image import (
    ImageInfo,
    ImageTypeDetection,
    check_imagemagick,
    detect_image_type,
    find_images,
    get_optimization_recommendation,
    human_readable_size,
    parse_size_string,
)


class TestHumanReadableSize:
    """Tests for human_readable_size function."""

    def test_bytes(self):
        assert human_readable_size(500) == "500.0 B"

    def test_kilobytes(self):
        assert human_readable_size(1024) == "1.0 KB"
        assert human_readable_size(2048) == "2.0 KB"
        assert human_readable_size(1536) == "1.5 KB"

    def test_megabytes(self):
        assert human_readable_size(1024 * 1024) == "1.0 MB"
        assert human_readable_size(2.5 * 1024 * 1024) == "2.5 MB"

    def test_gigabytes(self):
        assert human_readable_size(1024 * 1024 * 1024) == "1.0 GB"


class TestParseSizeString:
    """Tests for parse_size_string function."""

    def test_bytes(self):
        assert parse_size_string("100B") == 100

    def test_kilobytes(self):
        assert parse_size_string("100KB") == 100 * 1024
        assert parse_size_string("100kb") == 100 * 1024

    def test_megabytes(self):
        assert parse_size_string("1MB") == 1024 * 1024
        assert parse_size_string("2.5MB") == int(2.5 * 1024 * 1024)

    def test_gigabytes(self):
        assert parse_size_string("1GB") == 1024 * 1024 * 1024

    def test_with_spaces(self):
        assert parse_size_string("  100KB  ") == 100 * 1024

    def test_plain_number(self):
        assert parse_size_string("1000") == 1000


class TestCheckImagemagick:
    """Tests for ImageMagick availability check."""

    @patch("analyze_image.subprocess.run")
    def test_imagemagick_available(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        assert check_imagemagick() is True

    @patch("analyze_image.subprocess.run")
    def test_imagemagick_not_available_error(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        assert check_imagemagick() is False

    @patch("analyze_image.subprocess.run")
    def test_imagemagick_not_available_nonzero(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        assert check_imagemagick() is False


class TestImageTypeDetection:
    """Tests for image type detection logic."""

    def test_photo_detection(self):
        # Create mock image info for a photo
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
            unique_colors=500000,  # High color count
        )

        # Mock the analysis functions
        with patch("analyze_image.calculate_edge_density", return_value=0.08):
            with patch("analyze_image.estimate_solid_region_ratio", return_value=0.15):
                detection = detect_image_type(info, Path("/test/photo.jpg"))

        assert detection.detected_type == "photo"
        assert detection.confidence > 0.5

    def test_diagram_detection(self):
        # Create mock image info for a diagram
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
            unique_colors=50,  # Very low color count
        )

        with patch("analyze_image.calculate_edge_density", return_value=0.35):
            with patch("analyze_image.estimate_solid_region_ratio", return_value=0.8):
                detection = detect_image_type(info, Path("/test/diagram.png"))

        assert detection.detected_type == "diagram"
        assert detection.confidence > 0.5

    def test_screenshot_detection(self):
        # Create mock image info for a screenshot
        info = ImageInfo(
            path="/test/screenshot.png",
            filename="screenshot.png",
            width=1920,
            height=1080,
            format="PNG",
            color_space="sRGB",
            depth=8,
            size_bytes=200000,
            has_transparency=False,
            unique_colors=50000,  # Medium color count
        )

        with patch("analyze_image.calculate_edge_density", return_value=0.25):
            with patch("analyze_image.estimate_solid_region_ratio", return_value=0.5):
                detection = detect_image_type(info, Path("/test/screenshot.png"))

        assert detection.detected_type == "screenshot"
        assert detection.confidence > 0.5


class TestOptimizationRecommendation:
    """Tests for optimization recommendation generation."""

    def test_photo_recommendation(self):
        info = ImageInfo(
            path="/test/photo.jpg",
            filename="photo.jpg",
            width=3000,
            height=2000,
            format="JPEG",
            color_space="sRGB",
            depth=8,
            size_bytes=2000000,
            has_transparency=False,
            unique_colors=1000000,
        )

        detection = ImageTypeDetection(
            detected_type="photo", confidence=0.9, edge_density=0.1, color_variance=0.8, solid_region_ratio=0.1
        )

        rec = get_optimization_recommendation(info, detection)

        assert rec.format == "webp"
        assert 75 <= rec.quality <= 90
        assert rec.max_dimension == 2560  # Should cap large images
        assert rec.estimated_size_bytes < info.size_bytes

    def test_diagram_recommendation(self):
        info = ImageInfo(
            path="/test/diagram.png",
            filename="diagram.png",
            width=800,
            height=600,
            format="PNG",
            color_space="sRGB",
            depth=8,
            size_bytes=100000,
            has_transparency=False,
            unique_colors=50,
        )

        detection = ImageTypeDetection(
            detected_type="diagram", confidence=0.85, edge_density=0.35, color_variance=0.01, solid_region_ratio=0.8
        )

        rec = get_optimization_recommendation(info, detection)

        assert rec.format == "png"  # Lossless for diagrams
        assert rec.quality == 100
        assert rec.max_dimension is None  # Small image, no resize

    def test_transparency_preserved(self):
        info = ImageInfo(
            path="/test/icon.png",
            filename="icon.png",
            width=256,
            height=256,
            format="PNG",
            color_space="sRGB",
            depth=8,
            size_bytes=50000,
            has_transparency=True,  # Has alpha
            unique_colors=1000,
        )

        detection = ImageTypeDetection(
            detected_type="illustration", confidence=0.8, edge_density=0.2, color_variance=0.1, solid_region_ratio=0.5
        )

        rec = get_optimization_recommendation(info, detection)

        # Should not recommend JPEG for transparent images
        assert rec.format != "jpeg"


class TestFindImages:
    """Tests for image file discovery."""

    def test_find_single_image(self, tmp_path):
        # Create a test image file
        image_file = tmp_path / "test.jpg"
        image_file.write_bytes(b"fake jpeg data")

        found = find_images(image_file)

        assert len(found) == 1
        assert found[0] == image_file

    def test_find_images_in_directory(self, tmp_path):
        # Create multiple test image files
        (tmp_path / "image1.jpg").write_bytes(b"fake jpeg")
        (tmp_path / "image2.png").write_bytes(b"fake png")
        (tmp_path / "image3.webp").write_bytes(b"fake webp")
        (tmp_path / "document.txt").write_text("not an image")

        found = find_images(tmp_path)

        assert len(found) == 3
        names = {f.name for f in found}
        assert names == {"image1.jpg", "image2.png", "image3.webp"}

    def test_find_no_images(self, tmp_path):
        # Create only non-image files
        (tmp_path / "document.txt").write_text("text")
        (tmp_path / "data.json").write_text("{}")

        found = find_images(tmp_path)

        assert len(found) == 0

    def test_find_unsupported_format(self, tmp_path):
        # File with unsupported extension
        unsupported = tmp_path / "image.xyz"
        unsupported.write_bytes(b"unknown format")

        found = find_images(unsupported)

        assert len(found) == 0
