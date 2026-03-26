---
name: generation-log
description: Track and query the history of all generated content across clients and formats. Use this skill before planning new content to check what's been generated recently and avoid repeating angles. Trigger on: "what have I generated this week", "what's been written for Brian", "check recent generations", "has this topic been covered", "morning scan", or any time the orchestrator needs cross-run awareness before planning. Log new generations with the append command. Query recent history before building a content manifest.
---

# Generation Log

Append-only log of every generated piece. Gives the engine cross-run memory — so it knows what it wrote yesterday when deciding what to generate today.

---

## Why this exists

Each generation run is isolated by default. Without a log, the morning scan might queue a post on the same topic that was generated two days ago. This skill solves that. It's the engine's short-term memory.

---

## Log file

`log/generations.jsonl` — one JSON object per line, newest entries at the bottom.

Each entry:
```json
{"date": "2026-03-18", "client": "brian", "format": "personal-linkedin", "title": "I killed the House of Fraud job board overnight", "quality_score": 10, "status": "approved", "pillar": "building-in-public", "angle": "overnight rebuild decision", "file": "drafts/brian/personal-linkedin/2026-03-18_personal_personal-linkedin_hof-job-board-rebuild.md"}
```

**Fields:**
- `date` — ISO date (YYYY-MM-DD)
- `client` — client slug (brian, house-of-fraud, safeguard, sayso)
- `format` — content format (personal-linkedin, company-linkedin, newsletter, twitter, blog)
- `title` — post title or question (for newsletters)
- `quality_score` — 0–10
- `status` — draft | approved | rejected | published
- `pillar` — content pillar tag (optional but useful for saturation detection)
- `angle` — one-phrase summary of the specific angle taken (helps distinguish two posts on the same topic)
- `file` — relative path to the draft file

---

## Appending a new entry

After every generation run, append to the log:

```bash
python .claude/skills/generation-log/scripts/query_log.py \
  --append '{"date": "2026-03-22", "client": "brian", "format": "personal-linkedin", ...}'
```

Or write the JSON line directly to `log/generations.jsonl` — the file is append-only plaintext.

**When to append:** After each piece passes the quality gate and is saved to `drafts/`. Append before moving to the next piece in a generation run.

---

## Querying recent history

```bash
# What's been generated for Brian this week?
python .claude/skills/generation-log/scripts/query_log.py --client brian --days 7

# All pieces on the building-in-public pillar, ever
python .claude/skills/generation-log/scripts/query_log.py --pillar building-in-public

# Last newsletter per client
python .claude/skills/generation-log/scripts/query_log.py --format newsletter --last 1

# Everything in the last 3 days across all clients
python .claude/skills/generation-log/scripts/query_log.py --days 3

# Check if a topic has been covered recently
python .claude/skills/generation-log/scripts/query_log.py --search "first-party fraud" --days 30
```

The script outputs plain text Claude can read inline — no need to load the full JSONL.

---

## Morning scan integration

Before building the content manifest, run:

```bash
python .claude/skills/generation-log/scripts/query_log.py \
  --client [active_client] --days 7 --summary
```

The `--summary` flag produces a compact view: formats generated, pillars covered, any pieces still in draft status. Load this output before deciding what to queue.

---

## Backfilling from cadence-log.yaml

The existing `performance/cadence-log.yaml` has generation history. To seed the log file:

```bash
python .claude/skills/generation-log/scripts/query_log.py --seed-from performance/cadence-log.yaml
```

This reads cadence-log entries and converts them to JSONL format. Run once to bootstrap the log.
