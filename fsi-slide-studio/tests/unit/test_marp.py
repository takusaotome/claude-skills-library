"""Tests for converter/marp.py."""

import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from converter.marp import convert_marp_to_pdf, convert_marp_to_html, render_mermaid_to_png

SAMPLE_MARP = "---\nmarp: true\n---\n# Test Slide\nContent"
SAMPLE_MERMAID = "gantt\n    title Project\n    section A\n    Task1 :a1, 2024-01-01, 30d"


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

    @patch("converter.marp.Path.rename")
    @patch("converter.marp.subprocess.run")
    def test_saves_markdown_source_on_success(self, mock_run, mock_rename):
        mock_run.return_value = MagicMock(stderr="")
        result = convert_marp_to_pdf(SAMPLE_MARP, "test_pres")
        # rename should be called to save the .md file
        mock_rename.assert_called_once()
        rename_target = mock_rename.call_args[0][0]
        assert str(rename_target).endswith("test_pres.md")

    @patch("converter.marp.subprocess.run")
    def test_cleans_up_tmp_on_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, "marp")
        with pytest.raises(subprocess.CalledProcessError):
            convert_marp_to_pdf(SAMPLE_MARP, "test")
        # tmp file should be cleaned up (unlink called in except block)


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


class TestRenderMermaidToPng:
    @patch("converter.marp.shutil.which", return_value="/usr/local/bin/mmdc")
    @patch("converter.marp.subprocess.run")
    def test_returns_png_path(self, mock_run, mock_which):
        mock_run.return_value = MagicMock(stderr="")
        result = render_mermaid_to_png(SAMPLE_MERMAID, "gantt_chart")
        assert result.suffix == ".png"
        assert result.name == "gantt_chart.png"

    @patch("converter.marp.shutil.which", return_value="/usr/local/bin/mmdc")
    @patch("converter.marp.subprocess.run")
    def test_calls_mmdc_with_correct_args(self, mock_run, mock_which):
        mock_run.return_value = MagicMock(stderr="")
        render_mermaid_to_png(SAMPLE_MERMAID, "test")
        args = mock_run.call_args[0][0]
        assert args[0] == "/usr/local/bin/mmdc"
        assert "-i" in args
        assert "-o" in args
        assert "-w" in args
        assert "-b" in args

    @patch("converter.marp.shutil.which", return_value=None)
    def test_raises_when_mmdc_not_found(self, mock_which):
        with pytest.raises(RuntimeError, match="mmdc"):
            render_mermaid_to_png(SAMPLE_MERMAID, "test")

    @patch("converter.marp.shutil.which", return_value="/usr/local/bin/mmdc")
    @patch("converter.marp.subprocess.run")
    def test_raises_on_called_process_error(self, mock_run, mock_which):
        mock_run.side_effect = subprocess.CalledProcessError(1, "mmdc")
        with pytest.raises(subprocess.CalledProcessError):
            render_mermaid_to_png(SAMPLE_MERMAID, "test")

    @patch("converter.marp.shutil.which", return_value="/usr/local/bin/mmdc")
    @patch("converter.marp.subprocess.run")
    def test_strips_extension_from_filename(self, mock_run, mock_which):
        mock_run.return_value = MagicMock(stderr="")
        result = render_mermaid_to_png(SAMPLE_MERMAID, "chart.png")
        assert result.name == "chart.png"
