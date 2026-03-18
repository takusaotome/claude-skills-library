"""Tests for generate_qr.py QR code generation functionality."""

import csv
import json
from pathlib import Path

import pytest
from generate_qr import (
    generate_qr_code,
    generate_vcard,
    parse_color,
    process_batch_csv,
    process_batch_json,
)


class TestParseColor:
    """Tests for color parsing functionality."""

    def test_named_color_passthrough(self):
        """Named colors should pass through unchanged."""
        assert parse_color("black") == "black"
        assert parse_color("white") == "white"
        assert parse_color("red") == "red"

    def test_hex_color_passthrough(self):
        """Hex colors should pass through unchanged."""
        assert parse_color("#000000") == "#000000"
        assert parse_color("#FFFFFF") == "#FFFFFF"
        assert parse_color("#003366") == "#003366"

    def test_rgb_tuple_conversion(self):
        """RGB tuples should be converted to hex."""
        assert parse_color("rgb(0,0,0)") == "#000000"
        assert parse_color("rgb(255,255,255)") == "#ffffff"
        assert parse_color("rgb(0, 51, 102)") == "#003366"

    def test_invalid_rgb_passthrough(self):
        """Invalid RGB format should pass through unchanged."""
        assert parse_color("rgb(invalid)") == "rgb(invalid)"


class TestGenerateVcard:
    """Tests for vCard generation functionality."""

    def test_minimal_vcard(self):
        """vCard with only name should be valid."""
        vcard = generate_vcard(name="John Doe")
        assert "BEGIN:VCARD" in vcard
        assert "VERSION:3.0" in vcard
        assert "FN:John Doe" in vcard
        assert "N:Doe;John" in vcard
        assert "END:VCARD" in vcard

    def test_single_name(self):
        """vCard with single name (no last name) should work."""
        vcard = generate_vcard(name="Madonna")
        assert "FN:Madonna" in vcard
        assert "N:;Madonna" in vcard

    def test_full_vcard(self):
        """vCard with all fields should include all data."""
        vcard = generate_vcard(
            name="Jane Smith",
            phone="+1-555-1234",
            email="jane@example.com",
            org="Acme Corp",
            title="Engineer",
            url="https://example.com",
            address="123 Main St, City, ST 12345",
        )
        assert "TEL:+1-555-1234" in vcard
        assert "EMAIL:jane@example.com" in vcard
        assert "ORG:Acme Corp" in vcard
        assert "TITLE:Engineer" in vcard
        assert "URL:https://example.com" in vcard
        assert "ADR:;;123 Main St, City, ST 12345" in vcard

    def test_vcard_optional_fields_excluded(self):
        """vCard should not include lines for None fields."""
        vcard = generate_vcard(name="Test User", phone="+1-555-0000")
        assert "TEL:" in vcard
        assert "EMAIL:" not in vcard
        assert "ORG:" not in vcard


class TestGenerateQrCode:
    """Tests for QR code generation functionality."""

    def test_generate_simple_qr(self, tmp_path: Path):
        """Generate a simple QR code with default settings."""
        output_path = tmp_path / "test_qr.png"
        result = generate_qr_code(
            data="https://example.com",
            output_path=output_path,
        )

        assert output_path.exists()
        assert result["status"] == "success"
        assert result["path"] == str(output_path)
        assert result["version"] >= 1
        assert result["error_correction"] == "M"

    def test_generate_qr_custom_size(self, tmp_path: Path):
        """Generate QR code with custom box size."""
        output_path = tmp_path / "custom_size.png"
        result = generate_qr_code(
            data="Test data",
            output_path=output_path,
            box_size=20,
        )

        assert output_path.exists()
        assert result["box_size"] == 20
        # Larger box size should result in larger image
        assert result["image_size"][0] > 200

    def test_generate_qr_custom_colors(self, tmp_path: Path):
        """Generate QR code with custom colors."""
        output_path = tmp_path / "custom_color.png"
        result = generate_qr_code(
            data="Color test",
            output_path=output_path,
            fill_color="#003366",
            back_color="white",
        )

        assert output_path.exists()
        assert result["status"] == "success"

    def test_generate_qr_error_correction_levels(self, tmp_path: Path):
        """Test all error correction levels."""
        for level in ["L", "M", "Q", "H"]:
            output_path = tmp_path / f"ec_{level}.png"
            result = generate_qr_code(
                data="Error correction test",
                output_path=output_path,
                error_correction=level,
            )

            assert output_path.exists()
            assert result["error_correction"] == level

    def test_border_minimum_enforcement(self, tmp_path: Path):
        """Border below 4 should be adjusted to 4."""
        output_path = tmp_path / "min_border.png"
        result = generate_qr_code(
            data="Border test",
            output_path=output_path,
            border=2,  # Below minimum
        )

        assert output_path.exists()
        assert result["border"] == 4  # Should be adjusted

    def test_nested_output_directory(self, tmp_path: Path):
        """Output to nested directory should create parents."""
        output_path = tmp_path / "nested" / "deep" / "qr.png"
        result = generate_qr_code(
            data="Nested test",
            output_path=output_path,
        )

        assert output_path.exists()
        assert result["status"] == "success"

    def test_long_data_truncation_in_result(self, tmp_path: Path):
        """Long data should be truncated in result metadata."""
        long_data = "A" * 200
        output_path = tmp_path / "long_data.png"
        result = generate_qr_code(
            data=long_data,
            output_path=output_path,
        )

        assert output_path.exists()
        assert len(result["data"]) < 150  # Should be truncated
        assert result["data"].endswith("...")


