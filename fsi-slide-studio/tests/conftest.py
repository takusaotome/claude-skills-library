"""Shared fixtures and SDK mock injection for FSI Slide Studio tests.

claude-agent-sdk is not installed locally, so we inject mock modules into
sys.modules BEFORE any source module can import it.  This block runs at
import time (when conftest.py is loaded by pytest).
"""

import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

import pytest

# ---------------------------------------------------------------------------
# Mock claude_agent_sdk  (must happen at module level, before test imports)
# ---------------------------------------------------------------------------
_sdk = types.ModuleType("claude_agent_sdk")
_sdk_types = types.ModuleType("claude_agent_sdk.types")


def _tool_decorator(name, description, params):
    """No-op @tool decorator — returns the original function unchanged."""
    def wrapper(fn):
        fn._tool_name = name
        fn._tool_description = description
        fn._tool_params = params
        return fn
    return wrapper


_sdk.tool = _tool_decorator
_sdk.create_sdk_mcp_server = MagicMock(name="create_sdk_mcp_server")
_sdk.query = AsyncMock(name="query")


class _ClaudeAgentOptions:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


_sdk.ClaudeAgentOptions = _ClaudeAgentOptions
_sdk.ClaudeSDKClient = MagicMock(name="ClaudeSDKClient")


# Type stubs used by client.py
class _AssistantMessage:
    def __init__(self, content=None):
        self.content = content or []


class _ResultMessage:
    def __init__(self, is_error=False, result=None, session_id=None):
        self.is_error = is_error
        self.result = result
        self.session_id = session_id


class _TextBlock:
    def __init__(self, text=""):
        self.text = text
        self.type = "text"


class _ToolUseBlock:
    def __init__(self, name="", input=None):
        self.name = name
        self.input = input or {}
        self.type = "tool_use"


class _ToolResultBlock:
    def __init__(self, content=""):
        self.content = content
        self.type = "tool_result"


class _Message:
    pass


class _StreamEvent:
    def __init__(self, event=None):
        self.event = event or {}


_sdk.AssistantMessage = _AssistantMessage
_sdk.ResultMessage = _ResultMessage
_sdk.TextBlock = _TextBlock
_sdk.ToolUseBlock = _ToolUseBlock
_sdk.ToolResultBlock = _ToolResultBlock
_sdk.Message = _Message

_sdk_types.StreamEvent = _StreamEvent

sys.modules["claude_agent_sdk"] = _sdk
sys.modules["claude_agent_sdk.types"] = _sdk_types

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_categories_yaml():
    """Path to the sample skill categories YAML fixture."""
    return FIXTURES_DIR / "sample_skill_categories.yaml"


@pytest.fixture
def tmp_skill_dir(tmp_path):
    """Create a temporary skill directory with SKILL.md and references/."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# Test Skill\n\nThis is a test skill.")
    refs = skill_dir / "references"
    refs.mkdir()
    (refs / "guide.md").write_text("# Guide\n\nShort reference content.")
    return skill_dir


@pytest.fixture
def tmp_skill_dir_with_long_ref(tmp_path):
    """Create a skill directory with a reference file exceeding 3000 bytes."""
    skill_dir = tmp_path / "verbose-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("# Verbose Skill\n\nContent here.")
    refs = skill_dir / "references"
    refs.mkdir()
    (refs / "long_ref.md").write_text("A" * 4000)
    return skill_dir
