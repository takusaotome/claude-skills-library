"""
Tests for design_log.py - Design decision tracking functionality.
"""

import argparse
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from design_log import (
    SCHEMA_VERSION,
    VALID_CATEGORIES,
    cmd_apply,
    cmd_history,
    cmd_init,
    cmd_query,
    cmd_record,
    cmd_resolve,
    cmd_search,
    cmd_token,
    generate_id,
    get_timestamp,
    load_log,
    save_log,
)


class TestLoadSaveLog:
    """Tests for log file I/O operations."""

    def test_load_nonexistent_returns_empty(self, tmp_path: Path):
        """Loading a non-existent file returns empty dict."""
        log_path = tmp_path / "nonexistent.json"
        result = load_log(log_path)
        assert result == {}

    def test_save_and_load_roundtrip(self, tmp_path: Path):
        """Data saved can be loaded back identically."""
        log_path = tmp_path / "test.json"
        data = {
            "schema_version": "1.0",
            "session": {"id": "test_001"},
            "decisions": [],
        }
        save_log(log_path, data)
        loaded = load_log(log_path)
        assert loaded == data

    def test_save_preserves_unicode(self, tmp_path: Path):
        """Unicode characters (Japanese) are preserved."""
        log_path = tmp_path / "unicode.json"
        data = {
            "session": {"name": "テストセッション"},
            "decisions": [{"reason": "日本語の理由"}],
        }
        save_log(log_path, data)
        loaded = load_log(log_path)
        assert loaded["session"]["name"] == "テストセッション"
        assert loaded["decisions"][0]["reason"] == "日本語の理由"


class TestGenerateId:
    """Tests for ID generation."""

    def test_generate_id_has_prefix(self):
        """Generated IDs have the correct prefix."""
        session_id = generate_id("session")
        assert session_id.startswith("session_")

        dec_id = generate_id("dec")
        assert dec_id.startswith("dec_")

    def test_generate_id_unique(self):
        """Generated IDs are unique."""
        ids = [generate_id("test") for _ in range(100)]
        assert len(ids) == len(set(ids))


class TestGetTimestamp:
    """Tests for timestamp generation."""

    def test_timestamp_format(self):
        """Timestamp is in ISO format."""
        ts = get_timestamp()
        # Should be parseable as ISO format
        assert "T" in ts
        assert ts.endswith("+00:00") or ts.endswith("Z")


class TestCmdInit:
    """Tests for the init command."""

    def test_init_creates_log_file(self, tmp_path: Path):
        """Init creates a new log file."""
        log_path = tmp_path / ".design-log.json"
        args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test Session",
            force=False,
        )
        result = cmd_init(args)
        assert result == 0
        assert log_path.exists()

        data = load_log(log_path)
        assert data["schema_version"] == SCHEMA_VERSION
        assert data["session"]["name"] == "Test Session"
        assert data["session"]["document"] == "test.pptx"

    def test_init_fails_if_exists_without_force(self, tmp_path: Path):
        """Init fails if log exists and force not set."""
        log_path = tmp_path / ".design-log.json"
        log_path.write_text("{}")

        args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        result = cmd_init(args)
        assert result == 1

    def test_init_overwrites_with_force(self, tmp_path: Path):
        """Init overwrites existing file with --force."""
        log_path = tmp_path / ".design-log.json"
        log_path.write_text('{"old": "data"}')

        args = argparse.Namespace(
            log_file=str(log_path),
            document="new.pptx",
            session_name="New Session",
            force=True,
        )
        result = cmd_init(args)
        assert result == 0

        data = load_log(log_path)
        assert "old" not in data
        assert data["session"]["document"] == "new.pptx"


