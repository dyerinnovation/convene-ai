# Convene AI — Documentation

## What is Convene AI?

Convene AI is a voice-first AI agent that dials into your meetings via phone, listens for commitments, extracts and tracks tasks across meetings, and eventually speaks to report progress. It's the accountability partner your team never had.

## Repository Structure

This is a Python monorepo managed with `uv` workspaces.

```
convene-ai/
├── CLAUDE.md                      # Bootstrap prompt for Claude Code development
├── docs/                          # Product & strategy documentation
│   ├── README.md                  # This file
│   ├── VISION.md                  # Product vision & business case
│   ├── ROADMAP.md                 # Feature roadmap (Claude Code-ready)
│   ├── COMPETITIVE_ANALYSIS.md    # Market sizing & competitive landscape
│   └── GO_TO_MARKET.md            # Go-to-market strategy
├── packages/                      # Shared libraries
│   ├── convene-core/              # Domain models, events, interfaces (ABCs)
│   ├── convene-providers/         # STT, TTS, LLM provider implementations
│   └── convene-memory/            # Four-layer persistent memory system
├── services/                      # Independently runnable services
│   ├── api-server/                # FastAPI REST + WebSocket API
│   ├── audio-service/             # Twilio phone integration + STT pipeline
│   ├── task-engine/               # LLM-powered task extraction workers
│   └── worker/                    # Background jobs (Slack, calendar, notifications)
└── web/                           # Dashboard frontend
```

## Documents

### [VISION.md](./VISION.md)
The product vision and business case. Covers the problem, insight, phased progression (listen → speak → converse → orchestrate), market opportunity, revenue model, unit economics, and competitive moat. Start here to understand what Convene is and why it matters.

### [ROADMAP.md](./ROADMAP.md)
Feature-by-feature development roadmap structured for Claude Code. Each feature includes context, acceptance criteria with checkboxes, and technical implementation notes. Organized into four phases with an implementation priority order and estimated timelines. This is the document you hand to Claude Code to start building.

### [COMPETITIVE_ANALYSIS.md](./COMPETITIVE_ANALYSIS.md)
Deep competitive analysis of the AI meeting assistant landscape. Covers market sizing (TAM/SAM/SOM), detailed profiles of Otter.ai, Fireflies.ai, MeetGeek, tl;dv, Sembly, Zoom AI Companion, Microsoft Copilot, and infrastructure players (Recall.ai, Pipecat). Includes a differentiation matrix and risk analysis.

### [GO_TO_MARKET.md](./GO_TO_MARKET.md)
Go-to-market strategy across four phases: consulting validation (Phase 0), developer-first launch (Phase 1), mid-market expansion (Phase 2), and voice agent launch (Phase 3). Covers channel strategy, pricing, revenue projections, key metrics, and competitive positioning.

## Getting Started with Development

1. Read `CLAUDE.md` at the repository root — this is the bootstrap prompt for Claude Code
2. Read `docs/ROADMAP.md` — start with Feature F1.1 (Project Scaffolding)
3. Follow the implementation priority order in the roadmap

## Architecture Decision: Phone Dial-In

Convene's core architectural bet is using **Twilio phone dial-in** to join meetings instead of platform-specific bot SDKs (Zoom SDK, Teams Bot Framework, etc.). Every major meeting platform supports phone participants. A Twilio agent calls the meeting's dial-in number, enters the meeting code via DTMF tones, and has bidirectional audio access.

This decision means:
- **Platform-agnostic from day one** — works on Zoom, Meet, Teams, Webex, and anything with a phone bridge
- **No marketplace approval process** — ship immediately without waiting for Zoom/Microsoft review
- **No platform SDK dependencies** — no risk of breaking changes in meeting platform APIs
- **Dramatically simpler engineering** — one Twilio integration vs. three platform-specific bot frameworks
- **Tradeoff**: phone-quality audio (8kHz) instead of 48kHz, no video/screen access, mixed audio stream instead of per-participant tracks

Modern STT models handle phone audio well, and for Convene's use case (task extraction and voice participation), the tradeoffs are acceptable. Platform-native bot integration is a future optimization, not a requirement.
