# /generate-weekly-report
# Generate the weekly performance report and populate performance/WEEKLY_REPORT.md.
# Run every Friday (or Monday morning for the previous week).
# Combines performance data, synthesis findings, and next-week priorities.
#
# Usage: /generate-weekly-report
# Optional: /generate-weekly-report --client=[name] --week=[YYYY-MM-DD]

---

## Step 1: Load all sources

Load:
1. `performance/tracker.yaml` — full performance history
2. `performance/tracker.csv` — confirm sync with yaml
3. `performance/insights.md` — current synthesized patterns
4. `performance/cadence-log.yaml` — what was generated and when
5. `config/cadence.yaml` — target frequencies
6. `SUCCESS_METRICS.md` — baseline thresholds for all channels
7. `learning/company-evolution.md` — current business state
8. `brand/[client]/pillars.md` — to identify topic coverage gaps

Scan `output/[client]/` and `drafts/[client]/` for all files created or published this week.

---

## Step 2: Define the week

Determine the week being reported:
- Default: Monday through Sunday of the most recent complete week
- If `--week` flag provided: use that Monday as start date

---

## Step 3: Compile published content

List all content objects with `status: published` and `created` within the report week.

For each:
- Format, voice profile, channel, title, date published
- Performance signal (from tracker.yaml if logged; otherwise note "not yet logged")
- Quality score from frontmatter

Also list:
- Pieces that moved to `status: draft` this week (generated but not published)
- Pieces that were archived this week

---

## Step 4: Performance analysis

For each active channel with published content this week:

**Compare against SUCCESS_METRICS.md baselines:**
- Is this channel at, above, or below baseline?
- What's the trend over the last 4 weeks?
- Any specific pieces that stood out (high or low)?

**Topic coverage:**
- Which pillars were covered this week?
- Are any pillars going more than 2 weeks without coverage?
- Are any topics appearing for the 3rd+ time in 30 days (saturation)?

**Quality gate review:**
- Average quality score for the week
- Any pieces that scored below 7 that still made it to published? (flag these)
- Any patterns in what the gate is catching?

---

## Step 5: Run synthesis if due

Check: are there 5+ unanalyzed entries in `performance/tracker.yaml`?

If yes:
→ Run the synthesis logic from `/synthesize-learnings`
→ Update `performance/insights.md`
→ Include synthesis findings in the report

If no:
→ Note how many entries are pending: "Need [n] more performance entries before next synthesis."

---

## Step 6: Check SUCCESS_METRICS thresholds

Compare this week's averages against thresholds in `SUCCESS_METRICS.md`.

Generate cadence proposals if thresholds are crossed:

```
CADENCE REVIEW:

Personal LinkedIn: [avg signal] vs [baseline]
→ [HOLD / PROPOSE INCREASE to Nx/week / PROPOSE DECREASE to Nx/week]
   Reason: [specific data point]

Newsletter: [open rate] vs [baseline open rate]
→ [HOLD / FLAG FOR REVIEW]
   Reason: [specific signal]

[etc.]
```

---

## Step 7: Generate next-week priorities

Based on:
- Pillars with coverage gaps
- Formats below cadence target
- Topics with strong recent performance (worth returning to)
- Any inputs in `inputs/` not yet processed
- Business changes from `learning/company-evolution.md`

Produce a ranked priority list for next week's content:

```
NEXT WEEK PRIORITIES:

1. [Format] — [Channel] — [Reason this is the top priority]
   Suggested angle: [specific angle based on current context]

2. [Format] — [Channel] — [Reason]
   Suggested angle: [angle]

3. [Format] — [Channel] — [Reason]
   Suggested angle: [angle]

Inputs to process first:
- [input file if any are sitting unprocessed]
```

---

## Step 8: Populate WEEKLY_REPORT.md

Write all findings into `performance/WEEKLY_REPORT.md`, replacing the template placeholders.

Use the existing report template structure. Do not add extra sections.
Do not generate filler — if a section has no data, write "No data this week" not a generic explanation.

---

## Step 9: Output summary

```
WEEKLY REPORT COMPLETE — Week of [date]

Published this week: [n] pieces
Performance trend: [improving / holding / declining]
Top performer: "[title]" — [signal] signal
Lowest performer: "[title]" — [signal] signal

[n] synthesis findings updated in performance/insights.md

Cadence proposals: [n]
  [List proposals if any]

Next week's top priority: [one-line summary]

Full report: performance/WEEKLY_REPORT.md
```

---

## Step 10: Learning archive entry

Append a summary entry to `learning/weekly-synthesis.md`:

```
---

## Week of [YYYY-MM-DD]

### What published
[List]

### What performed
[Top signals]

### What didn't
[Low signals]

### What changed in the business
[Pull from company-evolution.md if updated this week]

### What to do differently next week
[Top 1-2 adjustments from the synthesis]

### Synthesis notes
[Key findings from synthesis if it ran]
```
