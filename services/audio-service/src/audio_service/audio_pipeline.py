"""Audio pipeline for transcoding and streaming to STT providers."""

from __future__ import annotations

import logging
import struct
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from convene_core.interfaces.stt import STTProvider
    from convene_core.models.transcript import TranscriptSegment

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mu-law decoding table
# ---------------------------------------------------------------------------
# Pre-computed mu-law to 16-bit linear PCM lookup (ITU-T G.711).  Each
# mu-law byte maps to a signed 16-bit integer.

_MULAW_BIAS = 33
_MULAW_CLIP = 0x1FFF

_MULAW_DECODE_TABLE: list[int] = []


def _build_mulaw_table() -> list[int]:
    """Build the mu-law to PCM16 decode lookup table.

    Returns:
        A list of 256 signed 16-bit PCM values.
    """
    table: list[int] = []
    for i in range(256):
        val = ~i
        sign = val & 0x80
        exponent = (val >> 4) & 0x07
        mantissa = val & 0x0F
        sample = ((mantissa << 3) + _MULAW_BIAS) << exponent
        sample -= _MULAW_BIAS
        if sign:
            sample = -sample
        # Clamp to signed 16-bit range
        sample = max(-32768, min(32767, sample))
        table.append(sample)
    return table


_MULAW_DECODE_TABLE = _build_mulaw_table()

# ---------------------------------------------------------------------------
# Linear interpolation upsampler: 8 kHz -> 16 kHz
# ---------------------------------------------------------------------------


def _upsample_8k_to_16k(samples: list[int]) -> list[int]:
    """Upsample PCM16 samples from 8 kHz to 16 kHz via linear interpolation.

    For each pair of consecutive samples, an interpolated sample is inserted
    between them, effectively doubling the sample rate.

    Args:
        samples: List of signed 16-bit PCM values at 8 kHz.

    Returns:
        List of signed 16-bit PCM values at 16 kHz.
    """
    if not samples:
        return []

    out: list[int] = []
    for i in range(len(samples) - 1):
        out.append(samples[i])
        # Interpolated midpoint
        mid = (samples[i] + samples[i + 1]) // 2
        out.append(mid)
    # Append last sample and duplicate it for the interpolation pair
    out.append(samples[-1])
    out.append(samples[-1])
    return out


class AudioPipeline:
    """Transcodes Twilio mulaw 8 kHz audio to PCM16 16 kHz and streams
    through an STT provider.

    Attributes:
        _stt: The speech-to-text provider to stream audio to.
        _started: Whether the STT stream has been started.
    """

    def __init__(self, stt_provider: STTProvider) -> None:
        """Initialise the audio pipeline.

        Args:
            stt_provider: An STT provider implementing the STTProvider ABC.
        """
        self._stt = stt_provider
        self._started = False

    async def _ensure_started(self) -> None:
        """Start the STT stream if it hasn't been started yet."""
        if not self._started:
            await self._stt.start_stream()
            self._started = True

    async def process_audio(self, chunk: bytes) -> None:
        """Transcode a mulaw 8 kHz audio chunk and send to STT.

        Decodes the mu-law encoded bytes to linear PCM16, upsamples
        from 8 kHz to 16 kHz, and forwards the result to the
        configured STT provider.

        Args:
            chunk: Raw mu-law 8 kHz audio bytes from Twilio.
        """
        await self._ensure_started()
        pcm16_bytes = self._transcode_mulaw_to_pcm16(chunk)
        await self._stt.send_audio(pcm16_bytes)

    async def get_segments(self) -> AsyncIterator[TranscriptSegment]:
        """Yield finalised transcript segments from the STT provider.

        Yields:
            TranscriptSegment instances as they become available.
        """
        async for segment in self._stt.get_transcript():
            yield segment

    async def close(self) -> None:
        """Close the STT stream and release resources."""
        if self._started:
            await self._stt.close()
            self._started = False

    @staticmethod
    def _transcode_mulaw_to_pcm16(data: bytes) -> bytes:
        """Convert mu-law 8 kHz audio to linear PCM16 16 kHz.

        Decodes each byte using the mu-law lookup table, then
        upsamples from 8 kHz to 16 kHz using linear interpolation.

        Args:
            data: Raw mu-law encoded bytes.

        Returns:
            PCM16 16 kHz mono audio as bytes (little-endian signed 16-bit).
        """
        # Decode mu-law -> PCM16 samples at 8 kHz
        samples_8k: list[int] = [_MULAW_DECODE_TABLE[byte] for byte in data]

        # Upsample 8 kHz -> 16 kHz
        samples_16k = _upsample_8k_to_16k(samples_8k)

        # Pack as little-endian signed 16-bit
        return struct.pack(f"<{len(samples_16k)}h", *samples_16k)
