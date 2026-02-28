"""Speech-to-text provider implementations."""

from __future__ import annotations

from convene_providers.stt.assemblyai_stt import AssemblyAISTT
from convene_providers.stt.deepgram_stt import DeepgramSTT

__all__ = [
    "AssemblyAISTT",
    "DeepgramSTT",
]
