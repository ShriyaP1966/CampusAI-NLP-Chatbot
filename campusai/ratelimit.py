"""A small in-memory sliding-window rate limiter."""

from __future__ import annotations

import time
from collections import defaultdict, deque


class RateLimiter:
    """Allow at most ``limit`` calls per ``window`` seconds for each key."""

    def __init__(self, limit: int, window: float = 60.0, clock=time.monotonic):
        self.limit = limit
        self.window = window
        self._clock = clock
        self._calls: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        if self.limit <= 0:
            return True
        now = self._clock()
        calls = self._calls[key]
        while calls and now - calls[0] >= self.window:
            calls.popleft()
        if len(self._calls) > 10_000:
            self._drop_idle(now)
        if len(calls) >= self.limit:
            return False
        calls.append(now)
        return True

    def _drop_idle(self, now: float) -> None:
        for key in [k for k, v in self._calls.items() if not v or now - v[-1] >= self.window]:
            del self._calls[key]
