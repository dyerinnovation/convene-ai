# Convene AI

## Project Overview
Convene AI is a voice-first AI agent that dials into meetings via phone (Twilio), listens for commitments, extracts tasks, maintains persistent memory across meetings, and eventually speaks to report progress. The core insight: the AI is a meeting participant, not just a transcriber.

## Architecture
This is a Python monorepo managed with `uv` workspaces. The project is organized into shared packages and independent services.

### Packages (shared libraries)
- `packages/convene-core/` — Domain models (Pydantic v2), event definitions, abstract interfaces
- `packages/convene-providers/` — STT, TTS, and LLM provider implementations behind ABCs
- `packages/convene-memory/` — Four-layer memory system (working, short-term, long-term, structured)

### Services (independently runnable)
- `services/api-server/` — FastAPI REST + WebSocket API for dashboard and integrations
- `services/audio-service/` — Twilio Media Streams handler, audio pipeline, STT streaming
- `services/task-engine/` — Redis Streams consumer, LLM-powered task extraction workers
- `services/worker/` — Background jobs: notifications, Slack integration, calendar sync

### Infrastructure
- PostgreSQL 16 with pgvector extension — single database for relational + vector storage
- Redis 7 — event bus (Streams), working memory cache, pub/sub for real-time updates
- Twilio — outbound calls to meeting dial-in numbers, bidirectional audio via Media Streams

## Tech Stack & Conventions
- **Python 3.12+** with strict type hints everywhere
- **uv** for package management and workspaces (NOT pip, NOT poetry)
- **ruff** for linting and formatting (replaces black, isort, flake8)
- **mypy** in strict mode for type checking
- **pytest** with async support (pytest-asyncio) for testing
- **Pydantic v2** for all data models — use model_validator and field_validator
- **SQLAlchemy 2.0** async style with mapped_column for ORM models
- **Alembic** for database migrations
- **FastAPI** with dependency injection for API endpoints
- **asyncio** throughout — no blocking calls in async code paths

## Key Design Principles
1. **Provider abstraction via ABCs**: Every external service (STT, TTS, LLM, phone) has an abstract base class. Implementations are swappable without changing business logic.
2. **Event-driven between services**: Services communicate via Redis Streams events, never direct calls. The audio service publishes transcript segments; the task engine consumes them.
3. **Phone-first meeting access**: We dial into meetings via Twilio, not platform-specific bot SDKs. This works on every platform with a dial-in number.
4. **Pydantic models for API, SQLAlchemy for persistence**: Keep them separate. API models in convene-core, ORM models alongside the service that owns the table.
5. **Fail gracefully**: If STT drops, buffer audio and retry. If LLM extraction fails, queue for retry. Never lose meeting data.

## Code Style
- Use `async def` for all I/O operations
- Type hint every function signature and return value
- Docstrings on public methods (Google style)
- No `# type: ignore` without explanation
- Use `logging` module with structured log format (JSON in production)
- Environment variables for all config — never hardcode secrets
- Tests alongside code in `tests/` directories within each package/service

## File Naming
- Snake_case for all Python files
- Models: `models/task.py`, `models/meeting.py`
- Interfaces: `interfaces/stt.py`, `interfaces/llm.py`
- Implementations: `providers/assemblyai_stt.py`, `providers/anthropic_llm.py`

## Running Locally
```bash
# Start infrastructure
docker compose up -d postgres redis

# Install dependencies
uv sync

# Run migrations
uv run alembic upgrade head

# Start services (each in a separate terminal)
uv run uvicorn services.api_server.main:app --reload --port 8000
uv run python -m services.audio_service.main
uv run python -m services.task_engine.main
uv run python -m services.worker.main
```

## Environment Variables
```
# Database
DATABASE_URL=postgresql+asyncpg://convene:convene@localhost:5432/convene

# Redis
REDIS_URL=redis://localhost:6379/0

# Twilio
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

# STT Providers
ASSEMBLYAI_API_KEY=
DEEPGRAM_API_KEY=

# LLM Providers
ANTHROPIC_API_KEY=

# TTS Providers (Phase 2)
CARTESIA_API_KEY=
ELEVENLABS_API_KEY=
```

## Current Phase
Phase 1 — Listen & Extract. The agent dials into meetings, transcribes, extracts tasks, and builds persistent memory. No speaking yet.

## What NOT to Do
- Don't use platform-specific meeting SDKs (Zoom SDK, Teams SDK) — we use phone dial-in
- Don't use Poetry or pip — use uv exclusively
- Don't use synchronous database calls — always use async SQLAlchemy
- Don't put business logic in API endpoints — use service layer functions
- Don't skip type hints — mypy strict mode is enforced

## Package Implementation Details
- See `claude_docs/Convene_Core_Patterns.md` for convene-core package patterns (models, events, interfaces, database)
- See `claude_docs/Provider_Patterns.md` for provider ABC signatures, third-party library conventions, and registry usage
- See `claude_docs/Memory_Architecture.md` for the four-layer memory system design and ORM-to-domain conversion patterns
- See `claude_docs/Service_Patterns.md` for service layer conventions (health endpoints, lifespan, settings, DI, route organization)

## Infrastructure
- See `claude_docs/DGX_Spark_Reference.md` for DGX Spark connection details, K8s patterns, and deployment gotchas
- See `charts/stt/` for the Whisper STT Helm chart deployed on DGX Spark

## CoWork Coordination
- See `docs/TASKLIST.md` for the ordered development task queue
- See `docs/cowork-tasks/` for scheduled task instructions
- See `docs/SETUP_GUIDE.md` for full CoWork setup documentation
