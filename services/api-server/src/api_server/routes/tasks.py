"""Task CRUD endpoints."""

from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field

from convene_core.models.task import TaskPriority, TaskStatus

router = APIRouter(prefix="/tasks", tags=["tasks"])


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class TaskCreateRequest(BaseModel):
    """Request body for creating a new task.

    Attributes:
        meeting_id: ID of the meeting this task was extracted from.
        description: Human-readable description of the task.
        assignee_id: Optional participant assigned to the task.
        due_date: Optional due date.
        priority: Task priority level.
    """

    meeting_id: UUID
    description: str
    assignee_id: UUID | None = None
    due_date: date | None = None
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskStatusUpdateRequest(BaseModel):
    """Request body for updating a task's status.

    Attributes:
        status: The new status to transition to.
    """

    status: TaskStatus


class TaskResponse(BaseModel):
    """Response model for a single task.

    Attributes:
        id: Unique task identifier.
        meeting_id: ID of the originating meeting.
        description: Task description.
        assignee_id: Assigned participant ID.
        due_date: Task due date.
        priority: Priority level.
        status: Current task status.
        dependencies: IDs of tasks this depends on.
        source_utterance: Original transcript text.
        created_at: Record creation timestamp.
        updated_at: Record last-update timestamp.
    """

    id: UUID
    meeting_id: UUID
    description: str
    assignee_id: UUID | None = None
    due_date: date | None = None
    priority: TaskPriority
    status: TaskStatus
    dependencies: list[UUID] = Field(default_factory=list)
    source_utterance: str | None = None
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    """Paginated list of tasks.

    Attributes:
        items: List of task response objects.
        total: Total number of tasks matching the query.
    """

    items: list[TaskResponse]
    total: int = Field(ge=0)


# ---------------------------------------------------------------------------
# Placeholder helpers
# ---------------------------------------------------------------------------


def _utc_now() -> datetime:
    return datetime.now(tz=UTC)


_PLACEHOLDER_MEETING_ID = UUID("00000000-0000-0000-0000-000000000001")

_PLACEHOLDER = TaskResponse(
    id=UUID("00000000-0000-0000-0000-000000000010"),
    meeting_id=_PLACEHOLDER_MEETING_ID,
    description="Follow up on Q1 budget review",
    assignee_id=None,
    due_date=None,
    priority=TaskPriority.MEDIUM,
    status=TaskStatus.PENDING,
    dependencies=[],
    source_utterance="We need to follow up on the Q1 budget review.",
    created_at=_utc_now(),
    updated_at=_utc_now(),
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=TaskListResponse)
async def list_tasks() -> TaskListResponse:
    """List all tasks.

    Returns:
        TaskListResponse containing placeholder task data.
    """
    return TaskListResponse(items=[_PLACEHOLDER], total=1)


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(body: TaskCreateRequest) -> TaskResponse:
    """Create a new task.

    Args:
        body: The task creation payload.

    Returns:
        TaskResponse with the newly created task data.
    """
    now = _utc_now()
    return TaskResponse(
        id=UUID("00000000-0000-0000-0000-000000000011"),
        meeting_id=body.meeting_id,
        description=body.description,
        assignee_id=body.assignee_id,
        due_date=body.due_date,
        priority=body.priority,
        status=TaskStatus.PENDING,
        dependencies=[],
        source_utterance=None,
        created_at=now,
        updated_at=now,
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID) -> TaskResponse:
    """Get a single task by ID.

    Args:
        task_id: The UUID of the task to retrieve.

    Returns:
        TaskResponse for the requested task.
    """
    return TaskResponse(
        id=task_id,
        meeting_id=_PLACEHOLDER.meeting_id,
        description=_PLACEHOLDER.description,
        assignee_id=_PLACEHOLDER.assignee_id,
        due_date=_PLACEHOLDER.due_date,
        priority=_PLACEHOLDER.priority,
        status=_PLACEHOLDER.status,
        dependencies=_PLACEHOLDER.dependencies,
        source_utterance=_PLACEHOLDER.source_utterance,
        created_at=_PLACEHOLDER.created_at,
        updated_at=_PLACEHOLDER.updated_at,
    )


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_status(
    task_id: UUID,
    body: TaskStatusUpdateRequest,
) -> TaskResponse:
    """Update the status of an existing task.

    Validates the status transition before applying. Returns the
    updated task representation.

    Args:
        task_id: The UUID of the task to update.
        body: The status update payload.

    Returns:
        TaskResponse reflecting the updated status.
    """
    now = _utc_now()
    return TaskResponse(
        id=task_id,
        meeting_id=_PLACEHOLDER.meeting_id,
        description=_PLACEHOLDER.description,
        assignee_id=_PLACEHOLDER.assignee_id,
        due_date=_PLACEHOLDER.due_date,
        priority=_PLACEHOLDER.priority,
        status=body.status,
        dependencies=_PLACEHOLDER.dependencies,
        source_utterance=_PLACEHOLDER.source_utterance,
        created_at=_PLACEHOLDER.created_at,
        updated_at=now,
    )
