#!/usr/bin/env python3
"""
Pytest configuration and fixtures for multi-format-document-optimizer tests.
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

import pytest


@pytest.fixture
def sample_pdf_content():
    """Sample PDF-like content for testing."""
    return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\ntrailer\n<< /Root 1 0 R >>\n%%EOF"


@pytest.fixture
def sample_markdown_content():
    """Sample Markdown content for testing."""
    return """---
title: Test Document
---

# Test Document

## Introduction

This is a test document with some content.

- Item 1
- Item 2
- Item 3

## Table

| Column A | Column B |
|----------|----------|
| Value 1  | Value 2  |
"""


@pytest.fixture
def sample_image_path(tmp_path):
    """Create a sample test image."""
    # Create a simple 1x1 pixel PNG (minimal valid PNG)
    png_header = bytes(
        [
            0x89,
            0x50,
            0x4E,
            0x47,
            0x0D,
            0x0A,
            0x1A,
            0x0A,  # PNG signature
            0x00,
            0x00,
            0x00,
            0x0D,  # IHDR chunk length
            0x49,
            0x48,
            0x44,
            0x52,  # IHDR
            0x00,
            0x00,
            0x00,
            0x01,  # width = 1
            0x00,
            0x00,
            0x00,
            0x01,  # height = 1
            0x08,
            0x02,  # bit depth = 8, color type = 2 (RGB)
            0x00,
            0x00,
            0x00,  # compression, filter, interlace
            0x90,
            0x77,
            0x53,
            0xDE,  # CRC
            0x00,
            0x00,
            0x00,
            0x0C,  # IDAT chunk length
            0x49,
            0x44,
            0x41,
            0x54,  # IDAT
            0x08,
            0xD7,
            0x63,
            0xF8,
            0xFF,
            0xFF,
            0xFF,
            0x00,  # compressed data
            0x05,
            0xFE,
            0x02,
            0xFE,  # CRC
            0x00,
            0x00,
            0x00,
            0x00,  # IEND chunk length
            0x49,
            0x45,
            0x4E,
            0x44,  # IEND
            0xAE,
            0x42,
            0x60,
            0x82,  # CRC
        ]
    )

    img_path = tmp_path / "test_image.png"
    with open(img_path, "wb") as f:
        f.write(png_header)

    return img_path


@pytest.fixture
def sample_docx_path(tmp_path):
    """Create a placeholder DOCX file path (not a valid DOCX)."""
    docx_path = tmp_path / "test_document.docx"
    # Write minimal content to create the file
    with open(docx_path, "wb") as f:
        f.write(b"PK\x03\x04")  # ZIP magic number (DOCX is a ZIP)
    return docx_path


@pytest.fixture
def output_dir(tmp_path):
    """Create an output directory for test results."""
    output = tmp_path / "output"
    output.mkdir()
    return output
