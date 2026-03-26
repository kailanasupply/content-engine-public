---
name: morning-content-scan
description: The daily autonomous content intelligence engine. Scans all active brands for new inputs, applies cadence rules, loads performance context, and produces an approved generation queue. Follows the Plan → Work → Assess → Compound loop. Trigger: every morning, /morning-scan, "what should I make today", "daily scan", "run the scan". Never generates without human approval.
triggers:
  - /morning-scan
  - morning scan
  - what should I make today
  - daily scan
  - run the scan
  - what's in my queue
loop: Plan → Work → Assess → Compound
---

# Morning Content Scan

The daily intelligence run. Every session starts here. This skill is the engine's brain — it reads context, checks cadence, routes inputs, and tells you exactly what to make and why. It never generates anything. That's your call.

---

## LOOP: Plan → Work → Assess → Compound

Every run of this skill follows four phases:

### PLAN (what context do we need?)
### WORK (process inputs + build queue)
### ASSESS (synthetic persona check)
### COMPOUND (log + update learning files)

---

## Phase 1: PLAN

**Read these files in order — do not skip any:**

1. `knowledge/INDEX.md` — **Read first, always.** This file tells you what exists and where to find it.
2. `knowledge/ERRORS.md` — What went wrong in previous runs. Check for open issues before proceeding.
3. `anti-ai-rules.md` — Banned patterns and writing rules. Even planning language should avoid these.
4. `QUALITY_GATE.md` — The 0–10 scoring rubric. Use this when evaluating whether proposed pieces are worth the queue.
5. `knowledge/FREQUENCY_GUIDE.md` — Cadence philosophy. Informs what "enough" looks like.
6. `config/settings.yaml` — All registered brands, their active channels, and blocked channels.
7. `config/cadence.yaml` — Machine-readable frequency rules per brand and format.
8. `performance/cadence-log.yaml` — When each format was last generated per brand.
9. `performance/insights.md` — Synthesized performance patterns.

**After loading, state:**
- Active brands found: [list]
- Open errors from ERRORS.md: [list or "none"]
- Last generation per brand: [summary from cadence-log]

---

## Phase 2: WORK

### Step 2a: Scan inputs

Check for new files (created or modified in last 24 hours) in:
- `inputs/recordings/`
- `inputs/notes/`
- `inputs/briefs/`
- `inputs/processed/` (unprocessed transcripts)
- `inputs/inspiration/` (not in `/processed/` subfolder)

For each file:
- Determine type (recording / notes / brief / inspiration)
- Determine brand (from frontmatter, filename prefix, or content)
- Assign richness: high (recording or 500+ words) | medium (200–500) | low (<200 or inspiration)
- If brand ambiguous → assign to `brian`, flag for clarification

**If NO new inputs at all:**
→ Run `python .claude/skills/evergreen-miner/scripts/mine_evergreen.py --top 3` to surface evergreen candidates
→ If candidates found (score ≥ 7) → include in queue as "Evergreen queue" section
→ If nothing → output: "No new inputs and no strong evergreen candidates. Nothing to generate today." → STOP

### Step 2b: Route inputs to brands

Apply routing rules:
- Personal story / experience → `brian` (personal voice)
- Fraud/security industry → `house-of-fraud` or `safeguard`
- SaySo category/ICP → `sayso` (X/LinkedIn ONLY — enforce hard stop)
- Ambiguous → `brian` by default

**SaySo hard gate:** Before adding ANY SaySo proposal, confirm format ∈ {twitter, company-linkedin}. If not, log to ERRORS.md as "Skipped [format] for SaySo — channel blocked" and redirect or drop.

### Step 2c: Check cadence gates per brand

For each brand with inputs:
1. Load `brand/[brand]/channel-notes/CHANNEL_RESTRICTIONS.md` if it exists
2. Cross-reference `config/cadence.yaml` min_gap_days
3. Check `performance/cadence-log.yaml` for last generation date
4. Apply max_per_week limits
5. Block any oversaturated topics (check generation-log: `python .claude/skills/generation-log/scripts/query_log.py --client [brand] --days 7 --summary`)

