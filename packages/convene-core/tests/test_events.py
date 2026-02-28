"""Tests for Convene AI event definitions."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from convene_core.events.definitions import (
    BaseEvent,
    DecisionRecorded,
    MeetingEnded,
    MeetingStarted,
    TaskCreated,
    TaskUpdated,
    TranscriptSegmentFinal,
)
from convene_core.models.decision import Decision
from convene_core.models.task import Task, TaskPriority, TaskStatus
from convene_core.models.transcript import TranscriptSegment

MEETING_ID = uuid4()
PARTICIPANT_ID = uuid4()


class TestBaseEvent:
    """Tests for the BaseEvent base class."""

    def test_base_event_defaults(self) -> None:
        """BaseEvent generates event_id and timestamp automatically."""
        event = BaseEvent()
        assert isinstance(event.event_id, UUID)
        assert isinstance(event.timestamp, datetime)
        assert event.timestamp.tzinfo is not None

    def test_base_event_to_dict_includes_event_type(self) -> None:
        """to_dict() includes the event_type class variable."""
        event = BaseEvent()
        data = event.to_dict()
        assert "event_type" in data
        assert data["event_type"] == "base_event"
        assert "event_id" in data
        assert "timestamp" in data


class TestMeetingStarted:
    """Tests for the MeetingStarted event."""

    def test_meeting_started_creation(self) -> None:
        """MeetingStarted event can be created with meeting_id."""
        event = MeetingStarted(meeting_id=MEETING_ID)
        assert event.meeting_id == MEETING_ID
        assert isinstance(event.event_id, UUID)

    def test_meeting_started_event_type(self) -> None:
        """MeetingStarted has correct event_type."""
        event = MeetingStarted(meeting_id=MEETING_ID)
        assert event.to_dict()["event_type"] == "meeting.started"

    def test_meeting_started_to_dict(self) -> None:
        """MeetingStarted to_dict includes meeting_id."""
        event = MeetingStarted(meeting_id=MEETING_ID)
        data = event.to_dict()
        assert data["meeting_id"] == str(MEETING_ID)
        assert data["event_type"] == "meeting.started"


class TestMeetingEnded:
    """Tests for the MeetingEnded event."""

    def test_meeting_ended_creation(self) -> None:
        """MeetingEnded event can be created with meeting_id."""
        event = MeetingEnded(meeting_id=MEETING_ID)
        assert event.meeting_id == MEETING_ID

    def test_meeting_ended_event_type(self) -> None:
        """MeetingEnded has correct event_type."""
        event = MeetingEnded(meeting_id=MEETING_ID)
        assert event.to_dict()["event_type"] == "meeting.ended"


class TestTranscriptSegmentFinal:
    """Tests for the TranscriptSegmentFinal event."""

    def test_creation_with_segment(self) -> None:
        """TranscriptSegmentFinal wraps a TranscriptSegment."""
        segment = TranscriptSegment(
            meeting_id=MEETING_ID,
            speaker_id="spk_001",
            text="We need to ship by Friday",
            start_time=120.0,
            end_time=125.5,
            confidence=0.92,
        )
        event = TranscriptSegmentFinal(
            meeting_id=MEETING_ID,
            segment=segment,
        )
        assert event.segment.text == "We need to ship by Friday"
        assert event.meeting_id == MEETING_ID

    def test_event_type(self) -> None:
        """TranscriptSegmentFinal has correct event_type."""
        segment = TranscriptSegment(
            meeting_id=MEETING_ID,
            text="test",
            start_time=0.0,
            end_time=1.0,
        )
        event = TranscriptSegmentFinal(
            meeting_id=MEETING_ID,
            segment=segment,
        )
        assert event.to_dict()["event_type"] == "transcript.segment.final"

    def test_nested_serialization(self) -> None:
        """to_dict() correctly serializes nested TranscriptSegment."""
        segment = TranscriptSegment(
            meeting_id=MEETING_ID,
            speaker_id="spk_002",
            text="Let's discuss the roadmap",
            start_time=10.0,
            end_time=14.0,
            confidence=0.88,
        )
        event = TranscriptSegmentFinal(
            meeting_id=MEETING_ID,
            segment=segment,
        )
        data = event.to_dict()
        assert "segment" in data
        assert data["segment"]["text"] == "Let's discuss the roadmap"
        assert data["segment"]["speaker_id"] == "spk_002"
        assert data["segment"]["confidence"] == 0.88


class TestTaskCreated:
    """Tests for the TaskCreated event."""

    def test_task_created_event(self) -> None:
        """TaskCreated event wraps a Task."""
        task = Task(
            meeting_id=MEETING_ID,
            description="Update documentation",
            priority=TaskPriority.HIGH,
        )
        event = TaskCreated(task=task)
        assert event.task.description == "Update documentation"
        assert event.to_dict()["event_type"] == "task.created"

    def test_task_created_serialization(self) -> None:
        """TaskCreated to_dict includes full task data."""
        task = Task(
            meeting_id=MEETING_ID,
            description="Fix the bug",
            assignee_id=PARTICIPANT_ID,
        )
        event = TaskCreated(task=task)
        data = event.to_dict()
        assert data["task"]["description"] == "Fix the bug"
        assert data["task"]["assignee_id"] == str(PARTICIPANT_ID)


class TestTaskUpdated:
    """Tests for the TaskUpdated event."""

    def test_task_updated_event(self) -> None:
        """TaskUpdated event tracks previous status."""
        task = Task(
            meeting_id=MEETING_ID,
            description="Deploy v2",
            status=TaskStatus.IN_PROGRESS,
        )
        event = TaskUpdated(
            task=task,
            previous_status=TaskStatus.PENDING,
        )
        assert event.task.status == TaskStatus.IN_PROGRESS
        assert event.previous_status == TaskStatus.PENDING
        assert event.to_dict()["event_type"] == "task.updated"

    def test_task_updated_serialization(self) -> None:
        """TaskUpdated to_dict includes both task and previous_status."""
        task = Task(
            meeting_id=MEETING_ID,
            description="Review PR",
            status=TaskStatus.DONE,
        )
        event = TaskUpdated(
            task=task,
            previous_status=TaskStatus.IN_PROGRESS,
        )
        data = event.to_dict()
        assert data["previous_status"] == "in_progress"
        assert data["task"]["status"] == "done"


class TestDecisionRecorded:
    """Tests for the DecisionRecorded event."""

    def test_decision_recorded_event(self) -> None:
        """DecisionRecorded event wraps a Decision."""
        decision = Decision(
            meeting_id=MEETING_ID,
            description="Use PostgreSQL",
            decided_by_id=PARTICIPANT_ID,
        )
        event = DecisionRecorded(decision=decision)
        assert event.decision.description == "Use PostgreSQL"
        assert event.to_dict()["event_type"] == "decision.recorded"

    def test_decision_recorded_serialization(self) -> None:
        """DecisionRecorded to_dict includes full decision data."""
        p1, p2 = uuid4(), uuid4()
        decision = Decision(
            meeting_id=MEETING_ID,
            description="Migrate to AWS",
            decided_by_id=PARTICIPANT_ID,
            participants_present=[p1, p2],
        )
        event = DecisionRecorded(decision=decision)
        data = event.to_dict()
        assert data["decision"]["description"] == "Migrate to AWS"
        assert len(data["decision"]["participants_present"]) == 2
