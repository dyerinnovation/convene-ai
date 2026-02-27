# Convene AI — Claude Code Bootstrap Prompt

> Copy this entire file and paste it into Claude Code to scaffold the project.

---

## CLAUDE.md

```markdown
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
```

---

## Bootstrap Instructions

When pasting this into Claude Code, ask it to:

### Step 1: Create the monorepo structure

```
Create the Convene AI monorepo with the following structure. Use uv workspaces.
Initialize all packages with pyproject.toml files and proper dependency declarations.
Set up docker-compose.yml with PostgreSQL 16 (pgvector) and Redis 7.
Create the CLAUDE.md file at the root from the spec above.

Structure:
convene-ai/
├── CLAUDE.md
├── pyproject.toml              # Root workspace
├── docker-compose.yml
├── .env.example
├── .github/workflows/ci.yml
├── docs/
│   ├── VISION.md
│   └── ROADMAP.md
├── packages/
│   ├── convene-core/
│   │   ├── pyproject.toml
│   │   └── src/convene_core/
│   │       ├── __init__.py
│   │       ├── models/
│   │       │   ├── __init__.py
│   │       │   ├── meeting.py
│   │       │   ├── task.py
│   │       │   ├── participant.py
│   │       │   ├── decision.py
│   │       │   ├── transcript.py
│   │       │   └── agent.py
│   │       ├── events/
│   │       │   ├── __init__.py
│   │       │   └── definitions.py
│   │       └── interfaces/
│   │           ├── __init__.py
│   │           ├── stt.py
│   │           ├── tts.py
│   │           └── llm.py
│   ├── convene-providers/
│   │   ├── pyproject.toml
│   │   └── src/convene_providers/
│   │       ├── __init__.py
│   │       ├── stt/
│   │       │   ├── __init__.py
│   │       │   ├── assemblyai_stt.py
│   │       │   └── deepgram_stt.py
│   │       ├── tts/
│   │       │   ├── __init__.py
│   │       │   ├── cartesia_tts.py
│   │       │   └── elevenlabs_tts.py
│   │       ├── llm/
│   │       │   ├── __init__.py
│   │       │   └── anthropic_llm.py
│   │       └── registry.py
│   └── convene-memory/
│       ├── pyproject.toml
│       └── src/convene_memory/
│           ├── __init__.py
│           ├── working.py
│           ├── short_term.py
│           ├── long_term.py
│           └── structured.py
├── services/
│   ├── api-server/
│   │   ├── pyproject.toml
│   │   └── src/api_server/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── routes/
│   │       │   ├── __init__.py
│   │       │   ├── meetings.py
│   │       │   ├── tasks.py
│   │       │   └── agents.py
│   │       ├── deps.py
│   │       └── middleware.py
│   ├── audio-service/
│   │   ├── pyproject.toml
│   │   └── src/audio_service/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── twilio_handler.py
│   │       ├── audio_pipeline.py
│   │       └── meeting_dialer.py
│   ├── task-engine/
│   │   ├── pyproject.toml
│   │   └── src/task_engine/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── extractor.py
│   │       └── deduplicator.py
│   └── worker/
│       ├── pyproject.toml
│       └── src/worker/
│           ├── __init__.py
│           ├── main.py
│           ├── slack_bot.py
│           ├── calendar_sync.py
│           └── notifications.py
└── alembic/
    ├── alembic.ini
    ├── env.py
    └── versions/
```

### Step 2: Implement core domain models

```
Implement all Pydantic v2 models in packages/convene-core/src/convene_core/models/.
Then implement the corresponding SQLAlchemy 2.0 ORM models.
Create the initial Alembic migration.

Key models:
- Meeting: id (UUID), platform, dial_in_number, meeting_code, scheduled_at, started_at, ended_at, status (scheduled/active/completed/failed)
- Participant: id (UUID), name, email (optional), speaker_id (from diarization)
- Task: id (UUID), meeting_id (FK), description, assignee (FK to Participant), due_date, priority (low/medium/high/critical), status (pending/in_progress/done/blocked), dependencies (list of Task UUIDs), source_utterance, created_at, updated_at
- Decision: id (UUID), meeting_id (FK), description, decided_by (FK to Participant), created_at
- TranscriptSegment: id (UUID), meeting_id (FK), speaker_id, text, start_time, end_time, confidence
- AgentConfig: id (UUID), name, voice_id, system_prompt, capabilities (list), meeting_type_filter (list)

Use proper validators — Task status transitions should be validated. UUIDs for all PKs. Timestamps with timezone.
```

