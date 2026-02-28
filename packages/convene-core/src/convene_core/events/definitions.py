"""Event definitions for inter-service communication."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, ClassVar
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from convene_core.models.decision import Decision  # noqa: TC001
from convene_core.models.task import Task, TaskStatus  # noqa: TC001
from convene_core.models.transcript import TranscriptSegment  # noqa: TC001


def _utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(tz=UTC)


class BaseEvent(BaseModel):
    """Base class for all domain events.

    Attributes:
        event_id: Unique identifier for this event instance.
        timestamp: When the event was created (UTC).
    """

    event_id: UUID = Field(default_factory=uuid4)
    event_type: ClassVar[str] = "base_event"
    timestamp: datetime = Field(default_factory=_utc_now)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the event to a dictionary including event_type.

        Returns:
            Dictionary representation of the event with event_type field.
        """
        data = self.model_dump(mode="json")
        data["event_type"] = self.event_type
        return data


class MeetingStarted(BaseEvent):
    """Emitted when a meeting begins.

    Attributes:
        meeting_id: ID of the meeting that started.
    """

    event_type: ClassVar[str] = "meeting.started"
    meeting_id: UUID


class MeetingEnded(BaseEvent):
    """Emitted when a meeting ends.

    Attributes:
        meeting_id: ID of the meeting that ended.
    """

    event_type: ClassVar[str] = "meeting.ended"
    meeting_id: UUID


class TranscriptSegmentFinal(BaseEvent):
    """Emitted when a final transcript segment is available.

    Attributes:
        meeting_id: ID of the meeting the segment belongs to.
        segment: The finalized transcript segment.
    """

    event_type: ClassVar[str] = "transcript.segment.final"
    meeting_id: UUID
    segment: TranscriptSegment


class TaskCreated(BaseEvent):
    """Emitted when a new task is extracted from a meeting.

    Attributes:
        task: The newly created task.
    """

    event_type: ClassVar[str] = "task.created"
    task: Task


class TaskUpdated(BaseEvent):
    """Emitted when an existing task is updated.

    Attributes:
        task: The updated task.
        previous_status: The status before the update.
    """

    event_type: ClassVar[str] = "task.updated"
    task: Task
    previous_status: TaskStatus


class DecisionRecorded(BaseEvent):
    """Emitted when a decision is recorded during a meeting.

    Attributes:
        decision: The recorded decision.
    """

    event_type: ClassVar[str] = "decision.recorded"
    decision: Decision


# Rebuild models to resolve forward references from __future__ annotations
TranscriptSegmentFinal.model_rebuild()
TaskCreated.model_rebuild()
TaskUpdated.model_rebuild()
DecisionRecorded.model_rebuild()
