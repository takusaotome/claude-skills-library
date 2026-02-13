"""Tests for agent/client.py."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from agent.client import PresentationAgent
from claude_agent_sdk import AssistantMessage, TextBlock, ToolUseBlock, ResultMessage
from claude_agent_sdk.types import StreamEvent


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _async_iter(items):
    """Async generator that yields items from a list (mocks receive_response)."""
    for item in items:
        yield item


def _connected_agent():
    """Create a PresentationAgent with pre-set connection (skips auto-connect)."""
    agent = PresentationAgent()
    agent._client = MagicMock()
    agent._client.query = AsyncMock()
    agent._connected = True
    return agent


class TestPresentationAgentInit:
    def test_defaults(self):
        agent = PresentationAgent()
        assert agent.language == "EN"
        assert agent._connected is False
        assert agent._client is None

    def test_custom_language(self):
        agent = PresentationAgent(language="JP")
        assert agent.language == "JP"

    def test_custom_model(self):
        agent = PresentationAgent(model="claude-opus-4-6")
        assert agent.model == "claude-opus-4-6"


class TestBuildOptions:
    def test_includes_seven_allowed_tools(self):
        agent = PresentationAgent()
        with patch("agent.client.create_presentation_tools_server"):
            with patch("agent.client.build_system_prompt", return_value="prompt"):
                with patch("agent.client.ClaudeAgentOptions") as MockOpts:
                    agent._build_options()
                    kwargs = MockOpts.call_args[1]
                    expected = [
                        "mcp__ptools__list_skills",
                        "mcp__ptools__load_skill",
                        "mcp__ptools__convert_to_pdf",
                        "mcp__ptools__convert_to_html",
                        "mcp__ptools__review_structure",
                        "mcp__ptools__render_mermaid",
                        "mcp__ptools__review_design",
                    ]
                    assert kwargs["allowed_tools"] == expected

    def test_uses_correct_language(self):
        agent = PresentationAgent(language="JP")
        with patch("agent.client.create_presentation_tools_server"):
            with patch("agent.client.build_system_prompt", return_value="JP prompt") as mock_build:
                with patch("agent.client.ClaudeAgentOptions") as MockOpts:
                    agent._build_options()
                    mock_build.assert_called_once_with("JP")
                    kwargs = MockOpts.call_args[1]
                    assert kwargs["system_prompt"] == "JP prompt"

    def test_permission_mode_is_bypass(self):
        agent = PresentationAgent()
        with patch("agent.client.create_presentation_tools_server"):
            with patch("agent.client.build_system_prompt", return_value="prompt"):
                with patch("agent.client.ClaudeAgentOptions") as MockOpts:
                    agent._build_options()
                    kwargs = MockOpts.call_args[1]
                    assert kwargs["permission_mode"] == "bypassPermissions"


class TestConnectDisconnect:
    @pytest.mark.asyncio
    async def test_connect_sets_connected(self):
        agent = PresentationAgent()
        mock_client = MagicMock()
        mock_client.connect = AsyncMock()
        with patch("agent.client.ClaudeSDKClient", return_value=mock_client):
            with patch.object(agent, "_build_options"):
                await agent.connect()
        assert agent._connected is True

    @pytest.mark.asyncio
    async def test_disconnect_clears_state(self):
        agent = PresentationAgent()
        agent._client = MagicMock()
        agent._client.disconnect = AsyncMock()
        agent._connected = True
        await agent.disconnect()
        assert agent._connected is False
        assert agent._client is None

    @pytest.mark.asyncio
    async def test_disconnect_noop_when_not_connected(self):
        agent = PresentationAgent()
        await agent.disconnect()  # should not raise
        assert agent._connected is False


class TestSendMessage:
    @pytest.mark.asyncio
    async def test_returns_text_from_assistant_message(self):
        agent = _connected_agent()
        messages = [AssistantMessage([TextBlock("Hello"), TextBlock(" World")])]
        agent._client.receive_response = lambda: _async_iter(messages)

        result = await agent.send_message("hi")
        assert result == "Hello\n World"

    @pytest.mark.asyncio
    async def test_records_tool_use_without_affecting_response(self):
        agent = _connected_agent()
        messages = [AssistantMessage([ToolUseBlock(name="load_skill"), TextBlock("Done")])]
        agent._client.receive_response = lambda: _async_iter(messages)

        result = await agent.send_message("do something")
        assert result == "Done"

    @pytest.mark.asyncio
    async def test_appends_error_from_result_message(self):
        agent = _connected_agent()
        messages = [ResultMessage(is_error=True, result="API error")]
        agent._client.receive_response = lambda: _async_iter(messages)

        result = await agent.send_message("fail")
        assert "⚠️ Error: API error" in result

    @pytest.mark.asyncio
    async def test_returns_no_response_when_empty(self):
        agent = _connected_agent()
        agent._client.receive_response = lambda: _async_iter([])

        result = await agent.send_message("hello")
        assert result == "(No response)"

    @pytest.mark.asyncio
    async def test_auto_connects_when_not_connected(self):
        agent = PresentationAgent()
        agent._client = None
        agent._connected = False

        async def fake_connect():
            agent._client = MagicMock()
            agent._client.query = AsyncMock()
            agent._client.receive_response = lambda: _async_iter([])
            agent._connected = True

        with patch.object(agent, "connect", new_callable=AsyncMock, side_effect=fake_connect):
            result = await agent.send_message("auto")
            agent.connect.assert_awaited_once()
            assert result == "(No response)"


class TestSendMessageStreaming:
    @pytest.mark.asyncio
    async def test_yields_text_delta_from_stream_event(self):
        agent = _connected_agent()
        event = StreamEvent({
            "type": "content_block_delta",
            "delta": {"type": "text_delta", "text": "Hi"},
        })
        agent._client.receive_response = lambda: _async_iter([event])

        chunks = [chunk async for chunk in agent.send_message_streaming("hi")]
        assert chunks == [{"type": "text_delta", "content": "Hi"}]

    @pytest.mark.asyncio
    async def test_yields_tool_use_from_stream_event(self):
        agent = _connected_agent()
        event = StreamEvent({
            "type": "content_block_start",
            "content_block": {"type": "tool_use", "name": "convert_to_pdf"},
        })
        agent._client.receive_response = lambda: _async_iter([event])

        chunks = [chunk async for chunk in agent.send_message_streaming("convert")]
        assert chunks == [{"type": "tool_use", "content": "convert_to_pdf"}]

    @pytest.mark.asyncio
    async def test_yields_text_fallback_from_assistant_message(self):
        agent = _connected_agent()
        messages = [AssistantMessage([TextBlock("fallback")])]
        agent._client.receive_response = lambda: _async_iter(messages)

        chunks = [chunk async for chunk in agent.send_message_streaming("test")]
        assert chunks == [{"type": "text", "content": "fallback"}]

    @pytest.mark.asyncio
    async def test_yields_error_from_result_message(self):
        agent = _connected_agent()
        messages = [ResultMessage(is_error=True, result="fail")]
        agent._client.receive_response = lambda: _async_iter(messages)

        chunks = [chunk async for chunk in agent.send_message_streaming("fail")]
        assert chunks == [{"type": "error", "content": "fail"}]

    @pytest.mark.asyncio
    async def test_yields_done_from_result_message(self):
        agent = _connected_agent()
        messages = [ResultMessage(is_error=False, session_id="sess-123")]
        agent._client.receive_response = lambda: _async_iter(messages)

        chunks = [chunk async for chunk in agent.send_message_streaming("done")]
        assert chunks == [{"type": "done", "content": "Session: sess-123"}]

    @pytest.mark.asyncio
    async def test_yields_tool_use_complete_from_tool_use_block(self):
        agent = _connected_agent()
        messages = [AssistantMessage([ToolUseBlock(name="load_skill", input={"skill_name": "fin"})])]
        agent._client.receive_response = lambda: _async_iter(messages)

        chunks = [chunk async for chunk in agent.send_message_streaming("test")]
        tool_complete = [c for c in chunks if c["type"] == "tool_use_complete"]
        assert len(tool_complete) == 1
        assert tool_complete[0]["content"] == "load_skill"
        assert tool_complete[0]["input"] == {"skill_name": "fin"}

    @pytest.mark.asyncio
    async def test_yields_tool_use_complete_with_empty_input(self):
        agent = _connected_agent()
        messages = [AssistantMessage([ToolUseBlock(name="list_skills", input={})])]
        agent._client.receive_response = lambda: _async_iter(messages)

        chunks = [chunk async for chunk in agent.send_message_streaming("test")]
        tool_complete = [c for c in chunks if c["type"] == "tool_use_complete"]
        assert len(tool_complete) == 1
        assert tool_complete[0]["input"] == {}

    @pytest.mark.asyncio
    async def test_yields_both_tool_use_and_tool_use_complete(self):
        agent = _connected_agent()
        stream_event = StreamEvent({
            "type": "content_block_start",
            "content_block": {"type": "tool_use", "name": "convert_to_pdf"},
        })
        assistant_msg = AssistantMessage([ToolUseBlock(name="convert_to_pdf", input={"filename": "deck"})])
        agent._client.receive_response = lambda: _async_iter([stream_event, assistant_msg])

        chunks = [chunk async for chunk in agent.send_message_streaming("test")]
        types = [c["type"] for c in chunks]
        assert "tool_use" in types
        assert "tool_use_complete" in types
