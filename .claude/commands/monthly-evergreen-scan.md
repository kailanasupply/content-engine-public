# /monthly-evergreen-scan
# Surfaces the best archived ideas ready for a fresh spin this month.
# Accounts for recent content, cadence eligibility, and brand fit.
# Run at the start of each month (or anytime you need a repurposing queue).
#
# Usage: /monthly-evergreen-scan
# Optional: /monthly-evergreen-scan --brand=[name] to filter by brand
# Optional: /monthly-evergreen-scan --theme=[theme] to filter by theme

---

## Step 1: Load context

Load in this order:

1. `anti-ai-rules.md`
2. `QUALITY_GATE.md`
3. `config/settings.yaml` — all active brands and their active/blocked channels
4. `config/cadence.yaml` — current cadence rules and recent generation log
5. `performance/tracker.yaml` — what's been published in the last 60 days across all brands
6. `performance/cadence-log.yaml` — what formats have been generated recently
7. `performance/insights.md` — what's performing (informs which topics are worth refreshing)

---

## Step 2: Inventory evergreen candidates

Scan `archive/evergreen-candidates/` for all files:

For each file, extract:
1. **Filename** and **original date** (from the `YYYY-MM-DD-` prefix)
2. **Age** — how many days/months since it was archived
3. **Core insight** — read the file and extract the central idea in one sentence
4. **Theme tags** — identify which core themes are present: dad-life | fraud | building | trust | leadership | personal growth | other
5. **Last repurposed** — check if this file appears as `repurposed_from:` in any draft or published piece in `drafts/` or `performance/tracker.yaml`

Build an internal candidate list before scoring.

---

## Step 3: Score each candidate

Score every candidate on a simple 3-dimension rubric (1–3 each, max 9):

**Dimension 1: Freshness window (1–3)**
- 3 — Archived 6+ months ago and never repurposed
- 2 — Archived 3–6 months ago, or repurposed once 6+ months ago
- 1 — Archived less than 3 months ago, or repurposed in last 3 months

**Dimension 2: Topic saturation (1–3)**
- 3 — Topic hasn't appeared in published content in 60+ days for any brand
- 2 — Topic appeared 30–60 days ago
- 1 — Topic appeared in the last 30 days (flag as recently covered)

**Dimension 3: Resonance potential (1–3)**
- 3 — Strong narrative hook; story-driven; would work across multiple formats
- 2 — Clear insight but needs more craft to become a standout piece
- 1 — Thin idea; might need to be combined with another item to have enough to say

**Disqualify if:**
- The same angle was published within the last 14 days for any active brand
- The core idea is tied to a news event that has passed (no longer relevant)

---

## Step 4: Filter and rank

Sort all non-disqualified candidates by total score (highest first).

Select the top 5–10:
- Minimum score: 5/9
- Maximum: 10 items in the report (never list more than 10 — the goal is a focused shortlist, not a dump)
- If there are fewer than 5 qualifying candidates: report all qualifying, plus suggest seeding new inspiration items via `/process-inspiration`

---

## Step 5: Present the scan report

```
MONTHLY EVERGREEN SCAN — [Month YYYY]
Run date: [today]
Candidates reviewed: [n]
Qualifying for refresh: [n]
Disqualified: [n] ([reason summary])

---

TOP EVERGREEN CANDIDATES THIS MONTH

[Rank]. [Score]/9 — "[Core insight — one sentence]"
   File: [filename]
   Archived: [date] ([X months ago])
   Themes: [tag1, tag2]
   Last repurposed: [never / X months ago]
   Topic coverage: [last published: X days ago / not recently covered]
   Best formats now: [channel 1] (brian), [channel 2] (brian), [channel 3 if SaySo-eligible] (sayso)
   Why now: [one sentence — what makes this timing good or the angle fresh]

[Rank]. [Score]/9 — "[Core insight]"
   ...

---

DISQUALIFIED THIS MONTH

- [filename]: [reason — too recent / topic saturated / news-tied]
- ...

---

SUGGESTED NEXT STEPS

1. Run /repurpose-idea on your top pick:
   /repurpose-idea [path to #1 candidate]

2. Queue multiple for this month's content:
   /repurpose-idea [path to #2]
   /repurpose-idea [path to #3]

3. If the archive is thin (fewer than 5 candidates), run:
   /process-inspiration — to process any new inspiration items
```

---

## Step 6: Optional — queue for repurposing

After presenting the report, ask:

"Would you like to repurpose any of these now? (enter numbers, 'all top 3', or 'no')"

- If numbers selected → run `/repurpose-idea` on each selected file in sequence
- If 'all top 3' → run `/repurpose-idea` on items ranked 1, 2, 3
- If 'no' → close with the report saved to `performance/evergreen-scan-[YYYY-MM].md`

---

## Step 7: Save the scan log

Always save the scan report to:
```
performance/evergreen-scan-[YYYY-MM].md
```

This creates a running record of what was surfaced each month, what was repurposed, and what was skipped — so future scans can reference it and avoid re-surfacing the same items repeatedly.

Include in the saved file:
```yaml
---
scan_date: [YYYY-MM-DD]
month: [YYYY-MM]
candidates_reviewed: [n]
items_in_report: [n]
items_queued_for_repurpose: [n] or none
items_disqualified: [n]
---
```
