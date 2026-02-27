# Daily Review Brief — Task Instructions

> These instructions are read and executed by the CoWork scheduled task.
> This task runs 90 minutes after the daily build sprint.

---

## Process

1. Pull latest changes:
   ```bash
   git pull origin main
   git fetch --all
   ```

2. Find today's scheduled branch:
   ```bash
   git branch -r | grep scheduled/$(date +%Y-%m-%d)
   ```

3. If a scheduled branch exists, get the diff:
   ```bash
   git diff main...origin/scheduled/$(date +%Y-%m-%d)-*
   ```

4. Read `docs/PROGRESS.md` — find today's entry.

5. Read `docs/HANDOFF.md` — check for blockers or warnings.

6. Run quality checks against the branch (if it exists):
   ```bash
   git checkout origin/scheduled/$(date +%Y-%m-%d)-* 2>/dev/null
   uv run pytest --tb=short -q 2>&1 | tail -20
   git checkout main
   ```

---

## Write the briefing

Overwrite `docs/DAILY_BRIEF.md` with the following format:

```markdown
# Daily Brief — {YYYY-MM-DD}

## Summary
{2-3 sentences: what was built, which roadmap item, what files were touched}

## Code Quality
- **Tests:** {X passed, Y failed — or "no scheduled branch found today"}
- **Type checking:** {clean / N errors}
- **Linting:** {clean / N issues}

## Blockers
{List any blockers from PROGRESS.md or HANDOFF.md, or "None — clear to proceed"}

## Decisions Needed
{List any architectural decisions or trade-offs flagged by the build task, or "None"}

## Risk Assessment
{Flag anything that looks fragile, under-tested, or that deviates from CLAUDE.md patterns}

## Recommendation
{One of:}
- ✅ **Merge and proceed** — Work looks solid, merge the branch and continue tomorrow
- ⚠️ **Review before merge** — {specific concern that needs human eyes}
- 🛑 **Do not merge** — {critical issue that needs manual intervention}

## Branch to review
`scheduled/{YYYY-MM-DD}-{slug}` — merge with:
\```bash
git checkout main && git pull
git merge origin/scheduled/{YYYY-MM-DD}-{slug}
git push origin main
\```
```

---

## If no scheduled branch exists today

This means either:
- The daily build sprint hasn't run yet (check timing)
- The laptop was asleep and the task was skipped
- All roadmap items were complete or locked

Write a brief note to DAILY_BRIEF.md:

```markdown
# Daily Brief — {YYYY-MM-DD}

## Summary
No scheduled build ran today. Possible reasons: laptop was asleep, all roadmap
items complete/locked, or the build task encountered an error.

## Action needed
Check the CoWork Scheduled sidebar for task execution status.
Check docs/HANDOFF.md for any notes from the last session.
```

---

## Hard rules

- **Never modify code files.** This task is read-only analysis.
- **Always overwrite DAILY_BRIEF.md** — it should only contain today's brief.
- **Be concise.** The goal is a 2-minute morning read, not a novel.
- **Be honest about quality.** If tests are failing, say so clearly. Don't minimize issues.
