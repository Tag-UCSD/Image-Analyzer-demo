"""Event subscription helpers for Redis-backed integration."""

from __future__ import annotations

import json
import os
import threading
import time
from typing import Callable, Dict, List, Optional

from .schemas import EventMessage

try:  # pragma: no cover - optional dependency
    import redis
except ImportError:  # pragma: no cover - optional dependency
    redis = None


class RedisEventSubscriber:
    """Subscribe to Redis pub/sub channels and dispatch events."""

    def __init__(
        self,
        channels: List[str],
        handler: Callable[[EventMessage], None],
        redis_url: Optional[str] = None,
    ) -> None:
        if redis is None:
            raise RuntimeError("redis package is required for RedisEventSubscriber")

        self._channels = channels
        self._handler = handler
        self._redis = redis.from_url(redis_url or os.getenv("REDIS_URL", "redis://redis:6379/0"))
        self._pubsub = self._redis.pubsub()
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def start(self) -> None:
        """Start the background listener thread."""
        if self._thread and self._thread.is_alive():
            return

        self._pubsub.subscribe(*self._channels)
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the listener thread and close the Redis connection."""
        self._stop_event.set()
        try:
            self._pubsub.close()
        except Exception:
            pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)

    def _listen(self) -> None:
        while not self._stop_event.is_set():
            try:
                message = self._pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            except Exception:
                if self._stop_event.is_set():
                    break
                time.sleep(0.1)
                continue
            if not message:
                continue
            if message.get("type") != "message":
                continue

            try:
                data = json.loads(message.get("data", "{}"))
                event = EventMessage.from_dict(data)
                self._handler(event)
            except Exception:
                continue


class InMemoryEventBus:
    """In-memory event bus for local testing without Redis."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[EventMessage], None]]] = {}
        self._lock = threading.Lock()

    def subscribe(self, channel: str, handler: Callable[[EventMessage], None]) -> None:
        """Register a handler for the given channel."""
        with self._lock:
            self._subscribers.setdefault(channel, []).append(handler)

    def publish(self, channel: str, event: EventMessage) -> None:
        """Publish an event to all handlers for the channel."""
        with self._lock:
            handlers = list(self._subscribers.get(channel, []))
        for handler in handlers:
            handler(event)
