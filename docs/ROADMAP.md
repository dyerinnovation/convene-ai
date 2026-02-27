# Convene AI — Feature Roadmap

> This document is structured for Claude Code to pick up individual features and implement them. Each feature includes context, acceptance criteria, and technical notes. Features are ordered by phase and priority within each phase.

---

## Architecture Overview

```
convene-ai/
├── docs/                          # Product docs (you are here)
│   ├── VISION.md                  # Product vision & business case
│   └── ROADMAP.md                 # This file
├── packages/
│   ├── convene-core/              # Domain models, events, interfaces
│   │   ├── models/                # Pydantic models for tasks, meetings, agents
│   │   ├── events/                # Event definitions (Redis Streams)
│   │   └── interfaces/            # Abstract base classes for providers
│   ├── convene-providers/         # STT, TTS, LLM provider implementations
│   │   ├── stt/                   # AssemblyAI, Deepgram, Whisper
│   │   ├── tts/                   # Cartesia, ElevenLabs
│   │   └── llm/                   # Anthropic, OpenAI, local models
│   └── convene-memory/            # Persistent memory layers
│       ├── working.py             # In-memory / Redis current meeting state
│       ├── short_term.py          # Recent meetings (PostgreSQL)
│       ├── long_term.py           # Vectorized summaries (pgvector)
│       └── structured.py          # Tasks, decisions (relational)
├── services/
│   ├── api-server/                # FastAPI REST + WebSocket API
│   ├── audio-service/             # Twilio integration + STT pipeline
│   ├── task-engine/               # LLM-powered task extraction workers
│   └── worker/                    # Background jobs (notifications, integrations)
├── web/                           # Dashboard frontend (React/Next.js)
├── CLAUDE.md                      # Bootstrap prompt for Claude Code
├── pyproject.toml                 # Root workspace config (uv)
└── docker-compose.yml             # Local dev environment
```

### Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.12+ | Pipecat ecosystem, ML tooling, team familiarity |
| API Framework | FastAPI | Async-native, WebSocket support, Pydantic integration |
| Database | PostgreSQL 16 + pgvector | Single DB for relational + vector, proven at scale |
| Cache / Event Bus | Redis Streams | Lightweight pub/sub between services |
| Package Manager | uv | 10-100x faster than pip/Poetry |
| Linting | ruff | Fast, replaces flake8/isort/black |
| Type Checking | mypy (strict) | Catch bugs early with provider abstractions |
| Phone Integration | Twilio Programmable Voice | Dial-in to any meeting platform |
| STT (Primary) | AssemblyAI Universal-Streaming | $0.0025/min, built-in diarization |
| STT (Fallback) | Deepgram Nova-3 | $0.0077/min, lowest latency |
| TTS (Phase 2) | Cartesia Sonic-3 | 40-90ms TTFA, fastest available |
| LLM (Extraction) | Claude Sonnet / GPT-4.1-mini | Structured output for task extraction |
| Container | Docker Compose (dev), fly.io or Railway (prod) | Simple deployment for solo founder |

---

## Phase 1 — Listen & Extract

> Goal: Agent dials into meetings, transcribes, extracts tasks, builds persistent memory. No speaking.

### F1.1 — Project Scaffolding ⭐ START HERE
**Context**: Set up the monorepo with uv workspaces, package structure, and local dev environment.

**Acceptance Criteria**:
- [ ] `uv` workspace with `packages/convene-core`, `packages/convene-providers`, `packages/convene-memory`
- [ ] `services/api-server`, `services/audio-service`, `services/task-engine`, `services/worker` as service packages
- [ ] `docker-compose.yml` with PostgreSQL 16 (+ pgvector extension), Redis 7
- [ ] `pyproject.toml` at root with shared dev dependencies (ruff, mypy, pytest)
- [ ] Basic CI config (GitHub Actions) running ruff, mypy, pytest
- [ ] `.env.example` with all required environment variables documented
- [ ] Health check endpoints on all services

**Technical Notes**:
- Use `uv workspace` with `members` in root `pyproject.toml`
- Each package has its own `pyproject.toml` with `[project.dependencies]`
- Use `ruff` for formatting + linting (replaces black, isort, flake8)
- PostgreSQL should have pgvector extension enabled in docker-compose

