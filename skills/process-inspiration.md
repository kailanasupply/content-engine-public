---
name: process-inspiration
description: Process everything in inputs/inspiration/ — liked posts, raw ideas, screenshots, notes. Extract the content angle, route to the right brand and format, and queue proposals for the next scan. Trigger: /process-inspiration, "process my ideas", "what can I make from my notes", "I dropped some inspiration", new files in inputs/inspiration/.
triggers:
  - /process-inspiration
  - process my ideas
  - I dropped some inspiration
  - what can I make from my notes
  - process inspiration
loop: Plan → Work → Assess → Compound
---

# Process Inspiration

Reads `inputs/inspiration/` and turns raw captured ideas into specific content proposals. The intelligence layer between "I saw something interesting" and "here's what to actually make."

---

## LOOP: Plan → Work → Assess → Compound

---

## Phase 1: PLAN

Load in order:
1. `knowledge/INDEX.md` — what files exist and what they contain
2. `knowledge/ERRORS.md` — check for any open routing errors from previous runs
3. `anti-ai-rules.md` — applies to proposal language, not just generated content
4. `config/settings.yaml` — all brands and their channel restrictions
5. For each active brand: `brand/[brand]/pillars.md` + `brand/[brand]/personas.yaml`
6. `performance/insights.md` — what's been working (informs angle prioritization)
7. `performance/cadence-log.yaml` — what's been generated recently (avoids duplicate angles)

---

## Phase 2: WORK

### Step 2a: Identify unprocessed files

Scan `inputs/inspiration/` for ALL files NOT in the `processed/` subfolder.
Include: `.md`, `.txt`, `.yaml`, `.json`, `.png`, `.jpg`
Exclude: `README.md` and any file with `_PROCESSED_` in the name.

For each file, extract:
1. **Type:** liked-post | quick-idea | client-question | competitor-content | news-data | screenshot | other
2. **Core content:** The raw idea. What is actually here?
3. **Signal extracted:** If liked post → what made it worth noting? (angle? structure? hook? topic?)
4. **Applicable brands:** Which brands could use this? Apply routing logic:
   - Personal story/experience → `brian` (personal voice)
   - Fraud/security industry → `house-of-fraud` or `safeguard`
   - SaySo ICP/category → `sayso` (X + Company LinkedIn ONLY)
   - Ambiguous → `brian` default

### Step 2b: Generate specific content angles

For each inspiration item × brand pairing, produce:
- **A specific angle** — not "write a post about X" but the exact take
  Bad: "A post about AI in fraud detection"
  Good: "The moment fraud teams realize their AI model is flagging the same patterns their rules already caught"
- **A hook draft** — one sentence, the actual opening line
- **The content reason:** insight | opinion | story | announcement | education | proof
- **The best format** for this brand (respecting channel restrictions)

**SaySo hard gate:** If routing to SaySo, ONLY propose twitter or company-linkedin.
Any other format → do not propose. Log the redirect.

### Step 2c: Check for saturation

Before queuing each proposal:
```bash
python .claude/skills/generation-log/scripts/query_log.py --client [brand] --search "[topic keyword]" --days 30
```
If same angle appears in recent content → flag as potential duplicate. Don't auto-drop, but note it.

### Step 2d: Apply evergreen tagging

For each processed inspiration item, evaluate against evergreen criteria:
- Core insight timeless (not tied to news cycle)?
- Falls in core themes: fraud/security, building-in-public, leadership, trust, dad-life?
- Would land in 6–12 months with minimal edits?
- Strong narrative hook?

If 3+ criteria met → flag as evergreen candidate (will be copied to `archive/evergreen-candidates/` on archive)

---

## Phase 3: ASSESS (Synthetic Persona Review)

Run each proposed piece through the 3 personas before presenting to user:

**Persona A — Skeptical Reader (scroll test)**
"Does this stop my thumb? Would I actually read this or click past?"
Score 0–3

**Persona B — Ideal ICP (relevance test)**
"Does this speak the exact language of the target persona? Does it name their pain?"
Score 0–3

**Persona C — Platform Fit (structural test)**
"Does this have what the platform rewards? (LinkedIn: specificity + POV; Twitter: tension + compression)"
Score 0–3

Minimum qualifying score: 6/9 to enter the queue.

Items scoring 4–5/9 → flag as "needs angle work" with specific note on what failed.
Items scoring < 4/9 → archive the idea but don't queue.

---

## Phase 4: COMPOUND

1. Move processed files:
   - `inputs/inspiration/[file]` → `inputs/inspiration/processed/[file]_PROCESSED_[date].[ext]`
   - Do NOT move `README.md`

2. Evergreen tagging:
   - Items flagged as evergreen → copy to `archive/evergreen-candidates/[date]-[slug]-[EVERGREEN].md`

3. Update `knowledge/ERRORS.md` if any routing issues found:
   - "SaySo channel block applied to [format]"
   - "Ambiguous brand routing for [file] — defaulted to brian"
   - "Duplicate angle detected: [file] similar to [recent post title]"

4. Write approved proposals to `inputs/processed/inspiration-queue-[date].yaml` for morning scan pickup.

---

## Output format

```
═══════════════════════════════════════════
INSPIRATION PROCESSED — [DATE]
Items found: [n] | Queued: [n] | Skipped: [n]
═══════════════════════════════════════════

BRIAN — [n] proposals

  1. [Format] | personal | Score: [A/B/C] = [n]/9
     Source: [filename]
     Angle: "[exact angle]"
     Hook: "[draft opening line]"
     Content reason: [insight/opinion/story/etc.]
     [EVERGREEN] if flagged

HOUSE OF FRAUD — [n] proposals
  [Same format]

SAYSO (X + Company LinkedIn only) — [n] proposals
  [Same format — never newsletter/blog/personal]

═══ NEEDS ANGLE WORK ════════
  - [file] → [brand]: scored [n]/9
    Persona B said: [what failed]

═══ ARCHIVED (not queued) ════
  - [file]: [reason]

═══ ERRORS LOGGED ══════════
  - [any routing issues]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Add these to tomorrow's morning scan queue?
yes | select | no
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
