"""Meeting domain model."""

from __future__ import annotations

import enum
from datetime import UTC, datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class MeetingStatus(enum.StrEnum):
    """Status of a meeting."""

    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


def _utc_now() -> datetime:
    """Return the current UTC datetime."""
    return datetime.now(tz=UTC)


class Meeting(BaseModel):
    """Represents a meeting that the AI agent can dial into.

    Attributes:
        id: Unique meeting identifier.
        platform: Meeting platform (e.g., "zoom", "teams", "meet").
        dial_in_number: Phone number to dial into the meeting.
        meeting_code: Access code for the meeting.
        title: Optional human-readable meeting title.
        scheduled_at: When the meeting is scheduled to start (tz-aware).
        started_at: When the meeting actually started (tz-aware).
        ended_at: When the meeting ended (tz-aware).
        status: Current status of the meeting.
        participants: List of participant UUIDs.
        created_at: When this record was created.
        updated_at: When this record was last updated.
    """

    id: UUID = Field(default_factory=uuid4)
    platform: str
    dial_in_number: str
    meeting_code: str
    title: str | None = None
    scheduled_at: datetime
    started_at: datetime | None = None
    ended_at: datetime | None = None
    status: MeetingStatus = MeetingStatus.SCHEDULED
    participants: list[UUID] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    @model_validator(mode="after")
    def _validate_datetimes(self) -> Meeting:
        """Validate that all datetimes are timezone-aware and time ordering."""
        dt_fields = [
            ("scheduled_at", self.scheduled_at),
            ("started_at", self.started_at),
            ("ended_at", self.ended_at),
            ("created_at", self.created_at),
            ("updated_at", self.updated_at),
        ]
        for name, value in dt_fields:
            if value is not None and value.tzinfo is None:
                msg = f"{name} must be timezone-aware"
                raise ValueError(msg)

        if (
            self.started_at is not None
            and self.ended_at is not None
            and self.started_at > self.ended_at
        ):
            msg = "started_at must be <= ended_at"
            raise ValueError(msg)

        return self