---

### F1.2 — Core Domain Models
**Context**: Define the data models that everything else builds on — meetings, tasks, participants, agents.

**Acceptance Criteria**:
- [ ] `Meeting` model: id, platform, dial_in_number, meeting_code, scheduled_at, started_at, ended_at, participants, status
- [ ] `Participant` model: id, name, email (optional), speaker_id (from diarization), role
- [ ] `Task` model: id, meeting_id (origin), description, assignee, due_date, priority, status (pending/in_progress/done/blocked), dependencies, created_at, updated_at, source_utterance
- [ ] `Decision` model: id, meeting_id, description, decided_by, participants_present, created_at
- [ ] `TranscriptSegment` model: id, meeting_id, speaker_id, text, start_time, end_time, confidence
- [ ] `AgentConfig` model: id, name, voice_id, system_prompt, capabilities, meeting_types
- [ ] All models as Pydantic v2 BaseModels with proper validators
- [ ] SQLAlchemy ORM models mirroring Pydantic models for database persistence
- [ ] Alembic migration for initial schema

**Technical Notes**:
- Keep Pydantic models (API/events) separate from SQLAlchemy models (persistence)
- Use UUIDs for all primary keys
- Tasks should support a DAG of dependencies via a `dependencies: list[UUID]` field
- Status transitions should be validated (e.g., can't go from "done" back to "pending" without explicit reopen)

---

### F1.3 — Provider Abstraction Layer
**Context**: Abstract STT, TTS, and LLM providers behind interfaces so we can swap providers without changing business logic.

**Acceptance Criteria**:
- [ ] `STTProvider` ABC with methods: `start_stream()`, `send_audio(chunk)`, `get_transcript()`, `close()`
- [ ] `TTSProvider` ABC with methods: `synthesize(text) -> AsyncIterator[bytes]`, `get_voices() -> list[Voice]`
- [ ] `LLMProvider` ABC with methods: `extract_tasks(transcript) -> list[Task]`, `summarize(transcript) -> str`, `generate_report(tasks) -> str`
- [ ] `AssemblyAISTT` implementation with WebSocket streaming and diarization
- [ ] `DeepgramSTT` implementation as fallback
- [ ] `AnthropicLLM` implementation using Claude for task extraction
- [ ] Provider registry pattern: `get_provider("stt", "assemblyai")` returns configured instance
- [ ] Automatic fallback: if primary STT fails, switch to fallback mid-stream

**Technical Notes**:
- Use Python ABCs (not complex DI frameworks)
- STT providers must handle 8kHz phone audio (mono, μ-law or PCM)
- LLM extraction should use structured output (Pydantic schemas as tool definitions)
- Provider config via environment variables with sensible defaults

---

### F1.4 — Twilio Phone Integration
**Context**: The core meeting access method. Convene dials into meetings via their phone number, joining as a phone participant.

**Acceptance Criteria**:
- [ ] Service that initiates outbound Twilio calls to meeting dial-in numbers
- [ ] DTMF tone generation to enter meeting IDs/PINs after connecting
- [ ] Bidirectional audio streaming via Twilio Media Streams (WebSocket)
- [ ] Audio format handling: receive μ-law 8kHz from Twilio, convert to format STT expects
- [ ] Call lifecycle management: initiate, monitor, detect meeting end, hang up
- [ ] Retry logic for failed dial-ins (busy, wrong PIN, etc.)
- [ ] Concurrent meeting support: handle multiple active calls
- [ ] Webhook endpoints for Twilio call status callbacks
- [ ] Meeting scheduling: accept a meeting URL or dial-in details, extract phone number + meeting ID, schedule the call

**Technical Notes**:
- Twilio Media Streams sends audio as base64-encoded μ-law at 8kHz
- Use `<Stream>` TwiML verb for bidirectional audio
- For Phase 1 (listen only), we only need the inbound audio stream
- Parse meeting invite URLs to extract dial-in info (regex patterns for Zoom, Meet, Teams)
- Zoom format: `+1XXXXXXXXXX,,MEETING_ID#`
- Meet format: varies by region, typically US/UK numbers
- Teams format: conference ID entered after connecting
- Cost: ~$0.018/min outbound + ~$0.0085/min for Media Streams

---

### F1.5 — Real-Time Transcription Pipeline
**Context**: Stream phone audio to STT provider, produce speaker-diarized transcript segments in real-time.

**Acceptance Criteria**:
- [ ] Audio pipeline: Twilio WebSocket → audio buffer → STT provider WebSocket
- [ ] Real-time transcript segments emitted as events (Redis Streams)
- [ ] Speaker diarization: identify different speakers in the mixed phone audio
- [ ] Transcript segments stored in PostgreSQL with meeting_id, speaker, timestamp
- [ ] Handle audio quality issues: silence detection, noise, cross-talk
- [ ] Emit `transcript.segment.final` events when STT confirms a segment
- [ ] Emit `meeting.started` and `meeting.ended` lifecycle events
- [ ] Configurable buffering: aggregate segments into ~30-second chunks for task extraction

**Technical Notes**:
- AssemblyAI streaming WebSocket expects PCM16 audio — need to transcode from Twilio's μ-law
- Use `audioop` or `pydub` for format conversion (μ-law 8kHz → PCM16 16kHz)
- Speaker diarization on phone audio is harder than per-participant streams — expect 70-85% accuracy
- Buffer management is critical: don't let audio queue grow unbounded if STT is slow
- Consider VAD (Voice Activity Detection) to skip silence and reduce STT costs

---

### F1.6 — Task Extraction Engine
**Context**: LLM-powered worker that processes transcript segments and extracts structured tasks, decisions, and commitments.

**Acceptance Criteria**:
- [ ] Worker subscribes to `transcript.segment.final` events from Redis Streams
- [ ] Batch processing: accumulate 3-5 minutes of transcript, then extract
- [ ] LLM prompt that identifies: action items, commitments, deadlines, owners, decisions
- [ ] Structured output as Pydantic `Task` and `Decision` models
- [ ] Deduplication: don't create duplicate tasks from overlapping transcript windows
- [ ] Confidence scoring: flag low-confidence extractions for human review
- [ ] Post-meeting summary extraction: when meeting ends, generate full summary
- [ ] Emit `task.created`, `task.updated`, `decision.recorded` events

**Technical Notes**:
- Use sliding window with overlap: process minutes 0-5, then 3-8, then 6-11, etc.
- Two-stage extraction works best:
  1. Identify utterances that contain commitments (classifier)
  2. Extract structured task data from identified utterances (extractor)
- Prompt should include previous tasks from this team for context (enables "still working on X" detection)
- Use Claude with tool_use for structured extraction — define Task schema as a tool
- Cost optimization: use Haiku for classification, Sonnet for extraction

---

### F1.7 — Memory System
**Context**: Four-layer memory that gives the agent context across meetings.

**Acceptance Criteria**:
- [ ] **Working memory** (Redis): current meeting transcript, active participants, real-time task candidates
- [ ] **Short-term memory** (PostgreSQL): last 10 meetings with each team/recurring meeting, recent task statuses
- [ ] **Long-term memory** (pgvector): vectorized meeting summaries, searchable by semantic query
- [ ] **Structured state** (PostgreSQL relational): tasks table with full lifecycle, decisions table, participant history
- [ ] Memory context builder: given a meeting about to start, assemble relevant context (previous tasks, open items, team patterns)
- [ ] Automatic memory consolidation: after meeting ends, compress working memory → short/long term
- [ ] Team detection: group meetings by recurring calendar events or participant overlap

**Technical Notes**:
- pgvector with HNSW index for vector search (better recall than IVFFlat at moderate scale)
- Embedding model: `text-embedding-3-small` (OpenAI) or `voyage-3-lite` (Anthropic ecosystem)
- Meeting context window for task extraction should include: open tasks for this team, last meeting summary, participant names
- Keep working memory TTL at 24 hours — no stale state
- Short-term memory window: 30 days or last 10 meetings, whichever is more

---

### F1.8 — API Server & Dashboard
**Context**: REST API for managing meetings and viewing extracted data. Simple React dashboard.

**Acceptance Criteria**:
- [ ] `POST /meetings` — schedule a meeting (accepts dial-in details or meeting URL)
- [ ] `GET /meetings` — list meetings with pagination and filters
- [ ] `GET /meetings/{id}` — meeting detail with transcript, tasks, decisions
- [ ] `GET /meetings/{id}/transcript` — full transcript with speaker labels and timestamps
- [ ] `GET /tasks` — list all tasks with filters (status, assignee, meeting, date range)
- [ ] `PATCH /tasks/{id}` — update task status, assignee, due date
- [ ] `GET /tasks/overdue` — tasks past due date
- [ ] `GET /agents` — list configured agents
- [ ] `POST /agents` — create/configure an agent
- [ ] WebSocket endpoint for real-time transcript streaming during active meetings
- [ ] Simple React dashboard showing: upcoming meetings, active meetings with live transcript, task board, meeting history
- [ ] Authentication: API key for MVP, OAuth later

**Technical Notes**:
- FastAPI with async SQLAlchemy sessions
- Use FastAPI's dependency injection for database sessions and auth
- WebSocket for live transcript uses Redis pub/sub to bridge from audio-service
- Dashboard can be a simple Next.js app or even a Vite + React SPA
- For MVP, the dashboard is secondary to the API — integrations (Slack, etc.) matter more

---

### F1.9 — Calendar Integration
**Context**: Automatically detect meetings from calendar and schedule agent dial-ins.

**Acceptance Criteria**:
- [ ] Google Calendar OAuth integration: read upcoming meetings
- [ ] Extract dial-in info from calendar event body/description (parse Zoom, Meet, Teams links)
- [ ] Auto-schedule agent to dial in N minutes before meeting starts
- [ ] Support recurring meetings: detect series and maintain continuity
- [ ] Manual override: user can enable/disable agent for specific meetings
- [ ] `GET /calendar/upcoming` — show detected meetings with dial-in status
- [ ] Sync frequency: poll every 5 minutes or use webhook push

**Technical Notes**:
- Google Calendar API v3 with service account or OAuth2
- Meeting URL parsing: regex patterns for zoom.us, meet.google.com, teams.microsoft.com
- Zoom URLs contain meeting ID in path; dial-in numbers are in the invite body
- Teams URLs require parsing the conference ID from the meeting body
- Store calendar events in PostgreSQL with a `dial_in_extracted` status

---

### F1.10 — Slack Integration
**Context**: Push task updates and meeting summaries to Slack. This is where most teams will interact with Convene outside of meetings.

**Acceptance Criteria**:
- [ ] Slack bot that posts meeting summaries to a configured channel after each meeting
- [ ] Task notifications: new tasks assigned, overdue reminders, status changes
- [ ] Slash command `/convene tasks` — show open tasks for the current user
- [ ] Slash command `/convene meetings` — show upcoming scheduled meetings
- [ ] Thread-based task updates: each meeting gets a Slack thread, task updates post as replies
- [ ] Interactive buttons: mark task as done, snooze, reassign — directly from Slack
- [ ] DM notifications for individually assigned tasks

**Technical Notes**:
- Use Slack Bolt (Python SDK) for event handling and interactivity
- Slack app manifest for easy installation
- Store Slack team_id and channel mappings in PostgreSQL
- Rate limit awareness: Slack's API limits are generous but batch messages when possible

---

## Phase 2 — Speak & Report

> Goal: Agent can speak during meetings to deliver status updates and confirm tasks. Requires TTS integration and careful interaction design.

### F2.1 — TTS Integration
**Context**: Add text-to-speech so the agent can generate spoken audio and send it back through the Twilio call.

**Acceptance Criteria**:
- [ ] `CartesiaTTS` provider implementation (primary — fastest TTFA)
- [ ] `ElevenLabsTTS` provider implementation (fallback — most natural)
- [ ] Audio format conversion: TTS output → μ-law 8kHz for Twilio Media Streams
- [ ] Streaming TTS: begin playback before full response is generated
- [ ] Configurable voice selection per agent
- [ ] Volume normalization to match other meeting participants

**Technical Notes**:
- Twilio Media Streams accepts base64-encoded μ-law audio for output
- Cartesia outputs PCM — need to downsample and encode to μ-law
- Implement audio chunking: send TTS audio in 20ms frames to match Twilio's expectations
- Pre-generate common phrases ("Here's an update on last meeting's action items") for instant playback

---

### F2.2 — Standup Report Generation
**Context**: Before a standup or recurring meeting, the agent prepares a spoken progress report based on its task memory.

**Acceptance Criteria**:
- [ ] Detect standup/recurring meetings from calendar metadata
- [ ] Pre-meeting context assembly: gather all open tasks, completed since last meeting, blocked items
- [ ] LLM-generated natural-language report: conversational tone, not robotic lists
- [ ] Report structure: completed items → in-progress → blocked → new items from last meeting
- [ ] Configurable verbosity: brief (30 seconds), standard (1-2 minutes), detailed (3+ minutes)
- [ ] Report preview: show the report text in dashboard before the meeting so user can edit
- [ ] Timing: agent waits for a natural pause or explicit cue before speaking

**Technical Notes**:
- LLM prompt should produce conversational speech, not bullet points
- Example output: "Since our last sync on Tuesday, three of the five items have been wrapped up. The API migration is done, the docs are updated, and the staging deploy went through. Two items are still open — the proposal draft hasn't started, and the credentials issue is blocking the data pipeline work."
- Include a "confidence" indicator — don't report on tasks the agent isn't sure about

---

### F2.3 — Speaking Interaction Protocol
**Context**: Define when and how the agent speaks in meetings. This is critical UX — a poorly designed interaction will make people hate the agent.

**Acceptance Criteria**:
- [ ] **Scheduled speaking**: agent speaks at designated times (start of standup, end of meeting)
- [ ] **Cued speaking**: agent speaks when directly addressed ("Convene, what's the status?")
- [ ] **Wake word detection**: detect "Convene" or "Hey Convene" in transcript stream
- [ ] **Silence detection**: only speak during natural pauses (>2 seconds of silence)
- [ ] **Interruption handling**: if someone starts talking while agent is speaking, stop immediately
- [ ] **Speaking indicator**: say "This is Convene" before first utterance in a meeting
- [ ] **Brevity mode**: keep all unprompted speech under 30 seconds
- [ ] **Mute option**: respond to "Convene, mute" or "Convene, be quiet" to stop all speech

**Technical Notes**:
- VAD (Voice Activity Detection) on the inbound audio stream to detect when others are speaking
- Use Silero VAD — runs locally, ~10ms latency
- The speaking protocol should be configurable per team — some teams want active participation, others want minimal interruption
- Log all speaking decisions (spoke/chose-not-to-speak) for analytics and tuning

---

### F2.4 — Real-Time Task Confirmation
**Context**: When the agent detects a new commitment during a meeting, it can speak to confirm and capture it accurately.

**Acceptance Criteria**:
- [ ] Detect high-confidence commitments in real-time (not just batch extraction)
- [ ] Optionally speak to confirm: "Just to confirm — Sarah, you're taking the API docs update by Friday?"
- [ ] Handle corrections: if someone says "No, that's John's item," update accordingly
- [ ] Confirmation mode: configurable (always confirm, only confirm ambiguous, never confirm)
- [ ] Visual confirmation: also post to Slack thread in real-time

**Technical Notes**:
- Real-time extraction requires faster processing — use Haiku for speed
- Confirmation utterances should be <10 seconds
- Queue confirmations — don't interrupt a speaker to confirm something they said 30 seconds ago
- Batching: if 3 tasks are identified in quick succession, confirm as a group

---

## Phase 3 — Converse & Clarify

> Goal: Full multi-turn dialogue capability. Agent can answer questions, discuss priorities, and flag issues.

### F3.1 — Multi-Turn Dialogue Engine
**Context**: Move from single-utterance responses to sustained conversation with context.

**Acceptance Criteria**:
- [ ] Conversation state machine: idle → listening → thinking → speaking → listening
- [ ] Context window: maintain last 5 minutes of transcript + full task state as LLM context
- [ ] Multi-turn: handle follow-up questions ("What about the other items?" after a status report)
- [ ] Graceful exit: detect when the conversation has moved on and return to listening
- [ ] Parallel processing: continue transcribing other speakers while formulating response

**Technical Notes**:
- Consider Pipecat pipeline for managing the full voice interaction loop
- Turn detection is the hardest problem — use both VAD and semantic end-of-turn detection
- LLM should have a system prompt defining agent personality and meeting role
- Latency budget: <1.5 seconds from end of user speech to start of agent speech

---

### F3.2 — Conflict & Dependency Detection
**Context**: Agent proactively identifies conflicts between commitments across team members and meetings.

**Acceptance Criteria**:
- [ ] Detect scheduling conflicts: "Sarah committed to both the API review and the client demo on Thursday"
- [ ] Detect dependency chains: "The deploy is blocked until the migration is done, which John owns"
- [ ] Detect overcommitment: "Marcus has 7 open tasks across 3 projects due this week"
- [ ] Optional proactive alerting: speak up during planning meetings to flag conflicts
- [ ] Dependency graph visualization in dashboard

---

### F3.3 — Meeting Facilitation
**Context**: Agent can actively facilitate structured meetings (standups, retros, planning).

**Acceptance Criteria**:
- [ ] Standup facilitation: prompt each participant for their update
- [ ] Time boxing: "We're at 12 minutes — should we wrap up?"
- [ ] Agenda tracking: "We've covered items 1 and 2, moving to item 3"
- [ ] Parking lot: "That's a great point but might be off-topic — should I add it to the parking lot?"
- [ ] Retro facilitation: collect went-well, didn't-go-well, action items

---

## Phase 4 — Specialize & Orchestrate

> Goal: Multiple agent voices with specialized roles. Agent marketplace potential.

### F4.1 — Multi-Agent Architecture
**Context**: Support multiple agent personas that can join different meeting types.

**Acceptance Criteria**:
- [ ] Agent registry: define agents with distinct names, voices, system prompts, capabilities
- [ ] Meeting-agent assignment: map meeting types to appropriate agents
- [ ] Shared memory: all agents read/write to the same task and decision store
- [ ] Agent handoff: one agent can invoke another's expertise mid-meeting
- [ ] Pre-built personas: Standup Agent, Decision Tracker, Client Meeting Agent

---

### F4.2 — Integration Marketplace
**Context**: Deep integrations with project management and developer tools.

**Acceptance Criteria**:
- [ ] Linear: create/update issues from extracted tasks, sync status bidirectionally
- [ ] Jira: same as Linear
- [ ] GitHub: link tasks to PRs, detect "closes #123" in meeting discussion
- [ ] Notion: push meeting summaries and task tables
- [ ] Asana: task sync
- [ ] Webhook API: generic event push for custom integrations

---

### F4.3 — Analytics & Insights
**Context**: Meta-analysis across meetings to surface team patterns.

**Acceptance Criteria**:
- [ ] Meeting effectiveness score: ratio of tasks completed vs. created
- [ ] Commitment reliability: per-person completion rate
- [ ] Meeting frequency optimization: "This meeting could be async based on patterns"
- [ ] Time analysis: how much meeting time is status updates vs. decisions vs. discussion
- [ ] Team dashboard with trends over time

---

## Implementation Priority

For a solo founder building with Claude Code, the recommended implementation order is:

1. **F1.1** — Project scaffolding (Day 1)
2. **F1.2** — Core domain models (Day 1-2)
3. **F1.3** — Provider abstraction (Day 2-3)
4. **F1.4** — Twilio phone integration (Day 3-5)
5. **F1.5** — Real-time transcription (Day 5-7)
6. **F1.6** — Task extraction engine (Day 7-9)
7. **F1.7** — Memory system (Day 9-11)
8. **F1.8** — API server & dashboard (Day 11-14)
9. **F1.10** — Slack integration (Day 14-16)
10. **F1.9** — Calendar integration (Day 16-18)

Phase 1 MVP target: **3 weeks** of focused Claude Code development.
