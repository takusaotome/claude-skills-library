"""Tests for agent/client.py."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from agent.client import PresentationAgent


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
    def test_includes_six_allowed_tools(self):
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