### Step 3: Implement provider interfaces and first providers

```
Implement the abstract base classes in packages/convene-core/src/convene_core/interfaces/:
- STTProvider: start_stream(), send_audio(chunk: bytes), get_transcript() -> AsyncIterator[TranscriptSegment], close()
- TTSProvider: synthesize(text: str) -> AsyncIterator[bytes], list_voices() -> list[Voice]
- LLMProvider: extract_tasks(segments: list[TranscriptSegment], context: MemoryContext) -> list[Task], summarize(segments: list[TranscriptSegment]) -> str

Then implement:
- AssemblyAI STT provider with WebSocket streaming and speaker diarization
- Anthropic LLM provider using Claude for structured task extraction (use tool_use for Pydantic schema output)
- Provider registry in convene-providers/src/convene_providers/registry.py
```

### Step 4: Implement Twilio phone integration

```
Implement the audio service that dials into meetings via Twilio:
- MeetingDialer: takes dial-in number + meeting code, initiates Twilio outbound call, sends DTMF tones for meeting code
- TwilioHandler: FastAPI WebSocket endpoint for Twilio Media Streams, handles bidirectional audio
- AudioPipeline: receives audio from Twilio (μ-law 8kHz), transcodes to PCM16 16kHz, forwards to STT provider

The audio service should:
1. Receive a request to join a meeting (dial-in number + code)
2. Initiate a Twilio outbound call
3. When connected, send DTMF tones for meeting code
4. Open Media Stream WebSocket for bidirectional audio
5. Forward inbound audio to STT provider
6. Publish transcript segments to Redis Streams
7. Detect meeting end (silence > 60s or Twilio hangup) and clean up
```

### Step 5: Implement task extraction and memory

```
Implement the task engine service:
- Subscribe to transcript.segment.final events on Redis Streams
- Buffer segments into 3-5 minute windows with overlap
- Send to Anthropic LLM for structured extraction
- Deduplicate against existing tasks
- Store in PostgreSQL
- Emit task.created / task.updated events

Implement the memory system:
- Working memory: Redis hash per active meeting
- Short-term memory: PostgreSQL queries for recent meetings by team/participants
- Long-term memory: pgvector embeddings of meeting summaries
- Structured state: Task and Decision tables with proper indexes
- Context builder: assemble relevant memory for a given meeting
```

### Step 6: Build API and minimal dashboard

```
Implement the FastAPI API server with routes for meetings, tasks, and agents.
Add a WebSocket endpoint that streams live transcript from Redis pub/sub.
Build a minimal React dashboard (Vite + React + Tailwind) with:
- Meeting list (upcoming, active, completed)
- Live transcript view for active meetings
- Task board (kanban-style: pending, in progress, done, blocked)
- Meeting detail view with transcript + extracted tasks
```

---

## Provider Configuration Reference

### AssemblyAI Streaming STT
```python
# WebSocket URL: wss://api.assemblyai.com/v2/realtime/ws
# Auth: token parameter in URL
# Audio format: PCM16, 16kHz, mono
# Features: speaker_labels=true, word_boost (optional)
# Events: SessionBegins, PartialTranscript, FinalTranscript, SessionTerminated
```

### Twilio Media Streams
```python
# Outbound call: client.calls.create(to=dial_in, from_=twilio_number, twiml=stream_twiml)
# TwiML: <Response><Connect><Stream url="wss://your-server/audio-stream" /></Connect></Response>
# Audio format: mulaw, 8kHz, mono, base64-encoded in JSON messages
# Events: connected, start, media, stop
# For DTMF: use <Play digits="w{meeting_code}#" /> in TwiML (w = 0.5s wait)
```

### Anthropic Claude (Task Extraction)
```python
# Model: claude-sonnet-4-20250514 (or claude-haiku for classification)
# Use tool_use with Pydantic schema for structured extraction
# System prompt should include: meeting context, participant names, open tasks
# Temperature: 0.0 for extraction (deterministic)
# Max tokens: 4096 for extraction responses
```
