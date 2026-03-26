# /synthesize-learnings
# Read all performance data and update performance/insights.md with patterns.
#
# Run this after logging 5+ new performance entries.
# This command is the engine learning — it reads what worked, what didn't,
# and writes updated guidance that generators use going forward.
#
# Usage: /synthesize-learnings
# Optional: /synthesize-learnings --client=[name]

---

## Step 1: Load all data

**⚠ Load these FIRST:**
- `knowledge/INDEX.md` — confirms file locations and current active state
- `knowledge/ERRORS.md` — all open errors. Resolving errors is part of this command's job.
- `skills/synthesize-learnings.md` — the full synthesis logic. Follow that skill's Plan→Work→Assess→Compound loop.

Then load:
- `QUALITY_GATE.md` — to correlate quality scores with real performance outcomes
- `SUCCESS_METRICS.md` — channel baselines (determines if cadence proposals are warranted)
- `performance/tracker.yaml` — full performance history
- `performance/tracker.csv` — cross-reference for data integrity
- `performance/insights.md` — current synthesized state (what was known before this run)
- `performance/WEEKLY_REPORT.md` — last report for recent context
- `config/cadence.yaml` — formats currently in use and their targets
- `learning/voice-calibration-log.md` — voice corrections already noted
- `learning/company-evolution.md` — current company state

---

## Step 2: Analyze the tracker data

Group entries by:
- Format (personal-linkedin, newsletter, blog, etc.)
- Pillar
- Voice profile (personal vs company)
- Performance signal (high / medium / low / none)

For each format with at least 3 entries, identify:

**What patterns correlate with high performance?**
- Opening styles (what first lines/structures appear in high-performing posts?)
- Length ranges
- Content reasons (insight / opinion / story / announcement / education / proof)
- Topics or angles
- Any structural elements (CTAs, use of specific data, named clients, etc.)

**What patterns correlate with low/no performance?**
- Same analysis in reverse
- Are there formats or topics that consistently underperform?

**What's the current topic saturation picture?**
- Topics covered 3+ times in the last 30 days
- Topics covered 0-1 times despite being core pillars (opportunity signal)

**What's the cadence picture?**
- Are we over-posting on any channel?
- Are there channels where we've been quiet too long?

---

## Step 3: Write updated insights

Rewrite `performance/insights.md` with fresh analysis.

Keep the same section structure:
- What's working
- What's not working
- Topics that are saturated
- Topics with untapped potential
- Format observations
- Cadence observations

Write in plain, specific language. No generic advice.

Examples of useful insight writing:
✓ "Personal LinkedIn posts that open with a specific dollar amount or client name outperform posts that open with a question — 3 of the last 4 high performers started this way."
✓ "Newsletter open rates are fine; reply rate is the real signal. The section that generates replies is always the personal story section, not the tactical tips."
✗ "Engaging content performs better than non-engaging content."
✗ "Keep posts short and punchy for maximum impact."

Mark each insight as:
`[strong]` — 3+ data points support this
`[emerging]` — 1-2 data points, worth testing
`[hypothesis]` — not yet in data but worth flagging based on patterns

---

## Step 4: Note voice calibration opportunities

If patterns suggest voice calibration is needed:
- Flag specific phrases or structures that keep appearing in low-performers
- Flag specific phrases or structures from high-performers worth capturing in voice profiles
- Add a note to `learning/voice-calibration-log.md` with the observation

---

## Step 5: Mark entries as synthesized

In `performance/tracker.yaml`, add `synthesized: true` to all entries analyzed in this run.

---

## Step 6: Report

Output a summary of what was found:

"Learnings synthesized from [n] entries.

**Key findings:**
- [Finding 1 — the most actionable insight]
- [Finding 2]
- [Finding 3 if applicable]

**Recommended adjustment:**
[One specific change to make — to cadence, voice profile, or content approach]

Updated `performance/insights.md` with [n] insights.
[n] entries marked as synthesized."
