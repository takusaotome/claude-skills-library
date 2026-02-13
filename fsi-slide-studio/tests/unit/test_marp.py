"""Tests for converter/marp.py."""

import subprocess
from unittest.mock import patch, MagicMock

import pytest

from converter.marp import convert_marp_to_pdf, convert_marp_to_html

SAMPLE_MARP = "---\nmarp: true\n---\n# Test Slide\nContent"


class TestConvertMarpToPdf:
    @patch("converter.marp.subprocess.run")
    def test_returns_pdf_path(self, mock_run):
        mock_run.return_value = MagicMock(stderr="")
        result = convert_marp_to_pdf(SAMPLE_MARP, "test_pres")
        assert result.suffix == ".pdf"
        assert result.name == "test_pres.pdf"

    @patch("converter.marp.subprocess.run")
    def test_strips_extension_from_filename(self, mock_run):
        mock_run.return_value = MagicMock(stderr="")
        result = convert_marp_to_pdf(SAMPLE_MARP, "proposal.pdf")
        assert result.name == "proposal.pdf"

    @patch("converter.marp.subprocess.run")
    def test_calls_marp_with_pdf_flag(self, mock_run):
        mock_run.return_value = MagicMock(stderr="")
        convert_marp_to_pdf(SAMPLE_MARP, "test")
        args = mock_run.call_args[0][0]
        assert "--pdf" in args
        assert "--allow-local-files" in args
        assert "--html" in args

    @patch("converter.marp.subprocess.run")
    def test_raises_on_called_process_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "marp")
        with pytest.raises(subprocess.CalledProcessError):
            convert_marp_to_pdf(SAMPLE_MARP, "test")

    @patch("converter.marp.subprocess.run")
    def test_raises_on_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired("marp", 120)
        with pytest.raises(subprocess.TimeoutExpired):
            convert_marp_to_pdf(SAMPLE_MARP, "test")


class TestConvertMarpToHtml:
    @patch("converter.marp.subprocess.run")
    def test_returns_html_path(self, mock_run):
        mock_run.return_value = MagicMock(stderr="")
        result = convert_marp_to_html(SAMPLE_MARP, "preview")
        assert result.suffix == ".html"
        assert result.name == "preview.html"

    @patch("converter.marp.subprocess.run")
    def test_calls_marp_with_html_flag_no_pdf(self, mock_run):
        mock_run.return_value = MagicMock(stderr="")
        convert_marp_to_html(SAMPLE_MARP, "test")
        args = mock_run.call_args[0][0]
        assert "--html" in args
        assert "--allow-local-files" in args
        assert "--pdf" not in args

    @patch("converter.marp.subprocess.run")
    def test_strips_extension_from_filename(self, mock_run):
        mock_run.return_value = MagicMock(stderr="")
        result = convert_marp_to_html(SAMPLE_MARP, "presentation.html")
        assert result.name == "presentation.html"

    @patch("converter.marp.subprocess.run")
    def test_raises_on_called_process_error(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "marp")
        with pytest.raises(subprocess.CalledProcessError):
            convert_marp_to_html(SAMPLE_MARP, "test")

    @patch("converter.marp.subprocess.run")
    def test_timeout_is_120(self, mock_run):
        mock_run.return_value = MagicMock(stderr="")
        convert_marp_to_html(SAMPLE_MARP, "test")
        kwargs = mock_run.call_args[1]
        assert kwargs.get("timeout") == 120
