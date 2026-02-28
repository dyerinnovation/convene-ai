"""Meeting CRUD endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field

from convene_core.models.meeting import MeetingStatus

router = APIRouter(prefix="/meetings", tags=["meetings"])


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class MeetingCreateRequest(BaseModel):
    """Request body for creating a new meeting.

    Attributes:
        platform: Meeting platform (e.g. "zoom", "teams").
        dial_in_number: Phone number to dial into the meeting.
        meeting_code: Access code for the meeting.
        title: Optional human-readable meeting title.
        scheduled_at: When the meeting is scheduled to start.
    """

    platform: str
    dial_in_number: str
    meeting_code: str
    title: str | None = None
    scheduled_at: datetime


class MeetingResponse(BaseModel):
    """Response model for a single meeting.

    Attributes:
        id: Unique meeting identifier.
        platform: Meeting platform name.
        dial_in_number: Phone dial-in number.
        meeting_code: Meeting access code.
        title: Human-readable meeting title.
        scheduled_at: Scheduled start time.
        started_at: Actual start time.
        ended_at: End time.
        status: Current meeting status.
        created_at: Record creation timestamp.
        updated_at: Record last-update timestamp.
    """

    id: UUID
    platform: str
    dial_in_number: str
    meeting_code: str
    title: str | None = None
    scheduled_at: datetime
    started_at: datetime | None = None
    ended_at: datetime | None = None
    status: MeetingStatus
    created_at: datetime
    updated_at: datetime


class MeetingListResponse(BaseModel):
    """Paginated list of meetings.

    Attributes:
        items: List of meeting response objects.
        total: Total number of meetings matching the query.
    """

    items: list[MeetingResponse]
    total: int = Field(ge=0)


# ---------------------------------------------------------------------------
# Placeholder data factory
# ---------------------------------------------------------------------------

_PLACEHOLDER = MeetingResponse(
    id=UUID("00000000-0000-0000-0000-000000000001"),
    platform="zoom",
    dial_in_number="+15551234567",
    meeting_code="123456#",
    title="Weekly Standup",
    scheduled_at=datetime(2026, 1, 1, 10, 0, 0),
    started_at=None,
    ended_at=None,
    status=MeetingStatus.SCHEDULED,
    created_at=datetime(2026, 1, 1, 9, 0, 0),
    updated_at=datetime(2026, 1, 1, 9, 0, 0),
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=MeetingListResponse)
async def list_meetings() -> MeetingListResponse:
    """List all meetings.

    Returns:
        MeetingListResponse containing placeholder meeting data.
    """
    return MeetingListResponse(items=[_PLACEHOLDER], total=1)


@router.post("", response_model=MeetingResponse, status_code=201)
async def create_meeting(body: MeetingCreateRequest) -> MeetingResponse:
    """Create a new meeting.

    Args:
        body: The meeting creation payload.

    Returns:
        MeetingResponse with the newly created meeting data.
    """
    return MeetingResponse(
        id=UUID("00000000-0000-0000-0000-000000000002"),
        platform=body.platform,
        dial_in_number=body.dial_in_number,
        meeting_code=body.meeting_code,
        title=body.title,
        scheduled_at=body.scheduled_at,
        started_at=None,
        ended_at=None,
        status=MeetingStatus.SCHEDULED,
        created_at=body.scheduled_at,
        updated_at=body.scheduled_at,
    )


@router.get("/{meeting_id}", response_model=MeetingResponse)
async def get_meeting(meeting_id: UUID) -> MeetingResponse:
    """Get a single meeting by ID.

    Args:
        meeting_id: The UUID of the meeting to retrieve.

    Returns:
        MeetingResponse for the requested meeting.
    """
    return MeetingResponse(
        id=meeting_id,
        platform=_PLACEHOLDER.platform,
        dial_in_number=_PLACEHOLDER.dial_in_number,
        meeting_code=_PLACEHOLDER.meeting_code,
        title=_PLACEHOLDER.title,
        scheduled_at=_PLACEHOLDER.scheduled_at,
        started_at=_PLACEHOLDER.started_at,
        ended_at=_PLACEHOLDER.ended_at,
        status=_PLACEHOLDER.status,
        created_at=_PLACEHOLDER.created_at,
        updated_at=_PLACEHOLDER.updated_at,
    )
