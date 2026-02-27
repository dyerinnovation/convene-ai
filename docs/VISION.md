# Convene AI — Product Vision & Business Case

## The One-Liner

Convene AI is an autonomous voice agent that dials into your meetings, listens for commitments, builds its own task list, and speaks up to report progress — turning conversations into accountability.

---

## The Problem

Every team has the same broken loop:

1. People have a meeting and make commitments
2. Someone (maybe) writes down action items
3. Those notes sit in a doc or Slack thread
4. At the next meeting, nobody remembers what was agreed
5. Repeat

The tools that exist today — Otter, Fireflies, tl;dv — solve step 2. They transcribe, summarize, and extract action items. But the output is a *document*. It sits in a dashboard nobody checks. The accountability loop never closes.

The manual workaround many teams use (and the workflow that inspired Convene) is feeding meeting transcripts into LLMs to extract action items and build plans. This works, but it's labor-intensive, breaks continuity between meetings, and requires a human to be the bridge between conversation and execution.

## The Insight

**The AI shouldn't just listen to the meeting — it should be a participant in it.**

An agent that dials into your standup, knows what was committed last Tuesday, and says "Three of five items from last week are complete — the API migration is blocked on credentials, and the proposal draft hasn't started" fundamentally changes meeting dynamics. It's not a note-taker. It's an accountability partner with a voice.

## The Vision

Convene AI is a voice-first AI agent that:

- **Dials into scheduled meetings** via phone (Twilio), joining as a participant on any platform — Zoom, Meet, Teams, or any service with dial-in
- **Listens and extracts commitments** in real-time, identifying who promised what and by when
- **Maintains persistent task state** across meetings — it never forgets a commitment
- **Speaks to report progress** at standups, retros, and check-ins
- **Engages in multi-turn dialogue** to clarify tasks, flag conflicts, and answer questions about team commitments
- **Orchestrates multiple specialized agents** — a Task Tracker, Decision Logger, Standup Facilitator — each with a distinct voice and role

### The Phased Progression

**Phase 1 — Listen & Learn**: The agent dials in, listens silently, extracts tasks and commitments, and presents them in a dashboard. It builds memory across meetings.

**Phase 2 — Speak & Report**: The agent can speak during meetings to deliver progress updates, flag overdue items, and confirm new commitments.

**Phase 3 — Converse & Clarify**: The agent participates in multi-turn dialogue — answering questions, flagging conflicts ("That deadline overlaps with what Sarah committed to on Thursday"), and suggesting priorities.

**Phase 4 — Specialize & Orchestrate**: Multiple agent voices with specialized roles join different meeting types. The Scrum agent facilitates standups. The Decision agent tracks and reminds. The Ops agent coordinates cross-team dependencies.

---

## Why Now

Three converging forces make this possible today:

### 1. Voice AI latency has crossed the "natural conversation" threshold
Sub-300ms STT (Deepgram, AssemblyAI), sub-100ms TTS (Cartesia), and ~320ms LLM time-to-first-token combine for <800ms total round-trip — below the threshold where conversation feels natural.

### 2. Phone dial-in eliminates the platform access problem
Every major meeting platform supports phone dial-in. A Twilio agent that calls a meeting's dial-in number works on Zoom, Meet, Teams, Webex, and anything else with a phone bridge. No SDK integration, no marketplace approval, no headless browser hacks. This is the architectural insight that makes a solo founder viable — you skip 6-12 months of platform-specific bot engineering.

### 3. The market is stuck in "transcription mode"
A dozen well-funded competitors (Otter at $100M ARR, Fireflies at $1B valuation) are competing on who can transcribe and summarize meetings better. This is a commodity race. The leap from passive transcription to active participation is the next inflection point, and only MeetGeek has taken early steps (limited beta, 30-minute speaking cap, no persistent memory).

---

## Business Case

### Target Market

**Primary**: Mid-market companies ($10M–$500M revenue) with 20–200 employees where meeting accountability is a real workflow gap, not just a productivity nice-to-have.

**Secondary**: 10–50 person startups, particularly engineering teams using standups and sprint ceremonies where structured accountability maps directly to shipping velocity.

**Tertiary**: AI-native agencies and consultancies that manage multiple client engagements and need automated status tracking across dozens of concurrent projects.

### Market Size

| Market | 2025 Size | Growth (CAGR) | 2030 Projection |
|---|---|---|---|
| AI Meeting Assistants | $2.5–3.7B | 25–35% | $7–20B |
| AI Agents (broad) | $5–8B | 38–46% | $43–53B |
| Voice AI Agents | $2–3B | ~35% | $8–12B |

Convene sits at the intersection of all three. Conservative SAM (mid-market teams willing to pay for active meeting participation) is estimated at $500M–$1B by 2027.

### Revenue Model

**Free tier**: Unlimited meeting attendance + task extraction. The agent listens and shows you what it found. This drives viral adoption — every meeting it joins is marketing.

**Pro ($19/seat/month)**: Speaking agent, persistent task tracking, integrations (Slack, Linear, Jira), meeting memory.

**Team ($39/seat/month)**: Multiple agent roles, cross-team dependency tracking, custom agent personas, analytics dashboard.

**Enterprise (custom)**: SSO, audit logs, data residency, dedicated agent training, API access.

### Unit Economics

| Cost Component | Per Meeting Hour |
|---|---|
| Twilio dial-in | ~$1.08 (inbound + outbound) |
| STT (AssemblyAI) | ~$0.15 |
| LLM (task extraction) | ~$0.05–0.10 |
| TTS (Phase 2+) | ~$0.05 |
| Infrastructure | ~$0.10 |
| **Total COGS** | **~$1.43–1.48** |

At $19/seat/month with an average of 20 meeting-hours/seat/month, COGS is ~$29/seat — requiring approximately 2 seats per paying user or margin optimization via batched extraction and cheaper STT. At $39/seat, margins improve to ~25%. Enterprise pricing at $79+ achieves healthy 50%+ margins.

**Key insight**: AI tool margins (50–60%) are lower than traditional SaaS (80–90%). Pricing must account for per-minute infrastructure costs. The path to better margins is reducing unnecessary real-time processing (batch extraction where possible) and negotiating volume pricing with STT/TTS providers.

### Competitive Moat

1. **Persistent memory creates switching costs**: Once the agent knows your team's commitment history, project dependencies, and communication patterns, switching to a competitor means losing institutional memory.

2. **Network effects within teams**: One person's agent improves as it hears from everyone on the team. The more meetings it attends, the more context it has. This is defensible against point solutions.

3. **Voice participation is a UX moat**: Building a reliable, natural-sounding meeting participant requires solving turn-detection, interruption handling, and social dynamics — hard engineering that compounds over time.

---

## The Founding Thesis

Enterprise AI should create compound improvement over time rather than repeatedly solving the same problems. Every meeting Convene attends makes it smarter about your team, your commitments, and your patterns. The agent that never forgets a promise — and has the voice to remind you — is the missing piece between conversation and execution.

Convene doesn't replace your meeting tool. It doesn't replace your project management tool. It closes the gap between them by being present in the room where commitments are made and persistent in the system where they're tracked.
