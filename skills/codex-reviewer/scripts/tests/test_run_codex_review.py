#!/usr/bin/env python3
"""Tests for run_codex_review.py"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from run_codex_review import (
    FOCUS_PROMPTS,
    PROFILES,
    REVIEW_PROMPTS,
    TYPE_MODEL_DEFAULTS,
    build_prompt,
    check_codex_installed,
    generate_output_filename,
    run_codex_review,
)


class TestBuildPrompt:
    """Tests for build_prompt function"""

    def test_code_review_prompt(self):
        prompt = build_prompt("code", "src/main.py")
        assert "src/main.py" in prompt
        assert "セキュリティ" in prompt
        assert "パフォーマンス" in prompt

    def test_document_review_prompt(self):
        prompt = build_prompt("document", "docs/spec.md")
        assert "docs/spec.md" in prompt
        assert "完全性" in prompt
        assert "正確性" in prompt

    def test_design_review_prompt(self):
        prompt = build_prompt("design", "design/architecture.md")
        assert "design/architecture.md" in prompt
        assert "アーキテクチャ" in prompt

    def test_test_review_prompt(self):
        prompt = build_prompt("test", "tests/")
        assert "tests/" in prompt
        assert "カバレッジ" in prompt

    def test_with_focus_areas(self):
        prompt = build_prompt("code", "src/", focus_areas=["security", "performance"])
        assert "OWASP" in prompt or "セキュリティ" in prompt
        assert "パフォーマンス" in prompt

    def test_custom_prompt(self):
        custom = "Review {target} for issues"
        prompt = build_prompt("code", "src/main.py", custom_prompt=custom)
        assert prompt == "Review src/main.py for issues"

    def test_custom_prompt_with_braces_in_code(self):
        # Ensure code snippets with {} don't crash
        custom = "Check code with dict = {} in {target}"
        prompt = build_prompt("code", "file.py", custom_prompt=custom)
        assert "file.py" in prompt


class TestGenerateOutputFilename:
    """Tests for generate_output_filename function"""

    def test_file_target(self):
        filename = generate_output_filename("code", "src/main.py", "./reviews")
        assert "code_review_main_" in filename
        assert filename.endswith(".md")
        assert filename.startswith("reviews/")

    def test_directory_target(self):
        filename = generate_output_filename("code", "src/", "./reviews")
        assert "code_review_src_" in filename

    def test_different_review_types(self):
        for review_type in ["code", "document", "design", "test"]:
            filename = generate_output_filename(review_type, "target", "./out")
            assert f"{review_type}_review_" in filename


class TestCheckCodexInstalled:
    """Tests for check_codex_installed function"""

    @patch("run_codex_review.subprocess.run")
    def test_codex_installed(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        assert check_codex_installed() is True

    @patch("run_codex_review.subprocess.run")
    def test_codex_not_installed_returncode(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1)
        assert check_codex_installed() is False

    @patch("run_codex_review.subprocess.run")
    def test_codex_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        assert check_codex_installed() is False


class TestProfiles:
    """Tests for profile configurations"""

    def test_profiles_exist(self):
        assert "deep-review" in PROFILES
        assert "quick-review" in PROFILES

    def test_deep_review_profile(self):
        profile = PROFILES["deep-review"]
        assert profile["model"] == "gpt-5.4"
        assert profile["reasoning"] == "high"

    def test_quick_review_profile(self):
        profile = PROFILES["quick-review"]
        assert profile["model"] == "gpt-5.4"
        assert profile["reasoning"] == "medium"


class TestTypeModelDefaults:
    """Tests for type-specific model defaults"""

    def test_code_defaults(self):
        config = TYPE_MODEL_DEFAULTS["code"]
        assert config["model"] == "gpt-5.4"
        assert config["reasoning"] == "high"

    def test_document_defaults(self):
        config = TYPE_MODEL_DEFAULTS["document"]
        assert config["model"] == "gpt-5.4"
        assert config["reasoning"] == "high"

    def test_design_defaults(self):
        config = TYPE_MODEL_DEFAULTS["design"]
        assert config["model"] == "gpt-5.4"

    def test_test_defaults(self):
        config = TYPE_MODEL_DEFAULTS["test"]
        assert config["model"] == "gpt-5.4"


class TestReviewPrompts:
    """Tests for review prompts"""

    def test_all_types_have_prompts(self):
        for review_type in ["code", "document", "design", "test"]:
            assert review_type in REVIEW_PROMPTS
            assert "{target}" in REVIEW_PROMPTS[review_type]

    def test_focus_prompts_exist(self):
        expected_focuses = [
            "security",
            "performance",
            "maintainability",
            "completeness",
            "accuracy",
            "clarity",
            "architecture",
            "scalability",
            "patterns",
            "coverage",
            "edge-cases",
            "quality",
        ]
        for focus in expected_focuses:
            assert focus in FOCUS_PROMPTS


class TestRunCodexReview:
    """Tests for run_codex_review function"""

    @patch("run_codex_review.subprocess.run")
    def test_stdin_devnull(self, mock_run, tmp_path):
        """Ensure subprocess.run is called with stdin=DEVNULL to prevent stdin reading"""
        mock_run.return_value = MagicMock(returncode=0)
        output_dir = str(tmp_path / "reviews")
        # Create a fake output file so validation passes
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        def side_effect(*args, **kwargs):
            # Create the output file that would normally be created by codex
            for arg in args[0]:
                if arg == "-o":
                    idx = args[0].index("-o")
                    output_file = args[0][idx + 1]
                    Path(output_file).write_text("Review content")
                    break
            return MagicMock(returncode=0)

        mock_run.side_effect = side_effect

        run_codex_review("code", "src/main.py", output_dir)
        _, kwargs = mock_run.call_args
        assert kwargs.get("stdin") == subprocess.DEVNULL

    @patch("run_codex_review.subprocess.run")
    def test_empty_output_file_detected(self, mock_run, tmp_path):
        """Ensure empty output file is detected as failure"""
        output_dir = str(tmp_path / "reviews")
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        def side_effect(*args, **kwargs):
            # Create empty output file (simulates codex error with exitcode=0)
            for i, arg in enumerate(args[0]):
                if arg == "-o":
                    output_file = args[0][i + 1]
                    Path(output_file).write_text("")
                    break
            return MagicMock(returncode=0, stderr="", stdout="")

        mock_run.side_effect = side_effect

        success, result = run_codex_review("code", "src/main.py", output_dir)
        assert success is False
        assert "空" in result or "empty" in result.lower()

    @patch("run_codex_review.subprocess.run")
    def test_default_model_is_gpt54(self, mock_run, tmp_path):
        """Ensure default model is gpt-5.4 for all review types"""
        output_dir = str(tmp_path / "reviews")
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        def side_effect(*args, **kwargs):
            for i, arg in enumerate(args[0]):
                if arg == "-o":
                    Path(args[0][i + 1]).write_text("Review content")
                    break
            return MagicMock(returncode=0)

        mock_run.side_effect = side_effect

        for review_type in ["code", "document", "design", "test"]:
            run_codex_review(review_type, "target", output_dir)
            cmd = mock_run.call_args[0][0]
            model_idx = cmd.index("--model")
            assert cmd[model_idx + 1] == "gpt-5.4", f"Expected gpt-5.4 for {review_type}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
