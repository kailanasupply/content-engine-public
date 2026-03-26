# /morning-scan
# Daily content intelligence run — multi-brand.
#
# ENTRY POINT: Load skills/morning-content-scan.md and follow its Plan→Work→Assess→Compound loop.
# This command is a thin wrapper. The full logic lives in skills/morning-content-scan.md.
#
# MANDATORY FIRST STEPS:
# 1. Read knowledge/INDEX.md — confirm active brands and open errors
# 2. Read knowledge/ERRORS.md — check for blocking issues
# 3. Load skills/morning-content-scan.md — follow that skill's loop exactly
#
# This command NEVER auto-generates content without human approval.
# It produces a plan. You approve. Then generation runs.
#
# Usage: /morning-scan
# Optional: /morning-scan --brand=[name] to scan one brand only

---

## Step 1: Load context

**⚠ Load these files FIRST — before anything else:**
1. `knowledge/INDEX.md` — master router. Confirms active brands, file locations, and open errors.
2. `knowledge/ERRORS.md` — check for blocking issues before proceeding.
3. `skills/morning-content-scan.md` — the full scan logic. Follow that skill's Plan→Work→Assess→Compound loop.

Then load:
4. `anti-ai-rules.md` — writing rules. Even scan report language should not use banned words.
5. `knowledge/QUALITY_GATE.md` — 4-level scoring rubric. Use this when evaluating whether proposed pieces are worth generating.
3. `knowledge/FREQUENCY_GUIDE.md` — cadence philosophy. This informs prioritization and what to flag as noise.

Then load operational config:
4. `config/settings.yaml` — ALL registered brands and their channel restrictions
5. `config/cadence.yaml` — machine-readable frequency rules including brand_overrides
6. `performance/cadence-log.yaml` — when each format was last generated per brand
7. `performance/insights.md` — what's been performing

---

## Step 2: Identify active brands for this scan

Read `config/settings.yaml` brands section. Collect all brands with `active: true`.

Default brands to scan: brian, safeguard, house-of-fraud, sayso

If `--brand=[name]` flag was passed → scan only that brand.

For each brand, note its:
- `active_channels` — what the scan can propose for this brand
- `blocked_channels` — formats to never propose (critical for sayso)
- Available voice profiles

---

## Step 3: Scan for new inputs (all types)

Check these directories for files created or modified in the last 24 hours:
- `inputs/recordings/` — audio files
- `inputs/notes/` — text notes
- `inputs/briefs/` — campaign briefs
- `inputs/processed/` — transcripts not yet used for generation
- `inputs/inspiration/` — liked posts, quick ideas, observations (NEW)

For each new input:
- Identify type (recording / notes / brief / inspiration / processed-transcript)
- Identify which brand it belongs to (from frontmatter `client:` field, filename prefix, or content)
- If brand is ambiguous → assign to `brian` by default, flag for clarification
- Identify richness level (high = recording or 500+ word notes | medium = 200-500 words | low = <200 words or inspiration item)
- Skip if: admin/logistics only, already processed and used

**Inspiration items:** If any new files are in `inputs/inspiration/` → run `/process-inspiration` first, then include any queued proposals in this scan.

If NO new inputs AND no queued inspiration proposals AND no unprocessed processed-transcripts:
→ Output: "No new inputs found in the last 24 hours. Nothing to generate today."
→ Stop.

---

## Step 4: Load brand context for brands with inputs

For each brand that has new inputs:
- Load `brand/[brand]/voice-personal.md` (if available and brand has personal voice)
- Load `brand/[brand]/voice-company.md`
- Load `brand/[brand]/pillars.md`
- Load `learning/company-evolution.md`

For SaySo specifically: also load `brand/sayso/channel-notes/CHANNEL_RESTRICTIONS.md`

---

## Step 5: Apply cadence rules per brand

For each brand with inputs, determine eligible formats:

1. Check `config/cadence.yaml` brand_overrides for this brand
2. Check `active: false` or `blocked: true` → never propose blocked formats
3. Check `performance/cadence-log.yaml` → has this format been generated recently for this brand?
4. Apply min_gap_days and max_per_week rules
5. Apply noise prevention: topic saturation, richness requirement, content reason

