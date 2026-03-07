"""Tests for mine_session_logs.py."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def mine_module():
    """Load mine_session_logs.py as a module."""
    script_path = Path(__file__).resolve().parents[1] / "mine_session_logs.py"
    spec = importlib.util.spec_from_file_location("mine_session_logs", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to load mine_session_logs.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


# ── find_project_dirs ──


def test_find_project_dirs(mine_module, tmp_path: Path):
    """When allowlist is provided, filter by suffix match and return (encoded_name, path)."""
    base = tmp_path / "projects"
    base.mkdir()

    (base / "-Users-alice-PycharmProjects-claude-skills-library").mkdir()
    (base / "-Users-bob-Code-trade-edge-finder").mkdir()
    (base / "-Users-carol-Projects-unrelated-project").mkdir()

    allowlist = ["claude-skills-library", "trade-edge-finder"]
    result = mine_module.find_project_dirs(base, allowlist)

    assert len(result) == 2
    # Returns (encoded_name, path) tuples
    encoded_names = [name for name, _ in result]
    assert "-Users-alice-PycharmProjects-claude-skills-library" in encoded_names
    assert "-Users-bob-Code-trade-edge-finder" in encoded_names


def test_find_project_dirs_no_match(mine_module, tmp_path: Path):
    """No matching dirs returns empty list."""
    base = tmp_path / "projects"
    base.mkdir()
    (base / "-Users-alice-Projects-something-else").mkdir()

    result = mine_module.find_project_dirs(base, ["claude-skills-library"])
    assert result == []


def test_find_project_dirs_no_allowlist(mine_module, tmp_path: Path):
    """allowlist=None returns all dirs as (encoded_name, path)."""
    base = tmp_path / "projects"
    base.mkdir()

    (base / "-Users-alice-PycharmProjects-project-a").mkdir()
    (base / "-Users-bob-Code-project-b").mkdir()
    (base / "some-file.txt").write_text("not a dir")

    result = mine_module.find_project_dirs(base, allowlist=None)

    assert len(result) == 2
    encoded_names = [name for name, _ in result]
    assert "-Users-alice-PycharmProjects-project-a" in encoded_names
    assert "-Users-bob-Code-project-b" in encoded_names


def test_find_project_dirs_with_allowlist(mine_module, tmp_path: Path):
    """allowlist filters by suffix match."""
    base = tmp_path / "projects"
    base.mkdir()

    (base / "-Users-alice-PycharmProjects-my-project").mkdir()
    (base / "-Users-bob-Code-other-project").mkdir()

    result = mine_module.find_project_dirs(base, allowlist=["my-project"])

    assert len(result) == 1
    assert result[0][0] == "-Users-alice-PycharmProjects-my-project"


# ── sanitize_project_name ──


def test_sanitize_project_name(mine_module):
    """-Users-taku-PycharmProjects-my-project -> PycharmProjects-my-project."""
    result = mine_module.sanitize_project_name("-Users-taku-PycharmProjects-my-project")
    assert result == "PycharmProjects-my-project"


def test_sanitize_project_name_double_dash(mine_module):
    """-Users-foo--claude-plans -> claude-plans."""
    result = mine_module.sanitize_project_name("-Users-foo--claude-plans")
    assert result == "claude-plans"


def test_sanitize_project_name_no_match(mine_module):
    """Non-matching name returned as-is."""
    result = mine_module.sanitize_project_name("simple-project")
    assert result == "simple-project"


# ── parse_projects_arg ──


def test_parse_projects_cli_arg(mine_module):
    """ "proj1, proj2, ,proj3" -> ["proj1", "proj2", "proj3"]."""
    result = mine_module.parse_projects_arg("proj1, proj2, ,proj3")
    assert result == ["proj1", "proj2", "proj3"]


# ── list_session_logs ──


def test_list_session_logs_date_filter(mine_module, tmp_path: Path):
    """Create files with recent and old mtime, verify filter."""
    proj_dir = tmp_path / "proj"
    proj_dir.mkdir()

    recent = proj_dir / "recent_session.jsonl"
    recent.write_text('{"type":"user"}\n')

    old = proj_dir / "old_session.jsonl"
    old.write_text('{"type":"user"}\n')
    old_time = time.time() - (30 * 86400)
    os.utime(old, (old_time, old_time))

    project_dirs = [("test-project", proj_dir)]
    result = mine_module.list_session_logs(project_dirs, lookback_days=7)

    assert len(result) == 1
    assert result[0][0] == "test-project"
    assert result[0][1].name == "recent_session.jsonl"


# ── parse_session ──


def test_parse_user_messages_str(mine_module, tmp_path: Path):
    """Parse JSONL with string content format."""
    log = tmp_path / "session.jsonl"
    lines = [
        json.dumps(
            {
                "type": "user",
                "message": {"type": "user", "content": "Analyze AAPL"},
                "userType": "external",
                "timestamp": "2026-02-28T10:00:00+00:00",
            }
        ),
        json.dumps(
            {
                "type": "user",
                "message": {"type": "user", "content": "Check breadth"},
                "userType": "external",
                "timestamp": "2026-02-28T10:01:00+00:00",
            }
        ),
    ]
    log.write_text("\n".join(lines))

    result = mine_module.parse_session(log)
    assert len(result["user_messages"]) == 2
    assert result["user_messages"][0] == "Analyze AAPL"
    assert result["user_messages"][1] == "Check breadth"


def test_parse_user_messages_list(mine_module, tmp_path: Path):
    """Parse JSONL with list[{type,text}] content format."""
    log = tmp_path / "session.jsonl"
    lines = [
        json.dumps(
            {
                "type": "user",
                "message": {
                    "type": "user",
                    "content": [
                        {"type": "text", "text": "Create a new skill"},
                        {"type": "text", "text": "for dividend analysis"},
                    ],
                },
                "userType": "external",
                "timestamp": "2026-02-28T10:00:00+00:00",
            }
        ),
    ]
    log.write_text("\n".join(lines))

    result = mine_module.parse_session(log)
    assert len(result["user_messages"]) == 2
    assert result["user_messages"][0] == "Create a new skill"
    assert result["user_messages"][1] == "for dividend analysis"


def test_parse_tool_usage(mine_module, tmp_path: Path):
    """Extract tool_use blocks from assistant messages."""
    log = tmp_path / "session.jsonl"
    lines = [
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "type": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Bash",
                            "input": {"command": "python3 skills/pead-screener/scripts/screen_pead.py"},
                        },
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {"file_path": "/tmp/report.md"},
                        },
                    ],
                },
                "timestamp": "2026-02-28T10:00:00+00:00",
            }
        ),
    ]
    log.write_text("\n".join(lines))

    result = mine_module.parse_session(log)
    tool_uses = [t for t in result["tool_uses"] if not t["name"].startswith("__")]
    assert len(tool_uses) == 2
    assert tool_uses[0]["name"] == "Bash"
    assert tool_uses[1]["name"] == "Read"


def test_parse_malformed_jsonl(mine_module, tmp_path: Path):
    """Bad lines are skipped, good lines parsed."""
    log = tmp_path / "session.jsonl"
    lines = [
        "this is not json",
        json.dumps(
            {
                "type": "user",
                "message": {"type": "user", "content": "Valid message"},
                "userType": "external",
                "timestamp": "2026-02-28T10:00:00+00:00",
            }
        ),
        "{broken json",
        json.dumps(
            {
                "type": "user",
                "message": {"type": "user", "content": "Another valid one"},
                "userType": "external",
                "timestamp": "2026-02-28T10:01:00+00:00",
            }
        ),
    ]
    log.write_text("\n".join(lines))

    result = mine_module.parse_session(log)
    assert len(result["user_messages"]) == 2
    assert result["user_messages"][0] == "Valid message"
    assert result["user_messages"][1] == "Another valid one"


# ── detect_signals ──


def test_detect_skill_usage(mine_module):
    """Detect skills/ references in tool args."""
    tool_uses = [
        {
            "name": "Bash",
            "input": {"command": "python3 skills/earnings-trade-analyzer/scripts/run.py"},
        },
        {
            "name": "Read",
            "input": {"file_path": "skills/pead-screener/SKILL.md"},
        },
        {
            "name": "Bash",
            "input": {"command": "ls -la"},
        },
    ]
    result = mine_module._detect_skill_usage(tool_uses)
    assert result["count"] == 2
    assert "earnings-trade-analyzer" in result["skills"]
    assert "pead-screener" in result["skills"]


def test_detect_errors(mine_module):
    """Detect error patterns in tool results."""
    tool_uses = [
        {"name": "__tool_result_error__", "output": "Error: API key missing"},
        {"name": "__tool_result_error__", "output": "Traceback (most recent call last):\n..."},
        {"name": "Bash", "input": {"command": "echo hello"}},
    ]
    result = mine_module._detect_errors(tool_uses)
    assert result["count"] == 2
    assert len(result["samples"]) == 2


def test_detect_automation_requests(mine_module):
    """Detect automation keywords in user messages."""
    messages = [
        "Can you create a skill for this?",
        "Just run the analysis",
        "I want to automate this workflow",
        "スキルを作成してほしい",
    ]
    result = mine_module._detect_automation_requests(messages)
    assert result["count"] == 3
    assert len(result["samples"]) == 3


def test_detect_automation_requests_excludes_automated_prompts(mine_module):
    """Claude -p automated prompts are excluded from automation_requests."""
    messages = [
        "# LLM Skill Review Request\nPlease review this skill...",
        "Improve the skill 'backtest-expert' using the review results below.",
        "Implement the following plan:\n1. Create skill...",
        "Score each skill idea candidate on three dimensions...",
        "Can you create a skill for this?",  # Real user request
    ]
    result = mine_module._detect_automation_requests(messages)
    assert result["count"] == 1
    assert "create a skill" in result["samples"][0].lower()


def test_is_automated_prompt(mine_module):
    """_is_automated_prompt correctly identifies automated prompts."""
    assert mine_module._is_automated_prompt("# LLM Skill Review Request\nContent...")
    assert mine_module._is_automated_prompt("Improve the skill 'x' using...")
    assert mine_module._is_automated_prompt("Implement the following plan:\n...")
    assert mine_module._is_automated_prompt("Score each skill idea candidate on...")
    assert not mine_module._is_automated_prompt("Can you create a skill?")
    assert not mine_module._is_automated_prompt("I want to automate this")


def test_is_automated_prompt_new_prefixes(mine_module):
    """'Design and create a complete Claude skill' returns True."""
    assert mine_module._is_automated_prompt("Design and create a complete Claude skill for project management")


def test_automated_prompt_filtering(mine_module):
    """_detect_automation_requests excludes automated prompts including new prefix."""
    messages = [
        "Design and create a complete Claude skill for PM",
        "Can you create a skill for this?",
    ]
    result = mine_module._detect_automation_requests(messages)
    assert result["count"] == 1
    assert "create a skill" in result["samples"][0].lower()


# ── _detect_unresolved_requests ──


def test_detect_unresolved_requests_no_gap(mine_module):
    """User message followed by quick assistant response is not unresolved."""
    timed_entries = [
        {"timestamp": "2026-02-28T10:00:00+00:00", "type": "user"},
        {"timestamp": "2026-02-28T10:00:30+00:00", "type": "assistant"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 0


def test_detect_unresolved_requests_with_gap(mine_module):
    """User message followed by 10-min gap before response is unresolved."""
    timed_entries = [
        {"timestamp": "2026-02-28T10:00:00+00:00", "type": "user"},
        {"timestamp": "2026-02-28T10:10:00+00:00", "type": "assistant"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 1


def test_detect_unresolved_requests_user_then_user(mine_module):
    """Consecutive user messages with gap: first is unresolved."""
    timed_entries = [
        {"timestamp": "2026-02-28T10:00:00+00:00", "type": "user"},
        {"timestamp": "2026-02-28T10:06:00+00:00", "type": "user"},
        {"timestamp": "2026-02-28T10:06:10+00:00", "type": "assistant"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 1


# ── _extract_json_from_claude ──


def test_extract_json_from_claude_candidates(mine_module):
    """JSON with candidates key is extracted."""
    raw = json.dumps(
        {
            "candidates": [
                {
                    "name": "test-skill",
                    "description": "A test",
                    "rationale": "Because",
                    "priority": "high",
                },
            ],
        }
    )
    result = mine_module._extract_json_from_claude(raw, ["candidates"])
    assert result is not None
    assert "candidates" in result
    assert len(result["candidates"]) == 1


def test_extract_json_from_claude_wrapped(mine_module):
    """JSON wrapped in claude --output-format json envelope."""
    inner = json.dumps(
        {
            "candidates": [{"name": "x", "description": "y", "rationale": "z", "priority": "low"}],
        }
    )
    wrapper = json.dumps({"result": f"Here are the ideas:\n{inner}\nDone."})
    result = mine_module._extract_json_from_claude(wrapper, ["candidates"])
    assert result is not None
    assert result["candidates"][0]["name"] == "x"


def test_extract_json_from_claude_no_candidates(mine_module):
    """JSON without 'candidates' key returns None."""
    raw = '{"score": 85, "summary": "review"}'
    result = mine_module._extract_json_from_claude(raw, ["candidates"])
    assert result is None


# ── Real session format: entry.type != msg.type ──


def test_parse_assistant_with_message_type(mine_module, tmp_path: Path):
    """Real session format: entry.type=assistant, msg.type=message, msg.role=assistant."""
    log = tmp_path / "session.jsonl"
    entry = {
        "type": "assistant",
        "message": {
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Read",
                    "input": {"file_path": "skills/pead-screener/SKILL.md"},
                },
            ],
        },
        "timestamp": "2026-02-28T10:00:00+00:00",
    }
    log.write_text(json.dumps(entry))
    result = mine_module.parse_session(log)
    tool_uses = [t for t in result["tool_uses"] if not t["name"].startswith("__")]
    assert len(tool_uses) == 1
    assert tool_uses[0]["name"] == "Read"


def test_timed_entries_correct_types(mine_module, tmp_path: Path):
    """timed_entries records entry-level type, not message-level type."""
    log = tmp_path / "session.jsonl"
    lines = [
        json.dumps(
            {
                "type": "user",
                "message": {"type": "user", "content": "Hello"},
                "userType": "external",
                "timestamp": "2026-02-28T10:00:00+00:00",
            }
        ),
        json.dumps(
            {
                "type": "assistant",
                "message": {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "text", "text": "Hi"}],
                },
                "timestamp": "2026-02-28T10:00:05+00:00",
            }
        ),
    ]
    log.write_text("\n".join(lines))
    result = mine_module.parse_session(log)
    assert result["timed_entries"][0]["type"] == "user"
    assert result["timed_entries"][1]["type"] == "assistant"


def test_parse_assistant_role_fallback(mine_module, tmp_path: Path):
    """When entry has no type but msg.role=assistant, tool_use blocks are extracted."""
    log = tmp_path / "session.jsonl"
    entry = {
        "message": {
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Bash",
                    "input": {"command": "ls"},
                },
            ],
        },
        "timestamp": "2026-02-28T10:00:00+00:00",
    }
    log.write_text(json.dumps(entry))
    result = mine_module.parse_session(log)
    tool_uses = [t for t in result["tool_uses"] if not t["name"].startswith("__")]
    assert len(tool_uses) == 1
    assert tool_uses[0]["name"] == "Bash"


# ── find_project_dirs endswith fix ──


def test_find_project_dirs_no_false_positive(mine_module, tmp_path: Path):
    """Suffix match without dash boundary should not match."""
    base = tmp_path / "projects"
    base.mkdir()
    (base / "-Users-alice-notclaude-skills-library").mkdir()
    (base / "-Users-bob-PycharmProjects-claude-skills-library").mkdir()

    result = mine_module.find_project_dirs(base, ["claude-skills-library"])
    assert len(result) == 1
    assert result[0][1].name == "-Users-bob-PycharmProjects-claude-skills-library"


def test_find_project_dirs_exact_name(mine_module, tmp_path: Path):
    """Directory with exact project name matches."""
    base = tmp_path / "projects"
    base.mkdir()
    (base / "claude-skills-library").mkdir()

    result = mine_module.find_project_dirs(base, ["claude-skills-library"])
    assert len(result) == 1
    assert result[0][0] == "claude-skills-library"


# ── Fix A: _parse_timestamp timezone normalization ──


def test_parse_timestamp_naive_gets_utc(mine_module):
    """Naive timestamps are normalized to UTC-aware."""
    from datetime import timezone

    dt = mine_module._parse_timestamp("2026-03-01T10:00:00")
    assert dt is not None
    assert dt.tzinfo is not None
    assert dt.tzinfo == timezone.utc


def test_parse_timestamp_aware_preserved(mine_module):
    """Aware timestamps keep their original tzinfo."""
    from datetime import timedelta

    dt = mine_module._parse_timestamp("2026-03-01T10:00:00+09:00")
    assert dt is not None
    assert dt.utcoffset() == timedelta(hours=9)


def test_unresolved_requests_mixed_tz(mine_module):
    """Naive and aware timestamps can be subtracted without TypeError."""
    timed_entries = [
        {"timestamp": "2026-03-01T10:00:00", "type": "user"},
        {"timestamp": "2026-03-01T10:10:00+00:00", "type": "assistant"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 1


# ── Fix A2: sidechain contamination ──


def test_sidechain_excluded_from_timed_entries(mine_module, tmp_path: Path):
    """Sidechain messages should not appear in timed_entries."""
    log = tmp_path / "session.jsonl"
    lines = [
        json.dumps(
            {
                "type": "user",
                "message": {"type": "user", "content": "Hello"},
                "userType": "external",
                "timestamp": "2026-03-01T10:00:00+00:00",
            }
        ),
        json.dumps(
            {
                "type": "assistant",
                "message": {"type": "assistant", "content": [{"type": "text", "text": "Hi"}]},
                "isSidechain": True,
                "timestamp": "2026-03-01T10:00:05+00:00",
            }
        ),
        json.dumps(
            {
                "type": "assistant",
                "message": {"type": "assistant", "content": [{"type": "text", "text": "Real"}]},
                "timestamp": "2026-03-01T10:00:10+00:00",
            }
        ),
    ]
    log.write_text("\n".join(lines))
    result = mine_module.parse_session(log)
    types = [e["type"] for e in result["timed_entries"]]
    assert len(types) == 2
    assert types == ["user", "assistant"]


# ── Fix A3: end-of-session exclusion ──


def test_unresolved_requests_end_of_session(mine_module):
    """User message at end of session (no following non-user entry) is NOT unresolved."""
    timed_entries = [
        {"timestamp": "2026-03-01T10:00:00+00:00", "type": "user"},
        {"timestamp": "2026-03-01T10:00:05+00:00", "type": "assistant"},
        {"timestamp": "2026-03-01T10:05:00+00:00", "type": "user"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 0


# ── Fix D: MAX_ERROR_OUTPUT_LEN truncation ──


def test_error_output_truncated(mine_module, tmp_path: Path):
    """Long error outputs are truncated to MAX_ERROR_OUTPUT_LEN."""
    log = tmp_path / "session.jsonl"
    long_error = "Error: " + "x" * 1000
    entry = {
        "type": "tool_result",
        "message": {"type": "tool_result", "content": long_error},
        "is_error": True,
        "timestamp": "2026-03-01T10:00:00+00:00",
    }
    log.write_text(json.dumps(entry))
    result = mine_module.parse_session(log)
    error_entries = [t for t in result["tool_uses"] if t["name"] == "__tool_result_error__"]
    assert len(error_entries) == 1
    assert len(error_entries[0]["output"]) <= mine_module.MAX_ERROR_OUTPUT_LEN


def test_error_pattern_output_truncated(mine_module, tmp_path: Path):
    """Error-pattern path (is_error=False) also truncates long output."""
    log = tmp_path / "session.jsonl"
    long_traceback = "Traceback (most recent call last):\n" + "  File x.py\n" * 200
    entry = {
        "type": "tool_result",
        "message": {"type": "tool_result", "content": long_traceback},
        "timestamp": "2026-03-01T10:00:00+00:00",
    }
    log.write_text(json.dumps(entry))
    result = mine_module.parse_session(log)
    error_entries = [t for t in result["tool_uses"] if t["name"] == "__tool_result_error__"]
    assert len(error_entries) == 1
    assert len(error_entries[0]["output"]) <= mine_module.MAX_ERROR_OUTPUT_LEN


# ── Z-suffix timestamp handling ──


def test_parse_timestamp_z_suffix(mine_module):
    """Timestamps ending with Z are parsed correctly."""
    from datetime import timezone

    dt = mine_module._parse_timestamp("2026-03-01T10:00:00Z")
    assert dt is not None
    assert dt.tzinfo == timezone.utc
    assert dt.hour == 10


def test_parse_timestamp_z_with_millis(mine_module):
    """Z-suffix with milliseconds is also handled."""
    dt = mine_module._parse_timestamp("2026-03-01T10:00:00.123Z")
    assert dt is not None
    assert dt.microsecond == 123000


def test_unresolved_requests_z_timestamps(mine_module):
    """Real session logs use Z-suffix timestamps; detection must work."""
    timed_entries = [
        {"timestamp": "2026-03-01T10:00:00Z", "type": "user"},
        {"timestamp": "2026-03-01T10:10:00Z", "type": "assistant"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 1


# ── Response type filtering ──


def test_unresolved_requests_ignores_system_entries(mine_module):
    """system/progress/queue-operation entries do not count as a response."""
    timed_entries = [
        {"timestamp": "2026-03-01T10:00:00+00:00", "type": "user"},
        {"timestamp": "2026-03-01T10:00:01+00:00", "type": "system"},
        {"timestamp": "2026-03-01T10:00:02+00:00", "type": "progress"},
        {"timestamp": "2026-03-01T10:06:00+00:00", "type": "assistant"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 1


def test_unresolved_requests_tool_result_counts_as_response(mine_module):
    """tool_result entries count as a valid response."""
    timed_entries = [
        {"timestamp": "2026-03-01T10:00:00+00:00", "type": "user"},
        {"timestamp": "2026-03-01T10:00:30+00:00", "type": "tool_result"},
    ]
    result = mine_module._detect_unresolved_requests(timed_entries)
    assert result["count"] == 0


# ── N4: C1 regression test (name->title conversion + id generation) ──


def test_run_converts_name_to_title_and_adds_id(mine_module, tmp_path: Path):
    """run() converts LLM-returned 'name' to 'title' and generates 'id' for each candidate."""
    import types
    from unittest.mock import patch

    import yaml

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    fake_candidates = [
        {"name": "Auto Reporter", "description": "Automated reports", "priority": "high"},
        {"title": "Already Titled", "description": "Has title", "priority": "low"},
    ]

    args = types.SimpleNamespace(
        output_dir=str(output_dir),
        projects=None,
        lookback_days=7,
        dry_run=False,
    )

    with (
        patch.object(mine_module, "find_project_dirs", return_value=[("proj_enc", tmp_path)]),
        patch.object(
            mine_module,
            "list_session_logs",
            return_value=[("proj_enc", tmp_path / "fake.jsonl")],
        ),
        patch.object(
            mine_module,
            "parse_session",
            return_value={
                "user_messages": ["hello"],
                "tool_uses": [],
                "timestamps": [],
                "timed_entries": [],
            },
        ),
        patch.object(mine_module, "abstract_with_llm", return_value=fake_candidates),
    ):
        rc = mine_module.run(args)

    assert rc == 0

    output_path = output_dir / "raw_candidates.yaml"
    assert output_path.exists()
    data = yaml.safe_load(output_path.read_text(encoding="utf-8"))

    candidates = data["candidates"]
    assert len(candidates) == 2

    assert "title" in candidates[0]
    assert candidates[0]["title"] == "Auto Reporter"
    assert "name" not in candidates[0]

    assert candidates[1]["title"] == "Already Titled"

    assert candidates[0]["id"].startswith("raw_")
    assert candidates[1]["id"].startswith("raw_")
    assert candidates[0]["id"] != candidates[1]["id"]


# ── Project name sanitization in output ──


def test_project_name_sanitized_in_output(mine_module, tmp_path: Path):
    """run() output session_details[].project has no username."""
    import types
    from unittest.mock import patch

    import yaml

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    encoded_name = "-Users-taku-PycharmProjects-my-project"
    proj_dir = tmp_path / encoded_name
    proj_dir.mkdir()

    args = types.SimpleNamespace(
        output_dir=str(output_dir),
        projects=None,
        lookback_days=7,
        dry_run=True,
    )

    with (
        patch.object(
            mine_module,
            "find_project_dirs",
            return_value=[(encoded_name, proj_dir)],
        ),
        patch.object(
            mine_module,
            "list_session_logs",
            return_value=[(encoded_name, tmp_path / "fake.jsonl")],
        ),
        patch.object(
            mine_module,
            "parse_session",
            return_value={
                "user_messages": ["hello"],
                "tool_uses": [],
                "timestamps": [],
                "timed_entries": [],
            },
        ),
    ):
        rc = mine_module.run(args)

    assert rc == 0
    output_path = output_dir / "raw_candidates.yaml"
    data = yaml.safe_load(output_path.read_text(encoding="utf-8"))

    # session_details project should be sanitized
    assert data["session_details"][0]["project"] == "PycharmProjects-my-project"


def test_project_name_sanitized_in_llm_prompt(mine_module):
    """LLM prompt uses sanitized project name (no username)."""
    signals = {"skill_usage": {"count": 0, "skills": {}}}
    user_samples = ["test message"]
    prompt = mine_module._build_llm_prompt(signals, user_samples, "PycharmProjects-my-project")
    assert "PycharmProjects-my-project" in prompt
    assert "-Users-" not in prompt


# ── scanned_projects field ──


def test_candidates_have_scanned_projects(mine_module, tmp_path: Path):
    """Enriched candidates have scanned_projects field."""
    import types
    from unittest.mock import patch

    import yaml

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    fake_candidates = [
        {"title": "Some Idea", "description": "desc", "priority": "high"},
    ]

    args = types.SimpleNamespace(
        output_dir=str(output_dir),
        projects=None,
        lookback_days=7,
        dry_run=False,
    )

    with (
        patch.object(
            mine_module,
            "find_project_dirs",
            return_value=[
                ("-Users-taku-PycharmProjects-proj-a", tmp_path),
                ("-Users-taku-Code-proj-b", tmp_path),
            ],
        ),
        patch.object(
            mine_module,
            "list_session_logs",
            return_value=[
                ("-Users-taku-PycharmProjects-proj-a", tmp_path / "a.jsonl"),
                ("-Users-taku-Code-proj-b", tmp_path / "b.jsonl"),
            ],
        ),
        patch.object(
            mine_module,
            "parse_session",
            return_value={
                "user_messages": ["hello"],
                "tool_uses": [],
                "timestamps": [],
                "timed_entries": [],
            },
        ),
        patch.object(mine_module, "abstract_with_llm", return_value=fake_candidates),
    ):
        rc = mine_module.run(args)

    assert rc == 0
    output_path = output_dir / "raw_candidates.yaml"
    data = yaml.safe_load(output_path.read_text(encoding="utf-8"))

    candidates = data["candidates"]
    assert len(candidates) == 1
    assert "scanned_projects" in candidates[0]
    assert isinstance(candidates[0]["scanned_projects"], list)
