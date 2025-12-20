"""Event schema definitions for cross-module integration."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4


@dataclass(frozen=True)
class EventMessage:
    """Standard event payload for module integration."""

    event_type: str
    source_module: str
    timestamp: str
    payload: Dict[str, Any] = field(default_factory=dict)
    correlation_id: str = field(default_factory=lambda: str(uuid4()))

    @classmethod
    def create(cls, event_type: str, source_module: str, payload: Dict[str, Any]) -> "EventMessage":
        """
        Create a new event message with a UTC timestamp.

        Args:
            event_type: Event type identifier.
            source_module: Originating module name.
            payload: Event payload data.

        Returns:
            EventMessage instance.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        return cls(event_type=event_type, source_module=source_module, timestamp=timestamp, payload=payload)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the event to a JSON-serializable dictionary."""
        return {
            "event_type": self.event_type,
            "source_module": self.source_module,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "correlation_id": self.correlation_id,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventMessage":
        """
        Build an EventMessage from a dictionary.

        Args:
            data: Dictionary containing event fields.

        Returns:
            EventMessage instance.
        """
        return cls(
            event_type=str(data.get("event_type", "")),
            source_module=str(data.get("source_module", "")),
            timestamp=str(data.get("timestamp", "")),
            payload=dict(data.get("payload", {})),
            correlation_id=str(data.get("correlation_id", "")) or str(uuid4()),
        )
