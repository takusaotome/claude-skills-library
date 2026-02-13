"""Persistent event loop bridge for Claude Agent SDK.

The SDK retains internal anyio task groups tied to the event loop
created during connect(). A new loop per call (asyncio.run / new_event_loop
+ close) breaks that invariant because the SDK's tasks reference the
destroyed loop.

This module keeps a single event loop alive across Streamlit reruns.
Coroutines are dispatched via run_until_complete() on the main thread,
which is safe for subprocess-based MCP servers on macOS (child watchers
require the main thread).
"""

import asyncio


class AsyncBridge:
    """Reusable event loop that survives across Streamlit reruns."""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()

    def run(self, coro, timeout: float = 600):
        """Run a coroutine on the persistent loop (blocks the calling thread).

        Args:
            coro: Awaitable to execute.
            timeout: Maximum seconds to wait (default 600 for long
                     presentation generation).

        Returns:
            The coroutine's return value.

        Raises:
            RuntimeError: If the loop has been closed.
        """
        if self._loop.is_closed():
            raise RuntimeError("AsyncBridge loop is closed")
        # Ensure this loop is the "current" loop so libraries that call
        # asyncio.get_event_loop() internally pick up the right one.
        asyncio.set_event_loop(self._loop)
        return self._loop.run_until_complete(coro)

    @property
    def is_alive(self) -> bool:
        """True when the loop has not been closed."""
        return not self._loop.is_closed()

    def shutdown(self) -> None:
        """Cancel pending tasks and close the loop."""
        if self._loop.is_closed():
            return
        try:
            pending = asyncio.all_tasks(self._loop)
            for task in pending:
                task.cancel()
            if pending:
                self._loop.run_until_complete(
                    asyncio.gather(*pending, return_exceptions=True)
                )
        except Exception:
            pass
        self._loop.close()