class TestCmdRecord:
    """Tests for the record command."""

    def test_record_adds_decision(self, tmp_path: Path):
        """Record adds a new decision to the log."""
        log_path = tmp_path / ".design-log.json"

        # Initialize first
        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        # Record a decision
        record_args = argparse.Namespace(
            log_file=str(log_path),
            category="color",
            element="header-bg",
            old_value="#FFFFFF",
            new_value="#003366",
            reason="Corporate blue",
            reference="slide-1",
        )
        result = cmd_record(record_args)
        assert result == 0

        data = load_log(log_path)
        assert len(data["decisions"]) == 1
        dec = data["decisions"][0]
        assert dec["category"] == "color"
        assert dec["element"] == "header-bg"
        assert dec["new_value"] == "#003366"

    def test_record_fails_without_session(self, tmp_path: Path):
        """Record fails if no session exists."""
        log_path = tmp_path / "nonexistent.json"
        args = argparse.Namespace(
            log_file=str(log_path),
            category="color",
            element="test",
            old_value="a",
            new_value="b",
            reason="",
            reference="",
        )
        result = cmd_record(args)
        assert result == 1

    def test_record_fails_with_invalid_category(self, tmp_path: Path):
        """Record fails with invalid category."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        record_args = argparse.Namespace(
            log_file=str(log_path),
            category="invalid",
            element="test",
            old_value="a",
            new_value="b",
            reason="",
            reference="",
        )
        result = cmd_record(record_args)
        assert result == 1


class TestCmdQuery:
    """Tests for the query command."""

    def test_query_returns_decisions(self, tmp_path: Path, capsys):
        """Query returns matching decisions."""
        log_path = tmp_path / ".design-log.json"

        # Setup
        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        # Add decisions
        for i in range(3):
            record_args = argparse.Namespace(
                log_file=str(log_path),
                category="color",
                element=f"element-{i}",
                old_value="#000",
                new_value=f"#00{i}",
                reason=f"Reason {i}",
                reference="",
            )
            cmd_record(record_args)

        # Query
        query_args = argparse.Namespace(
            log_file=str(log_path),
            category="color",
            limit=10,
        )
        result = cmd_query(query_args)
        assert result == 0

        captured = capsys.readouterr()
        assert "Found 3 decision(s)" in captured.out

    def test_query_filters_by_category(self, tmp_path: Path, capsys):
        """Query filters by category."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        # Add color decision
        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="color",
                element="color-elem",
                old_value="",
                new_value="#000",
                reason="",
                reference="",
            )
        )

        # Add typography decision
        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="typography",
                element="typo-elem",
                old_value="",
                new_value="14pt",
                reason="",
                reference="",
            )
        )

        # Query color only
        query_args = argparse.Namespace(
            log_file=str(log_path),
            category="color",
            limit=10,
        )
        result = cmd_query(query_args)
        assert result == 0

        captured = capsys.readouterr()
        assert "Found 1 decision(s)" in captured.out
        assert "color-elem" in captured.out


class TestCmdSearch:
    """Tests for the search command."""

    def test_search_by_keyword(self, tmp_path: Path, capsys):
        """Search finds decisions by keyword."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="color",
                element="corporate-header",
                old_value="",
                new_value="#003366",
                reason="Brand guidelines",
                reference="",
            )
        )

        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="typography",
                element="body-text",
                old_value="",
                new_value="14pt",
                reason="Readability",
                reference="",
            )
        )

        # Search for "corporate"
        search_args = argparse.Namespace(
            log_file=str(log_path),
            keyword="corporate",
            limit=10,
        )
        result = cmd_search(search_args)
        assert result == 0

        captured = capsys.readouterr()
        assert "Found 1 decision(s)" in captured.out
        assert "corporate-header" in captured.out


class TestCmdApply:
    """Tests for the apply command."""

    def test_apply_creates_new_decision(self, tmp_path: Path, capsys):
        """Apply creates a new decision referencing the source."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        # Record source decision
        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="color",
                element="header-1",
                old_value="#FFF",
                new_value="#003366",
                reason="Corporate blue",
                reference="",
            )
        )

        # Get the decision ID
        data = load_log(log_path)
        source_id = data["decisions"][0]["id"]

        # Apply to new element
        apply_args = argparse.Namespace(
            log_file=str(log_path),
            decision_id=source_id,
            target_element="header-2",
            context="Same styling",
        )
        result = cmd_apply(apply_args)
        assert result == 0

        # Check that new decision was created
        data = load_log(log_path)
        assert len(data["decisions"]) == 2
        new_dec = data["decisions"][1]
        assert new_dec["element"] == "header-2"
        assert new_dec["new_value"] == "#003366"
        assert new_dec["reference"] == source_id