class TestBatchProcessing:
    """Tests for batch QR code generation."""

    def test_batch_csv_processing(self, tmp_path: Path):
        """Process batch generation from CSV file."""
        # Create test CSV
        csv_path = tmp_path / "batch_input.csv"
        output_dir = tmp_path / "output"

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["data", "filename", "box_size"])
            writer.writeheader()
            writer.writerow({"data": "https://example1.com", "filename": "qr1.png", "box_size": "10"})
            writer.writerow({"data": "https://example2.com", "filename": "qr2.png", "box_size": "12"})

        defaults = {
            "box_size": 10,
            "border": 4,
            "fill_color": "black",
            "back_color": "white",
            "error_correction": "M",
        }

        results = process_batch_csv(csv_path, output_dir, defaults)

        assert len(results) == 2
        assert all(r["status"] == "success" for r in results)
        assert (output_dir / "qr1.png").exists()
        assert (output_dir / "qr2.png").exists()

    def test_batch_json_processing(self, tmp_path: Path):
        """Process batch generation from JSON file."""
        # Create test JSON
        json_path = tmp_path / "batch_input.json"
        output_dir = tmp_path / "output"

        batch_data = [
            {"data": "https://example1.com", "filename": "qr1.png"},
            {"data": "https://example2.com", "filename": "qr2.png", "box_size": 15},
        ]

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(batch_data, f)

        defaults = {
            "box_size": 10,
            "border": 4,
            "fill_color": "black",
            "back_color": "white",
            "error_correction": "M",
        }

        results = process_batch_json(json_path, output_dir, defaults)

        assert len(results) == 2
        assert all(r["status"] == "success" for r in results)
        assert (output_dir / "qr1.png").exists()
        assert (output_dir / "qr2.png").exists()

    def test_batch_csv_empty_data_handling(self, tmp_path: Path):
        """Batch processing should handle empty data gracefully."""
        csv_path = tmp_path / "batch_empty.csv"
        output_dir = tmp_path / "output"

        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["data", "filename"])
            writer.writeheader()
            writer.writerow({"data": "", "filename": "empty.png"})
            writer.writerow({"data": "https://valid.com", "filename": "valid.png"})

        defaults = {
            "box_size": 10,
            "border": 4,
            "fill_color": "black",
            "back_color": "white",
            "error_correction": "M",
        }

        results = process_batch_csv(csv_path, output_dir, defaults)

        assert len(results) == 2
        assert results[0]["status"] == "failed"
        assert results[1]["status"] == "success"

    def test_batch_json_default_filename(self, tmp_path: Path):
        """Batch items without filename should get auto-generated names."""
        json_path = tmp_path / "batch_no_filename.json"
        output_dir = tmp_path / "output"

        batch_data = [
            {"data": "https://example1.com"},
            {"data": "https://example2.com"},
        ]

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(batch_data, f)

        defaults = {
            "box_size": 10,
            "border": 4,
            "fill_color": "black",
            "back_color": "white",
            "error_correction": "M",
        }

        results = process_batch_json(json_path, output_dir, defaults)

        assert len(results) == 2
        assert all(r["status"] == "success" for r in results)
        # Should have auto-generated filenames
        assert (output_dir / "qr_0.png").exists()
        assert (output_dir / "qr_1.png").exists()
