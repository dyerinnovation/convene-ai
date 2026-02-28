"""FastAPI application entry point for the Convene AI audio service."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from audio_service.audio_pipeline import AudioPipeline
from audio_service.twilio_handler import TwilioHandler

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Placeholder STT provider for bootstrapping
# ---------------------------------------------------------------------------
# A real deployment would inject a concrete STTProvider via configuration.
# Here we keep a module-level reference that can be replaced at startup.

_stt_provider = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown lifecycle.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control back to the ASGI server while the app is running.
    """
    logger.info("audio-service starting up")
    yield
    logger.info("audio-service shutting down")


app = FastAPI(
    title="Convene AI Audio Service",
    description="Twilio Media Streams handler and audio pipeline",
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
    """Return the health status of the audio service.

    Returns:
        HealthResponse with status and service name.
    """
    return HealthResponse(status="healthy", service="audio-service")


# ---------------------------------------------------------------------------
# Twilio Media Streams WebSocket
# ---------------------------------------------------------------------------


@app.websocket("/audio-stream")
async def audio_stream(websocket: WebSocket) -> None:
    """WebSocket endpoint for Twilio Media Streams.

    Creates an AudioPipeline with the configured STT provider and
    delegates message handling to TwilioHandler.  When no STT
    provider is configured, the endpoint still accepts connections
    but logs a warning.

    Args:
        websocket: The incoming WebSocket connection from Twilio.
    """
    if _stt_provider is None:
        logger.warning("No STT provider configured; audio will not be transcribed")
        await websocket.accept()
        await websocket.close(code=1011, reason="STT provider not configured")
        return

    pipeline = AudioPipeline(stt_provider=_stt_provider)
    handler = TwilioHandler(pipeline=pipeline)
    await handler.handle_media_stream(websocket)
