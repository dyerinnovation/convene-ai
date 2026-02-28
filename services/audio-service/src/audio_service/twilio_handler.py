"""Twilio Media Streams WebSocket handler."""

from __future__ import annotations

import base64
import json
import logging
from typing import TYPE_CHECKING

from fastapi import WebSocket, WebSocketDisconnect

if TYPE_CHECKING:
    from audio_service.audio_pipeline import AudioPipeline

logger = logging.getLogger(__name__)


class TwilioHandler:
    """Handles bidirectional audio via Twilio Media Streams protocol.

    The Twilio Media Streams WebSocket sends JSON messages with the
    following event types:
    - ``connected``: Stream connection established.
    - ``start``: Stream metadata (call SID, tracks, etc.).
    - ``media``: Base64-encoded audio payload.
    - ``stop``: Stream has ended.

    Attributes:
        _pipeline: The audio pipeline for transcoding and STT.
    """

    def __init__(self, pipeline: AudioPipeline) -> None:
        """Initialise the handler with an audio pipeline.

        Args:
            pipeline: AudioPipeline instance for processing audio.
        """
        self._pipeline = pipeline

    async def handle_media_stream(self, websocket: WebSocket) -> None:
        """Process incoming Twilio Media Streams messages.

        Accepts the WebSocket connection, then loops over incoming
        messages, dispatching each to the appropriate handler method
        based on the ``event`` field.

        Args:
            websocket: The FastAPI WebSocket connection from Twilio.
        """
        await websocket.accept()
        stream_sid: str | None = None

        try:
            while True:
                raw = await websocket.receive_text()
                message: dict[str, object] = json.loads(raw)
                event = str(message.get("event", ""))

                if event == "connected":
                    logger.info("Twilio Media Stream connected")

                elif event == "start":
                    start_data = message.get("start", {})
                    if isinstance(start_data, dict):
                        stream_sid = str(start_data.get("streamSid", ""))
                    logger.info(
                        "Twilio Media Stream started: sid=%s",
                        stream_sid,
                    )

                elif event == "media":
                    await self._handle_media(message)

                elif event == "stop":
                    logger.info(
                        "Twilio Media Stream stopped: sid=%s",
                        stream_sid,
                    )
                    break

                else:
                    logger.debug("Unknown Twilio event: %s", event)

        except WebSocketDisconnect:
            logger.info("Twilio WebSocket disconnected: sid=%s", stream_sid)
        finally:
            await self._pipeline.close()

    async def _handle_media(self, message: dict[str, object]) -> None:
        """Decode and process a Twilio media event.

        Extracts the base64-encoded payload from the ``media`` field,
        decodes it to raw bytes, and forwards it to the audio pipeline.

        Args:
            message: The parsed JSON message from Twilio.
        """
        media_data = message.get("media", {})
        if not isinstance(media_data, dict):
            return

        payload_b64 = media_data.get("payload")
        if not isinstance(payload_b64, str):
            return

        audio_bytes = base64.b64decode(payload_b64)
        await self._pipeline.process_audio(audio_bytes)
