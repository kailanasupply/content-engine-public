---
name: evergreen-miner-task
description: Monthly evergreen miner — surfaces top 3 archive candidates based on current performance trends and queues them for repurposing. Run on the 1st of each month.
schedule: "0 8 1 * *"  # 8am on the 1st of every month
taskId: content-engine-evergreen-miner
---

# Monthly Evergreen Miner

Surfaces the top 3 ideas from the evergreen archive worth repurposing this month, scored against current performance trends. Produces a report — does NOT generate content automatically.

---

## TASK PROMPT
*(Copy this verbatim when creating the scheduled task)*

You are running the monthly evergreen content miner for the Content Ecosystem Engine.

## Objective
Read the evergreen candidates archive, cross-reference with current performance trends, and surface the top 3 ideas worth repurposing this month. Do NOT generate content — produce a surfacing report and wait for approval.

## Location
The Content Ecosystem Engine lives at: ~/Desktop/ContentEngine

---

## Step 1 — Load context

Read these files in order:
- `~/Desktop/ContentEngine/config/settings.yaml` — active client, brand settings
- `~/Desktop/ContentEngine/performance/insights.md` — what's currently performing well (topics, formats, angles)
- `~/Desktop/ContentEngine/performance/cadence-log.yaml` — what formats have been generated recently
- `~/Desktop/ContentEngine/performance/tracker.yaml` — raw performance log entries

From insights.md, extract:
- Top performing topics/pillars right now
- Formats that are working (personal-linkedin, newsletter, etc.)
- Any angles explicitly noted as resonating with the audience

---

## Step 2 — Read the evergreen candidates archive

List all files in `~/Desktop/ContentEngine/archive/evergreen-candidates/`

For each file:
1. Read its content
2. Extract: original title, core insight (1 sentence), pillar/theme, original date
3. Check `~/Desktop/ContentEngine/.claude/skills/generation-log/log/generations.jsonl` to see if it's been repurposed recently — skip any idea repurposed in the last 90 days

---

## Step 3 — Score each candidate against current performance trends

For each unrepurposed evergreen candidate, score it 0–10:

**Relevance to current trends (0–4 points)**
- 4: Core topic directly matches a top-performing pillar from insights.md
- 3: Adjacent to a top-performing topic
- 2: Loosely related
- 1: Unrelated but timeless
- 0: Topic is saturated (covered 3+ times in last 30 days per insights.md)

**Freshness of angle (0–3 points)**
- 3: The specific angle hasn't been used in 90+ days
- 2: Similar angle used 60–90 days ago
- 1: Similar angle used 30–60 days ago
- 0: Same angle used in last 30 days — skip

**Narrative strength (0–3 points)**
- 3: Has a specific story, number, or concrete scenario as its hook
- 2: Has a clear POV but abstract
- 1: Idea is interesting but underdeveloped
- 0: Too thin to anchor a post

---

## Step 4 — Select top 3

Pick the 3 highest-scoring candidates (minimum score: 6/10 to qualify).

If fewer than 3 candidates score ≥ 6, report how many qualified and why others were skipped.

For each selected candidate, generate:
1. **Best repurpose angle** — specific, not generic
2. **Recommended format** — personal-linkedin, newsletter, X thread, or company-linkedin
3. **Why now** — 1 sentence connecting this idea to something currently resonant
4. **Suggested title** — working title for the repurposed piece

---

## Step 5 — Produce the evergreen miner report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌱 EVERGREEN MINER — [Month YYYY]
Active client: [client] | Candidates evaluated: [n]
Qualified (score ≥ 6): [n] | Selected: top 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1 — [SCORE: X/10] "[Original title]"
Archive file: [filename]
Core insight: [1 sentence]
Best angle: "[specific repurpose angle]"
Format: [recommended format]
Why now: [1 sentence]
Working title: "[suggested title]"

#2 — [same structure]

#3 — [same structure]

━━━ SKIPPED ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Candidates that scored < 6 and brief reason why]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To repurpose: /repurpose [archive file path]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Constraints
- Never generate content automatically
- Skip any candidate repurposed in the last 90 days
- Skip saturated topics (3+ pieces in last 30 days)
- Minimum score 6/10 to qualify
- Maximum 3 candidates surfaced per run

---

## TO REGISTER AS A SCHEDULED TASK

Open a fresh Cowork session (not the morning scan session) and run:

> "Create a scheduled task called `content-engine-evergreen-miner` that runs on the 1st of every month at 8am. Use the prompt from `ContentEngine/skills/evergreen-miner-task.md`."
