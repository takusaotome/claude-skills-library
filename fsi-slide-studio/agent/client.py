"""Claude Agent SDK client management for multi-turn presentation conversations."""

import asyncio
from typing import AsyncIterator

from claude_agent_sdk import (
    ClaudeSDKClient,
    ClaudeAgentOptions,
    AssistantMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    Message,
)

from agent.system_prompt import build_system_prompt
from agent.tools import create_presentation_tools_server
from config.settings import DEFAULT_MODEL, OUTPUT_DIR


class PresentationAgent:
    """Manages a multi-turn conversation session with the Claude Agent SDK."""

    def __init__(self, language: str = "EN", model: str | None = None):
        self.language = language
        self.model = model or DEFAULT_MODEL
        self._client: ClaudeSDKClient | None = None
        self._connected = False

    def _build_options(self) -> ClaudeAgentOptions:
        """Build ClaudeAgentOptions with custom tools and system prompt."""
        tools_server = create_presentation_tools_server()
        system_prompt = build_system_prompt(self.language)

        return ClaudeAgentOptions(
            system_prompt=system_prompt,
            model=self.model,
            permission_mode="bypassPermissions",
            mcp_servers={"ptools": tools_server},
            allowed_tools=[
                "mcp__ptools__list_skills",
                "mcp__ptools__load_skill",
                "mcp__ptools__convert_to_pdf",
                "mcp__ptools__convert_to_html",
                "mcp__ptools__review_structure",
                "mcp__ptools__review_design",
            ],
            cwd=str(OUTPUT_DIR),
            max_turns=30,
        )

    async def connect(self) -> None:
        """Initialize and connect the client."""
        options = self._build_options()
        self._client = ClaudeSDKClient(options)
        await self._client.connect()
        self._connected = True

    async def disconnect(self) -> None:
        """Disconnect the client."""
        if self._client and self._connected:
            await self._client.disconnect()
            self._connected = False
            self._client = None

    async def send_message(self, user_message: str) -> str:
        """Send a message and collect the full text response.

        Args:
            user_message: The user's chat message.

        Returns:
            The agent's text response.
        """
        if not self._client or not self._connected:
            await self.connect()

        await self._client.query(user_message)

        response_parts = []
        tool_activity = []

        async for message in self._client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        response_parts.append(block.text)
                    elif isinstance(block, ToolUseBlock):
                        tool_activity.append(f"🔧 Using: {block.name}")
            elif isinstance(message, ResultMessage):
                if message.is_error:
                    response_parts.append(f"\n\n⚠️ Error: {message.result or 'Unknown error'}")

        return "\n".join(response_parts) if response_parts else "(No response)"

    async def send_message_streaming(self, user_message: str) -> AsyncIterator[dict]:
        """Send a message and yield response chunks for streaming display.

        Yields dicts with keys:
            - type: "text" | "tool_use" | "tool_result" | "done" | "error"
            - content: The text content or tool info
        """
        if not self._client or not self._connected:
            await self.connect()

        await self._client.query(user_message)

        async for message in self._client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        yield {"type": "text", "content": block.text}
                    elif isinstance(block, ToolUseBlock):
                        yield {"type": "tool_use", "content": block.name}
                    elif isinstance(block, ToolResultBlock):
                        content_str = ""
                        if isinstance(block.content, str):
                            content_str = block.content
                        elif isinstance(block.content, list):
                            for item in block.content:
                                if isinstance(item, dict) and item.get("type") == "text":
                                    content_str += item.get("text", "")
                        yield {"type": "tool_result", "content": content_str}
            elif isinstance(message, ResultMessage):
                if message.is_error:
                    yield {"type": "error", "content": message.result or "Unknown error"}
                else:
                    yield {
                        "type": "done",
                        "content": f"Session: {message.session_id}",
                    }
