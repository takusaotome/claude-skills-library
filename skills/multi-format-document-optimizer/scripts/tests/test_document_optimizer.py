#!/usr/bin/env python3
"""
Tests for document_optimizer.py

Tests cover:
- Format detection
- Preset configurations
- Document analysis
- Image optimization (when ImageMagick available)
- Conversion pipelines
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from document_optimizer import (
    ConversionResult,
    DocumentAnalysis,
    DocumentOptimizer,
    PresetConfig,
    QualityPreset,
)


class TestQualityPreset:
    """Tests for quality preset configurations."""

    def test_web_preset_values(self):
        """Test web preset has correct default values."""
        config = PresetConfig.from_preset(QualityPreset.WEB)
        assert config.name == "web"
        assert config.image_quality == 80
        assert config.image_dpi == 96
        assert config.image_format == "webp"
        assert config.max_width == 1920
        assert config.max_height == 1080
        assert config.strip_metadata is True

    def test_print_preset_values(self):
        """Test print preset has correct default values."""
        config = PresetConfig.from_preset(QualityPreset.PRINT)
        assert config.name == "print"
        assert config.image_quality == 95
        assert config.image_dpi == 300
        assert config.image_format == "jpeg"
        assert config.max_width == 0  # No limit
        assert config.max_height == 0
        assert config.strip_metadata is False

    def test_archive_preset_values(self):
        """Test archive preset has correct default values."""
        config = PresetConfig.from_preset(QualityPreset.ARCHIVE)
        assert config.name == "archive"
        assert config.image_quality == 90
        assert config.image_dpi == 150
        assert config.max_width == 2400
        assert config.max_height == 2400

    def test_minimal_preset_values(self):
        """Test minimal preset has correct default values."""
        config = PresetConfig.from_preset(QualityPreset.MINIMAL)
        assert config.name == "minimal"
        assert config.image_quality == 70
        assert config.image_dpi == 72
        assert config.image_format == "webp"
        assert config.max_width == 1280
        assert config.max_height == 720
        assert config.strip_metadata is True

    def test_custom_preset_defaults_to_web(self):
        """Test that custom preset falls back to web config."""
        config = PresetConfig.from_preset(QualityPreset.CUSTOM)
        assert config.image_quality == 80  # Same as web


class TestDocumentAnalysis:
    """Tests for DocumentAnalysis data class."""

    def test_analysis_to_json(self):
        """Test JSON serialization of analysis."""
        analysis = DocumentAnalysis(
            input_file="/path/to/test.pdf",
            format="pdf",
            page_count=10,
            file_size_bytes=1048576,
            images={"count": 5, "total_bytes": 500000},
            recommended_pipeline="pdf_optimize",
            recommended_preset="web",
        )

        json_str = analysis.to_json()
        parsed = json.loads(json_str)

        assert parsed["input_file"] == "/path/to/test.pdf"
        assert parsed["format"] == "pdf"
        assert parsed["page_count"] == 10
        assert parsed["file_size_bytes"] == 1048576
        assert parsed["images"]["count"] == 5
        assert parsed["schema_version"] == "1.0"


class TestConversionResult:
    """Tests for ConversionResult data class."""

    def test_result_to_json(self):
        """Test JSON serialization of conversion result."""
        result = ConversionResult(
            input_file="/path/to/input.pdf",
            output_file="/path/to/output.pdf",
            pipeline="pdf_optimize",
            preset="web",
            input_size_bytes=2000000,
            output_size_bytes=500000,
            compression_ratio=0.25,
            images_processed=8,
            processing_time_seconds=5.5,
            status="success",
        )

        json_str = result.to_json()
        parsed = json.loads(json_str)

        assert parsed["pipeline"] == "pdf_optimize"
        assert parsed["compression_ratio"] == 0.25
        assert parsed["images_processed"] == 8
        assert parsed["status"] == "success"


class TestDocumentOptimizer:
    """Tests for DocumentOptimizer class."""

    def test_detect_format_pdf(self, tmp_path):
        """Test PDF format detection."""
        optimizer = DocumentOptimizer()
        pdf_path = tmp_path / "test.pdf"
        pdf_path.touch()

        assert optimizer.detect_format(pdf_path) == "pdf"

    def test_detect_format_docx(self, tmp_path):
        """Test DOCX format detection."""
        optimizer = DocumentOptimizer()
        docx_path = tmp_path / "test.docx"
        docx_path.touch()

        assert optimizer.detect_format(docx_path) == "docx"

    def test_detect_format_image(self, tmp_path):
        """Test image format detection."""
        optimizer = DocumentOptimizer()

        for ext in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".tiff"]:
            img_path = tmp_path / f"test{ext}"
            img_path.touch()
            assert optimizer.detect_format(img_path) == "image"

    def test_detect_format_unknown(self, tmp_path):
        """Test unknown format detection."""
        optimizer = DocumentOptimizer()
        unknown_path = tmp_path / "test.xyz"
        unknown_path.touch()

        assert optimizer.detect_format(unknown_path) == "unknown"

    def test_analyze_nonexistent_file(self):
        """Test analysis of non-existent file raises error."""
        optimizer = DocumentOptimizer()
        with pytest.raises(FileNotFoundError):
            optimizer.analyze(Path("/nonexistent/file.pdf"))

    def test_analyze_image(self, sample_image_path):
        """Test analysis of image file."""
        optimizer = DocumentOptimizer()
        analysis = optimizer.analyze(sample_image_path)

        assert analysis.format == "image"
        assert analysis.page_count == 1
        assert analysis.recommended_pipeline == "images_to_pdf"
        assert analysis.recommended_preset == "web"

    def test_verify_nonexistent_file(self, tmp_path):
        """Test verify returns error for non-existent file."""
        optimizer = DocumentOptimizer()
        result = optimizer.verify(tmp_path / "nonexistent.pdf")

        assert result["status"] == "error"
        assert "not found" in result["message"].lower()

    def test_verbose_logging(self, capsys):
        """Test verbose logging is suppressed when verbose=False."""
        optimizer = DocumentOptimizer(verbose=False)
        optimizer._log("Test message")

        captured = capsys.readouterr()
        assert "Test message" not in captured.err

    def test_verbose_logging_enabled(self, capsys):
        """Test verbose logging when verbose=True."""
        optimizer = DocumentOptimizer(verbose=True)
        optimizer._log("Test message")

        captured = capsys.readouterr()
        assert "Test message" in captured.err


class TestImageOptimization:
    """Tests for image optimization functionality."""

    def test_optimize_image_without_imagemagick(self, sample_image_path, tmp_path):
        """Test image optimization fallback when ImageMagick not available."""
        optimizer = DocumentOptimizer()
        optimizer.has_imagemagick = False

        config = PresetConfig.from_preset(QualityPreset.WEB)
        output_path = tmp_path / "output.png"

        result = optimizer.optimize_image(sample_image_path, output_path, config)

        assert result is True
        assert output_path.exists()

    @patch("subprocess.run")
    def test_optimize_image_with_imagemagick(self, mock_run, sample_image_path, tmp_path):
        """Test image optimization with ImageMagick."""
        mock_run.return_value = MagicMock(returncode=0)

        optimizer = DocumentOptimizer()
        optimizer.has_imagemagick = True

        config = PresetConfig.from_preset(QualityPreset.WEB)
        output_path = tmp_path / "output.webp"

        # Create the expected output file
        expected_output = output_path.with_suffix(".webp")
        expected_output.touch()

        result = optimizer.optimize_image(sample_image_path, output_path, config)

        assert result is True
        assert mock_run.called

    @patch("subprocess.run")
    def test_optimize_image_imagemagick_failure(self, mock_run, sample_image_path, tmp_path):
        """Test image optimization handles ImageMagick failure."""
        mock_run.return_value = MagicMock(returncode=1, stderr="Error")

        optimizer = DocumentOptimizer()
        optimizer.has_imagemagick = True

        config = PresetConfig.from_preset(QualityPreset.WEB)
        output_path = tmp_path / "output.webp"

        result = optimizer.optimize_image(sample_image_path, output_path, config)

        assert result is False


class TestBatchProcessing:
    """Tests for batch processing functionality."""

    def test_batch_creates_output_dir(self, tmp_path):
        """Test batch processing creates output directory."""
        optimizer = DocumentOptimizer()
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output" / "nested"

        optimizer.batch(input_dir, output_dir)

        assert output_dir.exists()

    def test_batch_empty_directory(self, tmp_path):
        """Test batch processing of empty directory."""
        optimizer = DocumentOptimizer()
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"

        results = optimizer.batch(input_dir, output_dir)

        assert results == []

    def test_batch_skip_existing(self, tmp_path, sample_image_path):
        """Test batch processing skips existing files."""
        optimizer = DocumentOptimizer()
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Copy sample image to input
        import shutil

        shutil.copy(sample_image_path, input_dir / "test.png")

        # Create existing output
        (output_dir / "test.pdf").touch()

        results = optimizer.batch(input_dir, output_dir, pattern="*.png", skip_existing=True)

        assert len(results) == 0
