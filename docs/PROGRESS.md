# Convene AI — Development Progress Log

> Append-only log of completed work. Each entry is written by whoever completed
> the work — either CoWork (scheduled) or Jonathan (manual session).
> Never delete or overwrite previous entries.

---

<!-- New entries go at the top -->

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