**SaySo hard check:** Before adding any SaySo proposal, confirm format is in [twitter, company-linkedin]. If not — remove it from proposals. Log: "Skipped [format] for SaySo — channel blocked."

Build generation list per brand.

---

## Step 5: Prioritize

Apply the priority order from cadence.yaml:
1. personal-linkedin
2. company-linkedin
3. newsletter
4. blog
5. twitter

If the total eligible pieces exceed `daily_max_pieces` (default 5):
- Keep the top pieces by priority order
- Move the rest to "deferred" list in the scan report

---

## Step 6: Load performance context

Load `performance/insights.md` and `performance/tracker.yaml` (last 10 entries).

For each proposed piece, note:
- Is this angle or format currently trending up or down in performance?
- Has this topic been over-covered recently (saturation check)?
- Are there specific structural choices (length, hook style) that recent performance data suggests?

Add performance notes to each proposed piece in the scan report.

---

## Step 7: Produce the scan report

Output a unified multi-brand SCAN REPORT:

---

```
MORNING SCAN — [DATE]
Brands scanned: brian | safeguard | house-of-fraud | sayso
New inputs: [n total]
Total proposed pieces: [n total across all brands]
```

---

### NEW INPUTS (all brands)

| Input | Brand | Type | Richness | Key theme |
|-------|-------|------|----------|-----------|
| [filename] | [brand] | [type] | [level] | [one-line] |

(Inspiration items marked with ✨)

---

### GENERATION QUEUE — BRIAN
[n proposals | Personal LinkedIn [n] | Company LinkedIn [n] | Newsletter [n] | ...]

**1. [Format] — [Voice]**
Source: [input file] | Pillar: [pillar] | Reason: [insight/opinion/story/etc.]
Angle: "[specific angle]"
Cadence: ✓ last generated [n] days ago

[...additional brian proposals...]

---

### GENERATION QUEUE — SAFEGUARD
[n proposals]
[Same format per piece]

---

### GENERATION QUEUE — HOUSE OF FRAUD
[n proposals]
[Same format per piece]

---

### GENERATION QUEUE — SAYSO ⚠ X + LINKEDIN ONLY
[n proposals | Only Twitter and Company LinkedIn appear here]

**1. Twitter — company voice**
Source: [input] | Pillar: [pillar] | Reason: [reason]
Angle: "[specific angle]"
Cadence: ✓

[...sayso proposals — never newsletter, never personal LinkedIn...]

---

### DEFERRED (cadence rules)

| Brand | Format | Reason |
|-------|--------|--------|
| [brand] | [format] | [e.g., "newsletter last generated 3 days ago, min gap 7"] |
| sayso | personal-linkedin | BLOCKED — not an active channel for SaySo |

---

### SKIPPED INPUTS

| Input | Brand | Reason |
|-------|-------|--------|
| [filename] | [brand] | [reason] |

---

### RECOMMENDED ACTION

[Two-sentence summary — total pieces proposed, any important flags]

---

**Reply `go` to generate all queued pieces.**
**Reply `go brian` to generate only Brian's pieces.**
**Reply `go sayso` to generate only SaySo's pieces.**
**Reply `edit` to modify the queue before generating.**
**Reply `skip` to skip today.**

---

## Step 8: Wait for approval

After presenting the scan report, STOP and wait for user input.

**If user replies `go` or `yes` or approves:**
→ Run `/generate-campaign` for each piece in the queue, using the proposed angle
   as the campaign context, respecting voice_profile and cadence settings.
→ After generation completes, update `performance/cadence-log.yaml` with
   today's generation dates.

**If user replies `edit queue`:**
→ Ask what changes they want
→ Revise the queue
→ Re-present the modified scan report
→ Wait for approval again

**If user replies `skip` or `no`:**
→ Log the skip in cadence-log.yaml with reason "manual skip"
→ Confirm: "Got it — nothing generated today."

**If user replies with modifications:**
→ Parse their intent and adjust the queue accordingly before generating

---

## Notes for the 7am scheduled run

When running on the scheduled automation (not manually):
- Default to the active_client in settings.yaml
- The scan report is the OUTPUT — it does not auto-generate
- The schedule skill will need to notify you (via the session output) that the scan is ready to review
- You review the report and reply `go` to trigger generation

The point of the morning scan is to make you decide — not to generate noise while you sleep.
