# Convene AI — Go-to-Market Strategy

---

## Core GTM Thesis

Every AI meeting tool that reached scale did so through the same mechanism: **the product markets itself inside every meeting it joins.** One person uses it, the bot appears, everyone else in the meeting sees it, and a percentage sign up. Fireflies reached 20M users and a $1B valuation without spending a dollar on marketing. Otter reached $100M ARR the same way.

Convene inherits this viral loop — but with a twist. When Convene's agent *speaks* in a meeting, it creates a fundamentally more memorable impression than a silent bot. A participant who hears an AI deliver a progress report and confirm action items will talk about it after the meeting. That word-of-mouth effect compounds.

The flip side is that the meeting AI category has a serious trust problem. Otter is facing a federal class-action lawsuit for recording without adequate consent. Reddit is full of people describing meeting bots as "malware." IT teams are actively blocking these tools. Convene must grow through the same viral mechanism while deliberately positioning as the ethical, consent-first alternative.

---

## Phase 0: Validate Before Building (Weeks 1–4)

### Sell the Service, Build the Product

Before writing any code beyond the MVP, validate demand by offering the core Convene workflow as a manual consulting service:

1. **Attend client meetings** (or review their recordings/transcripts)
2. **Extract tasks and commitments** using Claude/GPT
3. **Deliver a structured brief** before their next meeting: completed items, open items, blocked items, conflicts
4. **Iterate on the format** based on what teams actually find useful

**Pricing**: $500–1,500/month per team for weekly meeting analysis. This is cheap enough for startups and small enough to be expensed without procurement.

**Goal**: 3–5 paying consulting clients. This validates:
- Do teams actually want cross-meeting task tracking?
- Will they let an AI (even a human-assisted one) into their meeting workflow?
- What meeting types benefit most? (Standups? Sprint planning? All-hands?)
- What output format do they actually use? (Slack? Dashboard? Email?)

Revenue from this phase ($1,500–7,500/month) offsets development costs and provides real usage data to inform product decisions.

---

## Phase 1: Developer-First Launch (Months 1–3)

### Target Persona: Technical Founder / Engineering Lead at a 10–50 person startup

This persona:
- Runs daily standups and weekly sprint planning
- Already uses AI tools (Cursor, Claude Code, Copilot)
- Has purchasing authority (no procurement hoops)
- Cares about accountability and shipping velocity
- Is on Hacker News, Reddit, Product Hunt, Twitter/X

### Launch Sequence

**Week 1–2: Soft launch with inner circle**
- Deploy Phase 1 MVP (listen + extract)
- Invite consulting clients to use the product version
- Invite 10–20 founders from personal network for beta
- Collect feedback aggressively — what's useful, what's missing, what's wrong

**Week 3: Hacker News / Twitter launch**
- "Show HN: I built an AI agent that dials into your standups and tracks what everyone committed to"
- Focus the narrative on the architectural choice (phone dial-in = works everywhere, no SDK hacks) and the vision (agent that never forgets a promise)
- Open source a component if possible — the meeting URL parser, the task extraction prompts, the Twilio dial-in utility

**Week 4: Product Hunt launch**
- Coordinate for a Tuesday launch (highest traffic)
- Leverage early users for launch-day comments and upvotes
- Fathom's Product Hunt launch was a significant growth accelerator — the meeting AI category performs well on PH

**Week 5–6: Content flywheel begins**
- Founder blog posts: "What I learned building an AI that joins meetings," "Why phone dial-in is the future of meeting AI"
- Technical blog posts: "How to build a Twilio meeting bot in Python," "Structured task extraction with Claude tool_use"
- These serve dual purpose: SEO and developer credibility

### Channels (Ranked by Expected ROI)

1. **In-meeting virality** — every meeting the agent joins, 3-10 people see it. Conversion rate TBD but this is the primary engine. The free tier (listen + extract) must be generous enough that people actually use it in every meeting.

2. **Hacker News / Reddit** — Technical founders live here. One successful HN post generates 10K+ site visits. Ongoing engagement in r/startups, r/SaaS, r/productivity, r/ChatGPT. Authentic, not promotional.

3. **Twitter/X founder community** — Build in public. Share metrics, architecture decisions, interesting findings from meeting data. Tag relevant voices in AI/productivity space.

4. **Product Hunt** — One-time launch event with sustained tail. Meeting AI tools consistently rank well.

5. **LinkedIn** — B2B-oriented content for reaching engineering managers and heads of product at mid-market companies. The secondary persona.

6. **Zoom App Marketplace** — Essential for distribution to mid-market. Multi-week review process — submit early. Even though Convene uses phone dial-in, a Zoom marketplace listing provides discovery and legitimacy.

7. **SEO / Content Marketing** — Longer-term play. Target keywords: "AI meeting assistant," "automated standup," "meeting action item tracker," "AI for standups." Blog + docs site.

