"""Tests for agent/async_bridge.py."""

import asyncio

import pytest

from agent.async_bridge import AsyncBridge


class TestAsyncBridge:
    def test_creates_event_loop(self):
        bridge = AsyncBridge()
        assert bridge.is_alive
        bridge.shutdown()

    def test_run_executes_coroutine(self):
        bridge = AsyncBridge()

        async def add(a, b):
            return a + b

        result = bridge.run(add(1, 2))
        assert result == 3
        bridge.shutdown()

    def test_run_returns_coroutine_result(self):
        bridge = AsyncBridge()

        async def greet(name):
            return f"Hello, {name}"

        result = bridge.run(greet("World"))
        assert result == "Hello, World"
        bridge.shutdown()

    def test_raises_after_shutdown(self):
        bridge = AsyncBridge()
        bridge.shutdown()
        assert not bridge.is_alive

        async def noop():
            pass

        with pytest.raises(RuntimeError, match="closed"):
            bridge.run(noop())

    def test_shutdown_is_idempotent(self):
        bridge = AsyncBridge()
        bridge.shutdown()
        bridge.shutdown()  # should not raise
        assert not bridge.is_alive

    def test_is_alive_property(self):
        bridge = AsyncBridge()
        assert bridge.is_alive is True
        bridge.shutdown()
        assert bridge.is_alive is False

    def test_preserves_loop_across_calls(self):
        bridge = AsyncBridge()

        async def get_loop_id():
            return id(asyncio.get_event_loop())

        id1 = bridge.run(get_loop_id())
        id2 = bridge.run(get_loop_id())
        assert id1 == id2
        bridge.shutdown()
