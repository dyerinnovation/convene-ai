"""Convene AI provider interfaces (ABCs)."""

from __future__ import annotations

from convene_core.interfaces.llm import LLMProvider
from convene_core.interfaces.stt import STTProvider
from convene_core.interfaces.tts import TTSProvider, Voice

__all__ = [
    "LLMProvider",
    "STTProvider",
    "TTSProvider",
    "Voice",
]
