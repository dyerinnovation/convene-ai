"""Cartesia text-to-speech provider."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import httpx

from convene_core.interfaces.tts import TTSProvider, Voice

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

logger = logging.getLogger(__name__)

_CARTESIA_BASE_URL = "https://api.cartesia.ai"
_TTS_BYTES_ENDPOINT = f"{_CARTESIA_BASE_URL}/tts/bytes"
_VOICES_ENDPOINT = f"{_CARTESIA_BASE_URL}/voices"
_AUDIO_CHUNK_SIZE = 4096


class CartesiaTTS(TTSProvider):
    """Cartesia text-to-speech provider.

    Synthesizes speech via Cartesia's HTTP streaming API and
    retrieves available voices.
    """

    def __init__(
        self,
        api_key: str,
        voice_id: str = "default",
        model_id: str = "sonic-english",
    ) -> None:
        """Initialize the Cartesia TTS provider.

        Args:
            api_key: Cartesia API key for authentication.
            voice_id: Default voice identifier for synthesis.
            model_id: Cartesia model to use for synthesis.
        """
        self._api_key = api_key
        self._voice_id = voice_id
        self._model_id = model_id
        self._client = httpx.AsyncClient(
            headers={
                "X-API-Key": self._api_key,
                "Cartesia-Version": "2024-06-10",
                "Content-Type": "application/json",
            },
            timeout=httpx.Timeout(30.0, connect=10.0),
        )

    async def synthesize(self, text: str) -> AsyncIterator[bytes]:
        """Synthesize text into streaming audio bytes via Cartesia.

        Sends a POST request to Cartesia's TTS bytes endpoint and
        yields audio chunks as they arrive.

        Args:
            text: The text to synthesize into speech.

        Yields:
            Audio bytes in the provider's output format (PCM/WAV).
        """
        payload: dict[str, Any] = {
            "model_id": self._model_id,
            "transcript": text,
            "voice": {
                "mode": "id",
                "id": self._voice_id,
            },
            "output_format": {
                "container": "raw",
                "encoding": "pcm_s16le",
                "sample_rate": 24000,
            },
        }

        async with self._client.stream("POST", _TTS_BYTES_ENDPOINT, json=payload) as response:
            response.raise_for_status()
            async for chunk in response.aiter_bytes(
                chunk_size=_AUDIO_CHUNK_SIZE,
            ):
                yield chunk

    async def get_voices(self) -> list[Voice]:
        """Retrieve available voices from Cartesia.

        Returns:
            List of Voice objects with id, name, and language.
        """
        response = await self._client.get(_VOICES_ENDPOINT)
        response.raise_for_status()
        data: list[dict[str, Any]] = response.json()

        voices: list[Voice] = []
        for entry in data:
            voice_id: str = entry.get("id", "")
            name: str = entry.get("name", "")
            language: str = entry.get("language", "en-US")
            if voice_id and name:
                voices.append(Voice(id=voice_id, name=name, language=language))

        logger.info("Fetched %d voices from Cartesia.", len(voices))
        return voices

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()
