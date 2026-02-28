# Convene AI — Development Progress Log

> Append-only log of completed work. Each entry is written by whoever completed
> the work — either CoWork (scheduled) or Jonathan (manual session).
> Never delete or overwrite previous entries.

---

<!-- New entries go at the top -->

## 2026-02-27 — Local/Free Providers, Mock Providers, Provider Docs

**Roadmap items:** Local providers for API-free development, mock providers for testing, provider setup documentation
**Branch:** main
**Author:** Jonathan (manual session with Claude Code)

### Changes

**New providers (4):**
- `WhisperSTT` — Local STT using faster-whisper (CTranslate2), no API key, CPU-optimized int8 inference
- `PiperTTS` — Local TTS using Piper ONNX neural voices, no API key, on-device synthesis
- `OllamaLLM` — Local LLM via Ollama REST API (httpx), no API key, default model: mistral
- `GroqLLM` — Free-tier cloud LLM using Groq SDK (AsyncGroq), LPU hardware, default model: llama-3.1-8b-instant

**Mock providers for testing:**
- `MockSTT`, `MockTTS`, `MockLLM` — Deterministic test doubles that return pre-configured fixtures

**Registry updates:**
- Registered all 4 new providers (whisper, piper, ollama, groq) — total: 3 STT, 3 TTS, 3 LLM
- Updated `__init__.py` re-exports for stt/, tts/, llm/ subpackages

**Provider documentation (10 files in docs/providers/):**
- README.md — Provider matrix with comparison table
- Individual setup guides for all 10 providers (whisper, assemblyai, deepgram, piper, cartesia, elevenlabs, ollama, groq, anthropic)

**Configuration updates:**
- `.env.example` — Added OLLAMA_HOST, OLLAMA_MODEL, GROQ_API_KEY, GROQ_MODEL
- `pyproject.toml` — Added optional deps: whisper, piper, groq
- Removed `tests/__init__.py` from all packages to fix namespace collision with multiple test directories

### Quality Check Results
- ruff: ✅ No issues
- ruff format: ✅ All files formatted
- pytest: ✅ 96 passed, 0 failed (48 original + 48 new)

### Notes
- Initial Alembic migration still not generated (Docker not running)
- Optional deps (faster-whisper, piper-tts, groq) must be installed with `uv sync --all-extras` for full test coverage
- Groq provider requires free API key from console.groq.com (no credit card)

### Blockers
None

### Next Up
- Start Docker and generate initial Alembic migration
- Write integration tests for providers (requires running Ollama, Groq API key)

---

## 2026-02-27 — Phase 1A Bootstrap: Monorepo & Domain Models

**Roadmap items:** All Phase 1A items (16 of 17) + Phase 1B provider ABCs and implementations (7 of 8)
**Branch:** main
**Author:** Jonathan (manual session with Claude Code)

### Changes

**Documentation fixes:**
- Fixed `scheduled-tasks` → `cowork-tasks` path references in SETUP_GUIDE.md and cowork-tasks/README.md
- Renamed ROADMAP-TASKLIST.md → TASKLIST.md, updated all references across docs
- Added CoWork Edit Protocol section to TASKLIST.md
- Updated VISION.md with "Giving Agents a Seat at the Table" section
- Replaced bootstrap CLAUDE.md with project conventions CLAUDE.md
- Moved bootstrap instructions to docs/BOOTSTRAP_REFERENCE.md

**Root configuration:**
- pyproject.toml (uv workspace with 7 members)
- docker-compose.yml (PostgreSQL 16 pgvector + Redis 7)
- .env.example, ruff.toml, mypy.ini
- .github/workflows/ci.yml (lint, type-check, test with services)
- .gitignore

**Packages:**
- `packages/convene-core/` — Pydantic v2 domain models (Meeting, Participant, Task, Decision, TranscriptSegment, AgentConfig), event definitions (6 event types), provider ABCs (STT, TTS, LLM), SQLAlchemy ORM models, Alembic config, async session factory
- `packages/convene-providers/` — STT (AssemblyAI, Deepgram), TTS (Cartesia, ElevenLabs), LLM (Anthropic), provider registry
- `packages/convene-memory/` — Working (Redis), short-term (SQL), long-term (pgvector), structured memory layers

**Services:**
- `services/api-server/` — FastAPI app with health check, meeting/task/agent CRUD routes, DI, CORS middleware
- `services/audio-service/` — Twilio handler, audio pipeline (mulaw→PCM16), meeting dialer
- `services/task-engine/` — Task extractor, deduplicator, health check
- `services/worker/` — Slack bot, calendar sync, notification service

**Tests:**
- 48 tests: 32 model tests + 16 event tests — all passing

### Quality Check Results
- ruff: ✅ No issues
- ruff format: ✅ All files formatted
- pytest: ✅ 48 passed, 0 failed

### Notes
- Initial Alembic migration not generated (requires running database)
- Provider registry integration tests deferred (requires API keys)
- `from __future__ import annotations` requires `model_rebuild()` on Pydantic models that reference other models in events
- All workspace packages need `[tool.hatch.build.targets.wheel] packages = ["src/package_name"]` for hatchling to find src layout

### Blockers
None

### Next Up
- Create initial Alembic migration (requires `docker compose up -d`)
- Write integration tests for provider registry
