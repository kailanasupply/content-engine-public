---
name: performance-intelligence
description: Analyze content performance and surface patterns for generation planning. Use this skill when running the morning scan, synthesizing learnings, asking what's performing well, checking topic saturation, or deciding what to generate next. Trigger on: "synthesize learnings", "what's working", "what should I generate", "analyze performance", "topic saturation check", "morning scan", or any time the orchestrator needs to ground a content plan in performance data. Run the analysis script first to refresh insights, then load the relevant insight files before planning.
---

# Performance Intelligence

Scripts and structured insight files that ground content decisions in what's actually working.

---

## What this skill does

Reads `performance/tracker.yaml` (published results) and `performance/cadence-log.yaml` (generation history) and produces structured insight files Claude can load before planning new content.

Two modes:

**Refresh mode** — run the analysis script to regenerate all insight files from current data. Do this when data has changed since the last run, or when `cache/last-analysis.json` is older than 7 days.

**Load mode** — skip the script, load the pre-generated insight files directly. Faster. Use when the cache is recent and data hasn't changed.

---

## Running the analysis

```bash
python .claude/skills/performance-intelligence/scripts/analyze_performance.py \
  --tracker performance/tracker.yaml \
  --cadence performance/cadence-log.yaml \
  --output .claude/skills/performance-intelligence/insights/ \
  --cache .claude/skills/performance-intelligence/cache/last-analysis.json
```

The script writes four insight files and updates the cache timestamp. If data hasn't changed since the last run (same file hash), it skips regeneration and exits 0.

**Exit codes:**
- `0` — analysis complete (or skipped — data unchanged)
- `1` — error reading input files
- `2` — no data to analyze (both files empty or missing entries)

---

## Loading insight files after analysis

Load the files relevant to what you're planning. Don't load all four every time.

| File | Load when |
|------|-----------|
| `insights/by-format.md` | Planning what format to generate next |
| `insights/by-client.md` | Planning for a specific client |
| `insights/topic-saturation.md` | Checking whether a topic has been covered too recently |
| `insights/structural-patterns.md` | Deciding on post length, hook style, or structure |

For morning scan: load `topic-saturation.md` and `by-client.md` at minimum.
For campaign planning: load all four.

---

## When to refresh vs. skip

Check `cache/last-analysis.json`:
- `last_run` older than 7 days → refresh
- New entries in cadence-log since `last_run` → refresh
- Cache recent and no new data → skip, load directly

---

## What the insight files contain

Each file is plain markdown with observations Claude can read as context. They are written in the same voice as `performance/insights.md` — pattern observations, not rules.

The script also updates `performance/insights.md` directly with a summary view, so the main insights file stays current without manual edits.

---

## Adding to this skill over time

When a piece performs exceptionally well or poorly:
1. Log it in `performance/tracker.yaml` with `/log-performance`
2. Run this skill to regenerate insights
3. If the pattern is new, it will surface automatically in `by-format.md` or `structural-patterns.md`

The insight files get more accurate with more data. They're most useful after 10+ tracked entries per client.