### What NOT to Spend Money On (Yet)
- Paid advertising (Google Ads, LinkedIn Ads) — CAC is too high for early stage
- Sales team — sell founder-to-founder for the first 100 customers
- PR agencies — organic HN/PH/Twitter outperforms paid PR at this stage
- Conference sponsorships — too expensive per lead for a solo founder

---

## Phase 2: Mid-Market Expansion (Months 4–8)

### Target Persona Expands: Engineering Manager / VP of Product at $10M–$500M company

This persona:
- Manages 3–5 teams running standups and planning meetings
- Frustrated that action items from meetings never get tracked
- Has budget ($1K–5K/month range is easy to approve)
- Evaluates tools based on integration quality and team-wide adoption
- Found Convene because a direct report started using it

### Key Activities

**Integrations as growth levers**: Slack and Linear/Jira integrations are table stakes. Every Slack notification from Convene is a mini-advertisement. Every Linear ticket auto-created from a meeting commitment demonstrates value.

**Team-level onboarding**: Shift from individual signup to team onboarding. "Add Convene to your team's recurring meetings" — one-click setup for all standup/planning meetings.

**Case studies from Phase 1 users**: Quantified results — "Team X reduced meeting time by 20% and increased task completion rate by 35% after 8 weeks with Convene." These power the sales motion for larger teams.

**Self-serve annual plans**: Offer 20% discount for annual billing. Reduces churn, improves cash flow, signals customer commitment.

### Pricing Adjustment for Mid-Market

| Tier | Price | Target |
|---|---|---|
| Free | $0 | Individual — listen + extract for up to 5 meetings/week |
| Pro | $19/seat/month | Small team — persistent memory, integrations, Slack bot |
| Team | $39/seat/month | Multi-team — speaking agent, cross-team tracking, analytics |
| Enterprise | Custom ($79+/seat) | 100+ seats — SSO, audit logs, dedicated support, custom agents |

**Important**: Do NOT cap by minutes. Users hate minute caps — it's the #1 complaint about Otter and Fireflies. Convene should be unlimited meetings at every tier, with differentiation on features and team size.

---

## Phase 3: Voice Agent Launch (Months 6–10)

### The "Agent Speaks" Moment

When Phase 2 of the product ships (agent can speak in meetings), the GTM motion shifts dramatically. This is a "show, don't tell" product — a demo of an AI delivering a standup progress report is more compelling than any landing page.

**Demo video as primary marketing asset**: Record a real standup where Convene's agent reports on last meeting's tasks. This video goes on the landing page, Twitter, LinkedIn, Product Hunt (as an update), and HN.

**"Convene just spoke in my meeting" viral moment**: When the agent speaks for the first time in a meeting, attendees who don't have Convene will be genuinely surprised. This creates organic social media posts, Slack messages to colleagues, and word-of-mouth that no amount of advertising can replicate.

**Gated access to speaking features**: Consider launching voice features as a waitlist or invite-only tier. This creates urgency, controls rollout quality, and generates "I just got access" social proof.

---

## Revenue Projections (Conservative)

| Month | MRR | Customers (teams) | Assumptions |
|---|---|---|---|
| 3 | $2,000 | 5 | Consulting + early beta converts |
| 6 | $8,000 | 25 | Post-launch growth, free → pro conversion |
| 9 | $25,000 | 70 | Voice agent launch, mid-market teams |
| 12 | $60,000 | 150 | Team tier adoption, word of mouth |
| 18 | $150,000 | 350 | Self-serve flywheel, integrations mature |
| 24 | $350,000 | 700 | Enterprise pilots, multi-team deployments |

These are deliberately conservative. Fireflies went from $0 to profitability and eventually $1B on organic growth alone. The meeting AI viral loop, once established, compounds faster than most B2B SaaS.

---

## Key Metrics to Track

**Leading indicators** (early signal of product-market fit):
- Meeting join success rate (can the agent reliably dial in?)
- Task extraction accuracy (are the extracted tasks actually useful?)
- Free → paid conversion rate (target: 5–8%)
- Meetings per team per week (engagement depth)
- "Aha moment": number of meetings before a user converts (optimize time-to-value)

**Lagging indicators** (business health):
- MRR and growth rate
- Net revenue retention (target: >110% — teams expand usage over time)
- CAC payback period (target: <3 months given organic growth)
- Churn rate (target: <5% monthly for pro, <3% for team/enterprise)

**Virality metrics**:
- Meetings with non-users present (exposure events)
- Signup rate from meeting exposure (viral coefficient)
- Time from first exposure to signup (viral cycle time)

---

## Competitive Positioning Statement

**For engineering teams and startup founders** who are frustrated that meeting commitments evaporate the moment the call ends, **Convene AI** is a voice-first meeting agent that dials into your calls, tracks every commitment, and speaks up to report progress. **Unlike Otter, Fireflies, and other transcription tools** that produce summaries nobody reads, Convene maintains persistent memory across meetings and holds your team accountable by being present in the room where promises are made and persistent in the system where they're tracked.