class TestCmdToken:
    """Tests for the token command."""

    def test_token_set_and_get(self, tmp_path: Path, capsys):
        """Token set and get work correctly."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        # Set token
        set_args = argparse.Namespace(
            log_file=str(log_path),
            action="set",
            category="color",
            name="primary",
            value="#003366",
        )
        result = cmd_token(set_args)
        assert result == 0

        # Get token
        get_args = argparse.Namespace(
            log_file=str(log_path),
            action="get",
            category="color",
            name="primary",
            value=None,
        )
        result = cmd_token(get_args)
        assert result == 0

        captured = capsys.readouterr()
        assert "color.primary = #003366" in captured.out


class TestCmdResolve:
    """Tests for the resolve command."""

    def test_resolve_color_reference(self, tmp_path: Path, capsys):
        """Resolve finds color decisions from contextual reference."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="color",
                element="header",
                old_value="#FFF",
                new_value="#003366",
                reason="Blue header",
                reference="",
            )
        )

        # Resolve Japanese reference
        resolve_args = argparse.Namespace(
            log_file=str(log_path),
            reference="前回の色",
            limit=3,
        )
        result = cmd_resolve(resolve_args)
        assert result == 0

        captured = capsys.readouterr()
        assert "Detected category: color" in captured.out
        assert "#003366" in captured.out

    def test_resolve_typography_reference(self, tmp_path: Path, capsys):
        """Resolve finds typography decisions."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="typography",
                element="body",
                old_value="12pt",
                new_value="14pt",
                reason="Better readability",
                reference="",
            )
        )

        resolve_args = argparse.Namespace(
            log_file=str(log_path),
            reference="さっきのフォント",
            limit=3,
        )
        result = cmd_resolve(resolve_args)
        assert result == 0

        captured = capsys.readouterr()
        assert "Detected category: typography" in captured.out


class TestCmdHistory:
    """Tests for the history command."""

    def test_history_markdown_output(self, tmp_path: Path, capsys):
        """History generates markdown report."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test Session",
            force=False,
        )
        cmd_init(init_args)

        cmd_record(
            argparse.Namespace(
                log_file=str(log_path),
                category="color",
                element="header",
                old_value="#FFF",
                new_value="#003366",
                reason="Brand color",
                reference="",
            )
        )

        history_args = argparse.Namespace(
            log_file=str(log_path),
            format="markdown",
            output=None,
        )
        result = cmd_history(history_args)
        assert result == 0

        captured = capsys.readouterr()
        assert "# Design History: Test Session" in captured.out
        assert "**Document**: test.pptx" in captured.out
        assert "Color Change" in captured.out

    def test_history_json_output(self, tmp_path: Path, capsys):
        """History generates JSON output."""
        log_path = tmp_path / ".design-log.json"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        history_args = argparse.Namespace(
            log_file=str(log_path),
            format="json",
            output=None,
        )
        result = cmd_history(history_args)
        assert result == 0

        captured = capsys.readouterr()
        # Should be valid JSON
        data = json.loads(captured.out)
        assert data["schema_version"] == SCHEMA_VERSION

    def test_history_writes_to_file(self, tmp_path: Path):
        """History writes to output file."""
        log_path = tmp_path / ".design-log.json"
        output_path = tmp_path / "history.md"

        init_args = argparse.Namespace(
            log_file=str(log_path),
            document="test.pptx",
            session_name="Test",
            force=False,
        )
        cmd_init(init_args)

        history_args = argparse.Namespace(
            log_file=str(log_path),
            format="markdown",
            output=str(output_path),
        )
        result = cmd_history(history_args)
        assert result == 0
        assert output_path.exists()

        content = output_path.read_text()
        assert "# Design History" in content
