# Scheduled Tasks — Overview

This directory contains version-controlled instructions for CoWork scheduled tasks. Each file is read by a CoWork scheduled task at runtime, meaning you can change the build process by editing these files and pushing to `main`.

## How it works

CoWork scheduled tasks are configured in the Claude Desktop app with minimal prompt instructions that simply point to these files:

```
Follow the instructions in docs/cowork-tasks/daily-build.md exactly.
```

The detailed logic lives here in the repo, not in the CoWork UI. This gives you:

- **Version control** — Full git history of every change to the build process
- **Branching** — Experiment with different approaches on feature branches
- **Code review** — PR changes to task behavior just like code changes
- **Reproducibility** — Anyone on the team can see exactly what the automated tasks do

## Active tasks

| Task | File | Schedule | Model | Purpose |
|---|---|---|---|---|
| Daily Build Sprint | `daily-build.md` | Weekdays 7:00 AM | Sonnet | Implements one roadmap item |
| Daily Review Brief | `daily-review.md` | Weekdays 8:30 AM | Haiku | Summarizes build results |
| Weekly Architecture Review | `weekly-architecture-review.md` | Fridays 4:00 PM | Opus | Deep codebase analysis |

## Coordination files

These files (in `docs/`) enable sync between you and the scheduled tasks:

| File | Purpose | Who writes |
|---|---|---|
| `TASKLIST.md` | Ordered task queue | You (CoWork checks items off) |
| `PROGRESS.md` | Append-only development log | CoWork daily build |
| `HANDOFF.md` | Shift change notes | Both you and CoWork |
| `DAILY_BRIEF.md` | Morning summary for review | CoWork daily review |
| `WEEKLY_REVIEW.md` | Architecture assessment | CoWork weekly review |

## Modifying task behavior

1. Edit the relevant `.md` file in this directory
2. Commit and push to `main`
3. The next scheduled run will use the updated instructions

## Adding new scheduled tasks

1. Create a new `.md` file in this directory with the task instructions
2. In CoWork Scheduled sidebar, create a new task pointing to your file
3. Update the table above in this README
