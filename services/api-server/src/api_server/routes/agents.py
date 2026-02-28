"""Agent configuration CRUD endpoints."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/agents", tags=["agents"])


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class AgentCreateRequest(BaseModel):
    """Request body for creating a new agent configuration.

    Attributes:
        name: Human-readable agent name.
        voice_id: Optional TTS voice identifier.
        system_prompt: System prompt for the agent.
        capabilities: List of capabilities the agent supports.
        meeting_type_filter: Meeting types this agent should join.
    """

    name: str
    voice_id: str | None = None
    system_prompt: str
    capabilities: list[str] = Field(default_factory=list)
    meeting_type_filter: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """Response model for a single agent configuration.

    Attributes:
        id: Unique agent configuration identifier.
        name: Human-readable agent name.
        voice_id: TTS voice identifier.
        system_prompt: System prompt text.
        capabilities: List of agent capabilities.
        meeting_type_filter: Meeting types this agent handles.
        created_at: Record creation timestamp.
        updated_at: Record last-update timestamp.
    """

    id: UUID
    name: str
    voice_id: str | None = None
    system_prompt: str
    capabilities: list[str] = Field(default_factory=list)
    meeting_type_filter: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class AgentListResponse(BaseModel):
    """Paginated list of agents.

    Attributes:
        items: List of agent response objects.
        total: Total number of agents matching the query.
    """

    items: list[AgentResponse]
    total: int = Field(ge=0)


# ---------------------------------------------------------------------------
# Placeholder helpers
# ---------------------------------------------------------------------------


def _utc_now() -> datetime:
    return datetime.now(tz=UTC)


_PLACEHOLDER = AgentResponse(
    id=UUID("00000000-0000-0000-0000-000000000100"),
    name="Convene Bot",
    voice_id=None,
    system_prompt="You are Convene, an AI meeting assistant.",
    capabilities=["transcribe", "extract_tasks"],
    meeting_type_filter=["standup", "planning"],
    created_at=_utc_now(),
    updated_at=_utc_now(),
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("", response_model=AgentListResponse)
async def list_agents() -> AgentListResponse:
    """List all agent configurations.

    Returns:
        AgentListResponse containing placeholder agent data.
    """
    return AgentListResponse(items=[_PLACEHOLDER], total=1)


@router.post("", response_model=AgentResponse, status_code=201)
async def create_agent(body: AgentCreateRequest) -> AgentResponse:
    """Create a new agent configuration.

    Args:
        body: The agent creation payload.

    Returns:
        AgentResponse with the newly created agent data.
    """
    now = _utc_now()
    return AgentResponse(
        id=UUID("00000000-0000-0000-0000-000000000101"),
        name=body.name,
        voice_id=body.voice_id,
        system_prompt=body.system_prompt,
        capabilities=body.capabilities,
        meeting_type_filter=body.meeting_type_filter,
        created_at=now,
        updated_at=now,
    )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: UUID) -> AgentResponse:
    """Get a single agent configuration by ID.

    Args:
        agent_id: The UUID of the agent to retrieve.

    Returns:
        AgentResponse for the requested agent.
    """
    return AgentResponse(
        id=agent_id,
        name=_PLACEHOLDER.name,
        voice_id=_PLACEHOLDER.voice_id,
        system_prompt=_PLACEHOLDER.system_prompt,
        capabilities=_PLACEHOLDER.capabilities,
        meeting_type_filter=_PLACEHOLDER.meeting_type_filter,
        created_at=_PLACEHOLDER.created_at,
        updated_at=_PLACEHOLDER.updated_at,
    )
