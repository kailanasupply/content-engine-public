---
name: synthesize-learnings
description: The Compound phase of the loop. Reads all performance data, updates performance/insights.md with real patterns, logs drift to knowledge/ERRORS.md, proposes voice profile edits, and updates cadence rules. Run after logging 5+ performance entries, every Monday, or after any generation run where quality scores were inconsistent. Trigger: /synthesize-learnings, "update learnings", "what's working", "update insights", "compound the learnings".
triggers:
  - /synthesize-learnings
  - update learnings
  - what's working
  - update insights
  - compound the learnings
  - weekly synthesis
loop: This IS the Compound phase
---

# Synthesize Learnings

The Compound step. This is how the engine gets smarter. Every performance data point, every voice correction, every quality score feeds back in here. Run this at least weekly.

---

## LOOP: This skill IS the Compound phase

---

## Phase 1: PLAN

Load everything that has learning signal:
1. `knowledge/INDEX.md` — what files exist and their current state
2. `knowledge/ERRORS.md` — all flagged issues since last synthesis. This is a priority read.
3. `performance/tracker.yaml` + `performance/tracker.csv` — full performance history
4. `performance/insights.md` — current synthesized state (what was known before this run)
5. `performance/cadence-log.yaml` — generation history
6. `.claude/skills/generation-log/log/generations.jsonl` — all generated pieces with scores
7. `learning/voice-calibration-log.md` — previous voice corrections
8. `learning/company-evolution.md` — current business context
9. `QUALITY_GATE.md` — scoring rubric to correlate scores with outcomes
10. `SUCCESS_METRICS.md` — performance baselines

Run performance-intelligence script:
```bash
python .claude/skills/performance-intelligence/scripts/analyze_performance.py \
  --tracker performance/tracker.yaml \
  --cadence performance/cadence-log.yaml \
  --output .claude/skills/performance-intelligence/insights/ \
  --insights-file performance/insights.md
```

---

## Phase 2: WORK

### Step 2a: Analyze quality scores vs. outcomes

Pull all entries from `generations.jsonl` that have both a quality_score AND a performance signal from tracker.yaml.

For each pairing, note: did high quality scores correlate with high engagement? Where did they diverge?

If quality score ≥ 8 but engagement was low → what voice or structural element may have killed reach despite good writing?
If quality score ≤ 7 but engagement was high → what are we missing in the scoring rubric?

### Step 2b: Pattern extraction per format

For each format with 3+ entries, find patterns:

**What correlates with high performance?**
- Opening structures (specific vs. question vs. statement)
- Length ranges
- Pillar/topic combinations
- Whether personal story or data-led

**What correlates with low performance or rejection?**
- Specific phrases or structures from `knowledge/ERRORS.md`
- Any banned patterns that slipped through
- Generic hooks, weak specificity signals

### Step 2c: Topic saturation analysis

```bash
python .claude/skills/generation-log/scripts/query_log.py --days 30 --summary
```

Flag any topic appearing 3+ times in 30 days as saturated for that brand.
Flag any core pillar not appearing in 30 days as "opportunity gap."

### Step 2d: Cadence analysis

For each brand × format:
- How often are we hitting the target frequency?
- Any formats going dark (0 pieces in 30 days despite being an active channel)?
- Any formats being overused (violating max_per_week)?

### Step 2e: Process ERRORS.md

Read every open error in `knowledge/ERRORS.md`.

For each error:
- **Resolved?** Mark as resolved with date.
- **Pattern?** If same error has appeared 2+ times → propose a fix to the system (cadence rule, voice profile update, channel restriction update).
- **Systemic?** If an error points to a structural problem (e.g., SaySo channel block happening repeatedly) → propose a CLAUDE.md or config update.

---

## Phase 3: ASSESS

Before writing updates, apply a self-check:

1. Are the insights specific enough to be actionable?
   Bad: "Personal posts perform better when they're authentic."
   Good: "Posts opening with a specific number or client outcome (not a question) have outperformed 3:1 in the last 30 days."

2. Are recommendations based on 3+ data points (strong) or 1–2 (emerging/hypothesis)?
   Label each: `[strong]` | `[emerging]` | `[hypothesis]`

3. Does any insight contradict the current voice profiles? → Flag for voice calibration.

---

## Phase 4: COMPOUND

### Update performance/insights.md

Rewrite with fresh patterns. Keep structure:
- What's working (with evidence)
- What's not working (with evidence)
- Topic saturation (with counts)
- Opportunity gaps (pillars underrepresented)
- Format observations
- Cadence observations
- Voice notes

Mark each insight strength: `[strong]` / `[emerging]` / `[hypothesis]`

### Update knowledge/ERRORS.md

- Mark resolved errors as `[RESOLVED: date]`
- Add any new patterns found
- Add any proposed system fixes

### Update learning/voice-calibration-log.md

If patterns suggest voice drift:
- Log the specific phrase or structure that keeps appearing in low-performers
- Log the specific phrase from high-performers worth capturing
- Flag which voice profile needs updating

### Propose voice profile edits

If 3+ examples suggest a specific pattern:
```
PROPOSED UPDATE: brand/[client]/voice-personal.md
Line to add: "[specific rule based on evidence]"
Evidence: [3 examples from tracker/generation-log]
Confidence: [strong|emerging]
```
Do not auto-edit voice profiles. Present the proposal and wait for approval.

### Update cadence recommendations

If analysis shows format over/underuse:
```
PROPOSED CADENCE CHANGE: config/cadence.yaml
Brand: [brand] | Format: [format]
Current: [current rule]
Proposed: [new rule]
Reason: [specific evidence]
```

---

## Output format

```
═══════════════════════════════════════════════════
LEARNINGS SYNTHESIZED — [DATE]
Entries analyzed: [n tracker] + [n generation-log]
Errors resolved: [n] | New patterns found: [n]
═══════════════════════════════════════════════════

KEY FINDINGS:

  1. [Most actionable insight — strong/emerging/hypothesis]
  2. [Second finding]
  3. [Third finding]

TOPIC SATURATION:
  Saturated (3+ in 30 days): [topic list]
  Opportunity gaps: [pillar list]

ERRORS.MD UPDATES:
  Resolved: [n errors closed]
  New patterns: [n added]

PROPOSED VOICE UPDATES:
  [proposal or "none this cycle"]

PROPOSED CADENCE CHANGES:
  [proposals or "none this cycle"]

Updated: performance/insights.md | learning/voice-calibration-log.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Approve voice/cadence changes? yes | edit | skip
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
