"""Event publishing helpers for Redis-backed integration."""

from __future__ import annotations

import json
import os
from typing import Optional

from .schemas import EventMessage

try:  # pragma: no cover - optional dependency
    import redis
except ImportError:  # pragma: no cover - optional dependency
    redis = None


class RedisEventPublisher:
    """Publish integration events to Redis pub/sub channels."""

    def __init__(self, redis_url: Optional[str] = None) -> None:
        if redis is None:
            raise RuntimeError("redis package is required for RedisEventPublisher")

        self._redis = redis.from_url(redis_url or os.getenv("REDIS_URL", "redis://redis:6379/0"))

    def publish(self, channel: str, event: EventMessage) -> None:
        """
        Publish an event message to a Redis channel.

        Args:
            channel: Redis pub/sub channel.
            event: EventMessage to publish.
        """
        payload = json.dumps(event.to_dict())
        self._redis.publish(channel, payload)
