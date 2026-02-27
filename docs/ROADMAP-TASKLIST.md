# Convene AI — Development Roadmap

> This file is the task queue for both manual and scheduled development sessions.
> The daily build sprint picks the next unchecked, unlocked item and implements it.
>
> **Legend:**
> - `[ ]` — Not started (eligible for scheduled pickup)
> - `[x]` — Completed
> - `🔒` — Locked (Jonathan is working on this — skip it)

---

## Phase 1A: Foundation — Monorepo & Domain Models (Steps 1-2)

- [ ] Initialize uv workspace with root pyproject.toml
- [ ] Create package directory structure (convene-core, convene-providers, convene-memory)
- [ ] Create service directory structure (api-server, audio-service, task-engine, worker)
- [ ] Set up docker-compose.yml with PostgreSQL 16 (pgvector) and Redis 7
- [ ] Create .env.example with all environment variables
- [ ] Set up ruff.toml and mypy.ini with strict settings
- [ ] Create CI workflow (.github/workflows/ci.yml) — ruff, mypy, pytest
- [ ] Implement Meeting Pydantic model with validators
- [ ] Implement Participant Pydantic model
- [ ] Implement Task Pydantic model with status transition validators
- [ ] Implement Decision Pydantic model
- [ ] Implement TranscriptSegment Pydantic model
- [ ] Implement AgentConfig Pydantic model
- [ ] Implement event definitions (convene-core/events/definitions.py)
- [ ] Create SQLAlchemy 2.0 ORM models for all domain entities
- [ ] Set up Alembic configuration with async support
- [ ] Create initial Alembic migration

## Phase 1B: Provider Interfaces & Implementations (Step 3)

- [ ] Implement STTProvider abstract base class
- [ ] Implement TTSProvider abstract base class
- [ ] Implement LLMProvider abstract base class
- [ ] Implement AssemblyAI streaming STT provider (WebSocket + speaker diarization)
- [ ] Implement Deepgram STT provider (alternative provider)
- [ ] Implement Anthropic LLM provider (Claude tool_use for structured extraction)
- [ ] Implement provider registry with factory pattern
- [ ] Write integration tests for provider registry

## Phase 1C: Twilio Audio Pipeline (Step 4)

- [ ] Implement MeetingDialer (outbound call + DTMF meeting code entry)
- [ ] Implement TwilioHandler (FastAPI WebSocket for Media Streams)
- [ ] Implement AudioPipeline (μ-law 8kHz → PCM16 16kHz transcoding)
- [ ] Implement Redis Streams publisher for transcript segments
- [ ] Implement meeting end detection (silence threshold + hangup handling)
- [ ] Implement graceful cleanup and audio buffering on STT failure
- [ ] Write end-to-end test for audio pipeline with mock Twilio

## Phase 1D: Task Extraction & Memory (Step 5)

- [ ] Implement Redis Streams consumer for transcript.segment.final events
- [ ] Implement transcript segment windowing (3-5 min windows with overlap)
- [ ] Implement LLM-powered task extraction pipeline
- [ ] Implement task deduplication against existing tasks
- [ ] Implement task persistence to PostgreSQL
- [ ] Implement task.created / task.updated event emission
- [ ] Implement working memory layer (Redis hash per active meeting)
- [ ] Implement short-term memory layer (recent meeting queries)
- [ ] Implement long-term memory layer (pgvector embeddings of meeting summaries)
- [ ] Implement structured state layer (task/decision indexes)
- [ ] Implement memory context builder (assembles relevant context for LLM)

## Phase 1E: API & Dashboard (Step 6)

- [ ] Implement FastAPI app setup with dependency injection (api-server/main.py)
- [ ] Implement meeting CRUD routes
- [ ] Implement task CRUD routes
- [ ] Implement agent config routes
- [ ] Implement WebSocket endpoint for live transcript streaming
- [ ] Implement API authentication middleware
- [ ] Implement CORS and rate limiting middleware
- [ ] Create OpenAPI schema documentation
- [ ] Scaffold React dashboard (Vite + React + Tailwind)
- [ ] Implement meeting list view (upcoming, active, completed)
- [ ] Implement live transcript view for active meetings
- [ ] Implement task board (kanban: pending, in progress, done, blocked)
- [ ] Implement meeting detail view (transcript + extracted tasks)

## Phase 2: Voice Output (Future)

- [ ] Implement Cartesia TTS provider
- [ ] Implement ElevenLabs TTS provider
- [ ] Implement bidirectional audio pipeline (Twilio → STT + TTS → Twilio)
- [ ] Implement agent speaking logic (when to interject, progress reports)
- [ ] Implement voice activity detection for turn-taking

---

## Notes

{Add notes here about roadmap changes, reordering decisions, or items to add}
