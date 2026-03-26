---
name: content-repurposer
description: Surface evergreen ideas from the archive and turn them into new content with fresh angles. Use when inputs/ is empty, for monthly evergreen scans, or when explicitly repurposing a specific idea. Trigger: /repurpose-idea, /monthly-evergreen-scan, "repurpose from archive", "what old ideas can I reuse", "find evergreen content", or when morning scan finds no new inputs.
triggers:
  - /repurpose-idea
  - /monthly-evergreen-scan
  - repurpose from archive
  - what old ideas can I reuse
  - find evergreen content
  - nothing new in inputs
loop: Plan → Work → Assess → Compound
---

# Content Repurposer

Mines the archive for ideas worth giving a second life. This is how the engine compounds — every good idea from the past becomes fuel for the future.

---

## LOOP: Plan → Work → Assess → Compound

---

## Phase 1: PLAN

Load in order:
1. `knowledge/INDEX.md` — what's in the archive and when it was last mined
2. `knowledge/ERRORS.md` — any previously flagged issues with evergreen candidates
3. `anti-ai-rules.md`
4. `config/settings.yaml` — active brands and channel restrictions
5. `.claude/skills/evergreen-miner/freshness-rubric.md` — how to score candidates
6. `.claude/skills/evergreen-miner/cluster-themes.md` — campaign clusters per brand
7. `performance/insights.md` — what formats and angles are currently working

Determine scan scope:
- **Standard repurpose:** Check `archive/evergreen-candidates/` only (fast, high-signal)
- **Monthly deep scan** (triggered by `/monthly-evergreen-scan`): Check full archive including `archive/YYYY-MM/` folders

---

## Phase 2: WORK

### Step 2a: Run the miner

```bash
# Standard scan
python .claude/skills/evergreen-miner/scripts/mine_evergreen.py \
  --top 5 --threshold 5

# Monthly deep scan
python .claude/skills/evergreen-miner/scripts/mine_evergreen.py \
  --full-archive --top 10 --threshold 5 --force

# Specific idea (from /repurpose-idea [keyword])
python .claude/skills/evergreen-miner/scripts/mine_evergreen.py \
  --full-archive --search "[keyword]" --force
```

Read the output. For each surfaced candidate, note:
- Score (X/10)
- Suggested angle from miner
- Last used (from generation log)
- Pillar and cluster membership

### Step 2b: Generate repurpose angles

For each strong candidate (score ≥ 7), generate 2 specific repurpose angles:

**Angle type 1: Fresh lens** — same core insight, different entry point
- Original: "First 90 days running fraud with AI"
- Fresh lens: "What the first 90 days taught me about what AI can't do"

**Angle type 2: Cross-brand** — same idea adapted for a different brand's voice
- Original: brian personal LinkedIn
- Cross-brand: house-of-fraud company newsletter (different voice, same insight)

**Angle type 3: Format shift** — same idea in a structurally different format
- Original: narrative LinkedIn post
- Format shift: Twitter thread with numbered takeaways

For each angle, confirm it clears the duplicate test:
```bash
python .claude/skills/generation-log/scripts/query_log.py --client [brand] --search "[angle keyword]" --days 60
```

### Step 2c: Check channel restrictions

For each proposed piece:
- Confirm format is active for the brand
- SaySo: only twitter + company-linkedin
- Apply cadence check: has this format been overused recently for this brand?

### Step 2d: Cluster detection

Check `cluster-themes.md` — if 2+ candidates share a cluster theme:
→ Flag as campaign opportunity: "3 ideas in the AI-and-fraud cluster — could anchor a mini-series"
→ Propose the series structure if appropriate

---

## Phase 3: ASSESS (Synthetic Persona Review)

Run each repurpose proposal through the 3 personas:

**Persona A — Skeptical Reader**
"Given that some version of this idea may have been seen before, does this angle feel fresh enough to stop the scroll?"
Score 0–3 (extra weight here — recycled ideas get judged harder on freshness)

**Persona B — Ideal ICP**
"Is this still relevant to what I care about today? Or does it feel like old news?"
Score 0–3

**Persona C — Platform Fit**
"Does the new angle work structurally for the platform?"
Score 0–3

Minimum to proceed: 6/9 for repurposed content (same threshold as new content — no special treatment for archive material).

---

## Phase 4: COMPOUND

1. Update `archive/evergreen-candidates/` mined-ideas.jsonl status:
   - Surfaced candidates → `status: surfaced`
   - If generation approved → update to `status: approved` after drafts are saved

2. Update `knowledge/ERRORS.md`:
   - Candidates that scored < 5/10 on rubric → "Low freshness score: [candidate] — [rubric breakdown]"
   - Any cluster campaigns flagged → "Campaign opportunity identified: [cluster] — [n] ideas"

3. After generation:
   - Update `.claude/skills/generation-log/log/generations.jsonl`
   - Update `performance/cadence-log.yaml`
   - Log original archive file as `used_in: [new draft file path]`

---

## Output format

```
═══════════════════════════════════════════
EVERGREEN SCAN — [DATE]
Archive scope: [standard|full] | Candidates evaluated: [n]
Strong candidates: [n] | Needs work: [n]
═══════════════════════════════════════════

STRONG CANDIDATES (score ≥ 7)

  1. [SCORE: 9/10] "[Original title]"
     Original: [archive path]
     Best angle: "[specific repurpose angle]"
     Brand: [brand] | Format: [format] | Voice: [personal/company]
     Persona scores: Skeptic=[n] ICP=[n] Platform=[n] → [total]/9
     Why now: [what makes this relevant today]

[Campaign clusters detected — if applicable]
  ★ CLUSTER: [cluster name]
    Ideas: [title 1], [title 2], [title 3]
    Campaign opportunity: "[proposed series structure]"

NEEDS ANGLE WORK (score 5–6)
  - "[title]": [what needs refreshing]

═══ ERRORS LOGGED ══════════════════════════
  - [any issues]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generate from queue? yes | select | skip
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
