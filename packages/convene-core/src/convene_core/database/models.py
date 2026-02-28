"""SQLAlchemy 2.0 ORM models for Convene AI."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlalchemy import ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from convene_core.database.base import Base

if TYPE_CHECKING:
    from datetime import date, datetime


class MeetingORM(Base):
    """ORM model for meetings table.

    Attributes:
        id: Primary key UUID.
        platform: Meeting platform identifier.
        dial_in_number: Phone number to dial into the meeting.
        meeting_code: Access code for the meeting.
        title: Optional human-readable meeting title.
        scheduled_at: Scheduled start time.
        started_at: Actual start time.
        ended_at: Actual end time.
        status: Current meeting status.
        created_at: Record creation timestamp.
        updated_at: Record update timestamp.
    """

    __tablename__ = "meetings"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    platform: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    dial_in_number: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    meeting_code: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    title: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)
    scheduled_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(sa.String(20), nullable=False, default="scheduled")
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )

    tasks: Mapped[list[TaskORM]] = relationship(back_populates="meeting", lazy="selectin")
    decisions: Mapped[list[DecisionORM]] = relationship(back_populates="meeting", lazy="selectin")
    transcript_segments: Mapped[list[TranscriptSegmentORM]] = relationship(
        back_populates="meeting", lazy="selectin"
    )

    __table_args__ = (Index("ix_meetings_status", "status"),)


class ParticipantORM(Base):
    """ORM model for participants table.

    Attributes:
        id: Primary key UUID.
        name: Display name of the participant.
        email: Optional email address.
        speaker_id: Speaker identifier from diarization.
        role: Participant role in the meeting.
        created_at: Record creation timestamp.
    """

    __tablename__ = "participants"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)
    speaker_id: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    role: Mapped[str] = mapped_column(sa.String(20), nullable=False, default="participant")
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )


class TaskORM(Base):
    """ORM model for tasks table.

    Attributes:
        id: Primary key UUID.
        meeting_id: Foreign key to meetings table.
        description: Task description.
        assignee_id: Foreign key to participants table.
        due_date: Optional due date.
        priority: Task priority level.
        status: Current task status.
        dependencies: JSON array of dependent task UUIDs.
        source_utterance: Original transcript text.
        created_at: Record creation timestamp.
        updated_at: Record update timestamp.
    """

    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    meeting_id: Mapped[UUID] = mapped_column(sa.Uuid, ForeignKey("meetings.id"), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    assignee_id: Mapped[UUID | None] = mapped_column(
        sa.Uuid, ForeignKey("participants.id"), nullable=True
    )
    due_date: Mapped[date | None] = mapped_column(sa.Date, nullable=True)
    priority: Mapped[str] = mapped_column(sa.String(20), nullable=False, default="medium")
    status: Mapped[str] = mapped_column(sa.String(20), nullable=False, default="pending")
    dependencies: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    source_utterance: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )

    meeting: Mapped[MeetingORM] = relationship(back_populates="tasks")

    __table_args__ = (
        Index("ix_tasks_meeting_id", "meeting_id"),
        Index("ix_tasks_status", "status"),
        Index("ix_tasks_assignee_id", "assignee_id"),
    )


class DecisionORM(Base):
    """ORM model for decisions table.

    Attributes:
        id: Primary key UUID.
        meeting_id: Foreign key to meetings table.
        description: Decision description.
        decided_by_id: Foreign key to participants table.
        participants_present: JSON array of participant UUIDs.
        created_at: Record creation timestamp.
    """

    __tablename__ = "decisions"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    meeting_id: Mapped[UUID] = mapped_column(sa.Uuid, ForeignKey("meetings.id"), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)
    decided_by_id: Mapped[UUID] = mapped_column(
        sa.Uuid, ForeignKey("participants.id"), nullable=False
    )
    participants_present: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    meeting: Mapped[MeetingORM] = relationship(back_populates="decisions")

    __table_args__ = (Index("ix_decisions_meeting_id", "meeting_id"),)


class TranscriptSegmentORM(Base):
    """ORM model for transcript_segments table.

    Attributes:
        id: Primary key UUID.
        meeting_id: Foreign key to meetings table.
        speaker_id: Speaker identifier from diarization.
        text: Transcribed text content.
        start_time: Segment start time in seconds.
        end_time: Segment end time in seconds.
        confidence: STT confidence score.
        created_at: Record creation timestamp.
    """

    __tablename__ = "transcript_segments"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    meeting_id: Mapped[UUID] = mapped_column(sa.Uuid, ForeignKey("meetings.id"), nullable=False)
    speaker_id: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    text: Mapped[str] = mapped_column(sa.Text, nullable=False)
    start_time: Mapped[float] = mapped_column(sa.Float, nullable=False)
    end_time: Mapped[float] = mapped_column(sa.Float, nullable=False)
    confidence: Mapped[float] = mapped_column(sa.Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )

    meeting: Mapped[MeetingORM] = relationship(back_populates="transcript_segments")

    __table_args__ = (Index("ix_transcript_segments_meeting_id", "meeting_id"),)


class AgentConfigORM(Base):
    """ORM model for agent_configs table.

    Attributes:
        id: Primary key UUID.
        name: Agent name.
        voice_id: TTS voice identifier.
        system_prompt: System prompt for the agent.
        capabilities: JSON array of capability strings.
        meeting_type_filter: JSON array of meeting type strings.
        created_at: Record creation timestamp.
        updated_at: Record update timestamp.
    """

    __tablename__ = "agent_configs"

    id: Mapped[UUID] = mapped_column(sa.Uuid, primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    voice_id: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    system_prompt: Mapped[str] = mapped_column(sa.Text, nullable=False)
    capabilities: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    meeting_type_filter: Mapped[list | None] = mapped_column(JSONB, nullable=True, default=list)
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
