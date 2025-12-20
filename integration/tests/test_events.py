"""Tests for shared event bus helpers."""

from __future__ import annotations

import os
import unittest

from integration.shared.events import EventMessage, InMemoryEventBus

try:  # pragma: no cover - optional dependency
    from integration.shared.events import RedisEventPublisher, RedisEventSubscriber
    import redis
except ImportError:  # pragma: no cover - optional dependency
    RedisEventPublisher = None
    RedisEventSubscriber = None
    redis = None


class TestEvents(unittest.TestCase):
    """Validate in-memory event bus behavior."""

    def test_publish_and_subscribe(self) -> None:
        bus = InMemoryEventBus()
        received = []

        def handler(event: EventMessage) -> None:
            received.append(event)

        bus.subscribe("test-channel", handler)
        event = EventMessage.create("image.tagged", "tagger", {"image_id": "img-1"})
        bus.publish("test-channel", event)

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0].event_type, "image.tagged")
        self.assertEqual(received[0].payload["image_id"], "img-1")

    def test_redis_pubsub_optional(self) -> None:
        if redis is None or RedisEventPublisher is None or RedisEventSubscriber is None:
            self.skipTest("redis package not available")

        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        try:
            client = redis.from_url(redis_url)
            client.ping()
        except Exception:
            self.skipTest("Redis server not available")

        received = []

        def handler(event: EventMessage) -> None:
            received.append(event)

        subscriber = RedisEventSubscriber(["test-channel"], handler, redis_url=redis_url)
        subscriber.start()

        publisher = RedisEventPublisher(redis_url=redis_url)
        event = EventMessage.create("paper.processed", "article", {"paper_id": "paper-1"})
        publisher.publish("test-channel", event)

        for _ in range(10):
            if received:
                break
            import time
            time.sleep(0.1)

        subscriber.stop()

        if not received:
            self.fail("Redis event was not received")

        self.assertEqual(received[0].event_type, "paper.processed")


if __name__ == "__main__":
    unittest.main()
