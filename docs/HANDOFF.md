# Convene AI — Handoff Notes

> This file is the shift-change log between Jonathan and CoWork scheduled tasks.
> Before starting any work, READ THIS FILE to understand the current state.
> After finishing work, OVERWRITE this section with your handoff notes.
>
> Think of it like passing a baton — the next person (human or AI) needs to know
> what just happened and what to watch out for.

---

## Latest Handoff

**Author:** Jonathan
**Date:** 2026-02-27
**What I did:** Added 4 local/free-tier providers (WhisperSTT, PiperTTS, OllamaLLM, GroqLLM), mock providers for unit testing, provider setup documentation for all 10 providers, and updated the registry. 96 tests passing.
**Branch:** main
**Merge status:** N/A — working directly on main
**Warnings:**
- Initial Alembic migration has NOT been generated yet — run `docker compose up -d` then `uv run alembic revision --autogenerate -m "initial"` before first use
- Optional deps must be installed separately: `uv sync --all-extras` to get faster-whisper, piper-tts, groq
- The `from __future__ import annotations` + Pydantic v2 pattern requires `model_rebuild()` calls — see `events/definitions.py`
- `tests/__init__.py` files were removed from all packages to fix namespace collision — do NOT re-add them
- Groq is recommended for local dev (free tier, fastest inference, no credit card needed)
**Dependencies introduced:** faster-whisper (optional), piper-tts (optional), groq (optional)

---

## Handoff Protocol

When writing your handoff, include:

1. **Author** — "Jonathan" or "CoWork (scheduled)"
2. **Date** — When you finished
3. **What I did** — 1-2 sentence summary
4. **Branch** — Which branch your work is on
5. **Merge status** — "Merged to main" or "Ready for review on branch X"
6. **Warnings** — Anything the next session MUST know (incomplete work, fragile code, don't touch X)
7. **Dependencies introduced** — Any new packages added