### Step 2d: Build generation manifest

For each eligible piece, create a manifest entry:

```
Brand: [name]
Format: [format]
Voice: [personal|company]
Source: [input file]
Angle: [specific angle — not "a post about X" but the actual take]
Hook draft: [one sentence attempt at the opening line]
Pillar: [pillar tag]
Persona: [target persona]
Content reason: [insight|opinion|story|announcement|education|proof]
Cadence check: [✓ last generated X days ago — eligible]
Performance note: [what insights.md says about this format/angle]
```

---

## Phase 3: ASSESS (Synthetic Persona Review)

**Before presenting the queue to the user, run each proposed piece through 3 synthetic personas:**

### Persona A: The Skeptical Reader
Role: A fraud professional who follows [brand] but has seen too much AI slop. They're about to scroll past.
Ask: "Does this stop my thumb? Why would I actually read this?"
Score: 0–3 (0=immediate scroll | 1=maybe | 2=probably | 3=definitely stops)

### Persona B: The Ideal ICP
Role: The exact person in the target persona — their title, their pain, their vocabulary.
Ask: "Does this speak my language? Does it solve something I care about?"
Score: 0–3

### Persona C: The Platform Algorithm (channel-specific)
Role: LinkedIn/Twitter engagement signals.
Ask: "Does this have the structural elements that signal quality to the platform? (hooks, specificity, engagement bait potential)"
Score: 0–3 (but never let "engagement bait" override voice rules)

**Minimum qualifying score: 6/9**

Pieces scoring < 6/9 → move to "Needs stronger angle" section, NOT to generation queue.
Include the persona scores in the scan report so you can see the reasoning.

---

## Phase 4: COMPOUND

**After the scan is complete (whether generation runs or not):**

1. **Update `knowledge/ERRORS.md`** if any issues were found:
   - Blocked channel attempts
   - Missing brand context files
   - Low-scoring proposals (< 6/9 persona score)
   - Cadence violations flagged

2. **If generation runs (user approves):** After content is saved:
   - Update `performance/cadence-log.yaml` with today's entries
   - Append to `.claude/skills/generation-log/log/generations.jsonl` via `--append` flag

3. **Weekly trigger:** If today is Monday OR it has been 7+ days since last synthesis run:
   - Remind: "You haven't synthesized learnings in 7 days. Run /synthesize-learnings when ready."

---

## Output format

```
═══════════════════════════════════════════════════
MORNING SCAN — [DATE]
Brands: brian | safeguard | house-of-fraud | sayso
New inputs: [n] | Proposed: [n] | Deferred: [n]
═══════════════════════════════════════════════════

[NEW INPUTS TABLE]

═══ GENERATION QUEUE ═══════════════════════════════

BRIAN ([n] pieces)
  1. [Format] | [Voice] | Score: [A/B/C] = [total]/9
     Source: [file] | Pillar: [pillar]
     Angle: "[angle]"
     Hook: "[hook draft]"
     Performance note: [from insights.md]

SAYSO ⚠ X + COMPANY LINKEDIN ONLY ([n] pieces)
  [Same format — only Twitter and company-linkedin appear here]

[OTHER BRANDS...]

═══ NEEDS STRONGER ANGLE ════════════════════════════
  - [Brand] [Format]: scored [n]/9 — [what persona flagged]

═══ DEFERRED (cadence) ══════════════════════════════
  - [Brand] [Format]: [reason]

═══ ERRORS LOGGED ═══════════════════════════════════
  - [any issues found]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply: go | go [brand] | edit | skip
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## After user approves

Route to: `.claude/commands/generate-campaign.md` with the manifest entries.
Each piece runs: anti-ai-scanner → adversarial-reviewer → quality score → save to drafts/
Then compound: update cadence-log + generation-log.
