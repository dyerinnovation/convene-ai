"""FastAPI application entry point for the Convene AI task engine."""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager, suppress
from typing import TYPE_CHECKING

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------


class TaskEngineSettings(BaseSettings):
    """Task engine configuration from environment variables.

    Attributes:
        database_url: Async PostgreSQL connection string.
        redis_url: Redis connection string.
        extraction_window_seconds: Transcript buffer window for extraction.
    """

    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+asyncpg://convene:convene@localhost:5432/convene"
    redis_url: str = "redis://localhost:6379/0"
    extraction_window_seconds: int = 180


# ---------------------------------------------------------------------------
# Extraction consumer placeholder
# ---------------------------------------------------------------------------


async def _run_extraction_consumer(
    settings: TaskEngineSettings,
) -> None:
    """Consume transcript.segment.final events from Redis Streams.

    Buffers segments into configurable time windows, then sends
    each window to the TaskExtractor for LLM-powered extraction.
    This is a long-running coroutine intended to be launched as a
    background task at startup.

    Args:
        settings: Task engine configuration.
    """
    logger.info(
        "Starting extraction consumer (window=%ds, redis=%s)",
        settings.extraction_window_seconds,
        settings.redis_url,
    )

    # In a full implementation this would:
    # 1. Connect to Redis Streams
    # 2. Read transcript.segment.final events in a consumer group
    # 3. Buffer segments into time windows
    # 4. Send each window to TaskExtractor.extract_from_segments()
    # 5. Run TaskDeduplicator.deduplicate() on results
    # 6. Emit task.created events back to Redis Streams

    while True:
        await asyncio.sleep(settings.extraction_window_seconds)
        logger.debug("Extraction consumer heartbeat")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

_consumer_task: asyncio.Task[None] | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown lifecycle.

    Starts the extraction consumer as a background task on startup
    and cancels it on shutdown.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control back to the ASGI server while the app is running.
    """
    global _consumer_task

    settings = TaskEngineSettings()
    logger.info("task-engine starting up")
    _consumer_task = asyncio.create_task(_run_extraction_consumer(settings))
    try:
        yield
    finally:
        logger.info("task-engine shutting down")
        if _consumer_task is not None:
            _consumer_task.cancel()
            with suppress(asyncio.CancelledError):
                await _consumer_task


app = FastAPI(
    title="Convene AI Task Engine",
    description="LLM-powered task extraction from meeting transcripts",
    version="0.1.0",
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    """Response model for the health check endpoint.

    Attributes:
        status: Current health status of the service.
        service: Name of the service reporting health.
    """

    status: str
    service: str


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return the health status of the task engine.

    Returns:
        HealthResponse with status and service name.
    """
    return HealthResponse(status="healthy", service="task-engine")
