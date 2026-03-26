---
name: quality-assessor
description: The Assess phase of the Plan→Work→Assess→Compound loop. Runs every generated draft through synthetic personas and the QUALITY_GATE rubric before saving. Never skip this. Also use standalone when reviewing drafts or checking if a piece is ready to approve. Trigger: automatically after generation, "assess this draft", "score this", "is this ready", "quality check", or any time a draft needs a cold read before saving.
triggers:
  - automatically after generation
  - assess this draft
  - score this
  - is this ready
  - quality check
  - cold read
  - synthetic persona check
loop: runs inside the Assess phase of every generation
---

# Quality Assessor

The Assess step. Runs after generation, before saving. Every piece goes through this. No exceptions.

The goal is to catch what the generator can't see — because the generator still remembers its own intent. Fresh eyes (synthetic personas) catch the drift.

---

## When this runs

Automatically after any generation step in any skill.
Manually when: a draft needs a standalone review, a piece scored below 8, you want a cold read on something already in drafts/.

---

## Step 1: Load rubric context

1. `knowledge/INDEX.md` — confirm which client/brand this draft belongs to
2. `QUALITY_GATE.md` — 0–10 scoring rubric. Read the full rubric before scoring.
3. `anti-ai-rules.md` — banned patterns. Run the mental checklist first.
4. `brand/[client]/voice-personal.md` or `voice-company.md` — the voice standard to hold the draft against
5. `.claude/skills/adversarial-reviewer/gotchas/[client].md` — client-specific patterns to watch for

---

## Step 2: Anti-AI scanner (deterministic pass — runs first)

```bash
python .claude/skills/anti-ai-scanner/scripts/scan_draft.py [draft-file]
```

**If exit code 1 (violations found):**
→ List every violation
→ Rewrite the violating lines
→ Re-run scanner until exit code 0
→ Do NOT proceed to persona scoring until scanner passes

**If exit code 0:**
→ Continue to persona scoring

---

## Step 3: Synthetic Persona Assessment

Three personas read the draft cold. They do not know the intent. They only see what's on the page.

---

### Persona A: The Skeptical Reader (scroll test)

**Who they are:** A [job title from brand's primary persona] who follows [brand] on [platform]. They've seen too much AI content. They're scrolling fast. They are predisposed to skip anything that feels like it could have been written by anyone.

**Their only question:** "Why would I stop scrolling for this specific sentence?"

**Score 0–3:**
- 0 = Immediate scroll. Nothing specific, nothing owned, nothing worth reading.
- 1 = Maybe. Has a hook but it's generic. Someone else could have written this.
- 2 = Probably stops. Has something specific — a number, a named situation, a counterintuitive take.
- 3 = Definite stop. Only this person could have written this. Something real, specific, earned.

**What to look for:**
- Does the first sentence create forward momentum or explain the topic?
- Is there a specific detail that anchors it (number, name, date, decision, consequence)?
- Would you read past line 3?

---

### Persona B: The Ideal ICP (relevance test)

**Who they are:** The exact target persona from `brand/[client]/personas.yaml`. Their title, their frustration, their vocabulary, their current priorities.

**Their question:** "Does this solve or name something I'm actually dealing with?"

**Score 0–3:**
- 0 = Wrong audience. This speaks past them or down to them.
- 1 = Adjacent. Related to their world but not their actual problem.
- 2 = Relevant. Names a real pain point or provides a real angle they hadn't considered.
- 3 = Direct hit. Uses their vocabulary, addresses their exact situation, makes them feel understood.

**What to look for:**
- Are the words ones the persona would actually use?
- Does it address a decision they're actively facing?
- Would they share this with a colleague?

---

### Persona C: The Platform Algorithm (structural test)

**Who they are:** A structural model of what [platform] rewards based on engagement patterns.

**For LinkedIn:** Specificity, clear POV, first-comment worthy, no hashtag spam, no engagement bait
**For Twitter/X:** Compression, tension, opinion or observation that invites retweet
**For Newsletter:** Strong subject line energy, value in first paragraph, one idea fully developed
**For Blog:** Clear value prop in opening, scannable structure, SEO signal in headline

**Score 0–3:**
- 0 = Structurally broken. Wrong format, no hook, CTA is a pitch.
- 1 = Adequate. Has the right shape but nothing that makes the algorithm prefer it.
- 2 = Good structure. Follows platform best practices from `brand/[client]/channel-notes/[channel].md`.
- 3 = Excellent structure. Everything in the right place, opening line has pull, CTA invites without pitching.

---

## Step 4: Quality Gate score (0–10)

Apply the full rubric from `QUALITY_GATE.md`.

Score dimensions (load from QUALITY_GATE.md — do not improvise):
- Voice accuracy
- Specificity
- Hook strength
- Substance / insight
- Channel fit
- Anti-AI cleanliness

**Gate rules:**
- Score ≥ 8 → save to `drafts/[client]/[channel]/` with `status: draft`
- Score 7 → save with `quality_notes:` flagging what needs review before approval
- Score 5–6 → flag, do NOT save, ask whether to rewrite or skip
- Score < 5 → archive, do NOT save

**If adversarial reviewer estimate differs from generator self-score by > 1 point → use the lower score.**

---

## Step 5: Publish validator (pre-save check)

```bash
python .claude/skills/publish-validator/scripts/validate_frontmatter.py [draft-file]
```

Must pass exit code 0 before any file is written to drafts/.

---

## Step 6: Report

```
═══ QUALITY ASSESSMENT ═══════════════════════════════
Draft: [filename]
Brand: [brand] | Format: [format] | Voice: [personal/company]

ANTI-AI SCANNER: [PASS | violations found]

SYNTHETIC PERSONA SCORES:
  Persona A (Skeptical Reader): [0-3] — [one-sentence explanation]
  Persona B (Ideal ICP): [0-3] — [one-sentence explanation]
  Persona C (Platform): [0-3] — [one-sentence explanation]
  Total: [n]/9

QUALITY GATE: [n]/10
  Voice accuracy: [score note]
  Specificity: [score note]
  Hook strength: [score note]
  Substance: [score note]

DECISION: [SAVE | REWRITE | SKIP]
  Quality notes: [specific note for reviewer]
═══════════════════════════════════════════════════════
```

---

## When rewriting is needed

If the piece scores < 7 or Persona A scores 0–1:

1. Identify the single biggest failure:
   - No specificity → find a real detail (number, name, consequence, decision)
   - Wrong voice → reload voice-fingerprint layers and rewrite with stronger constraint
   - Bad hook → generate 3 alternative opening lines, pick the most specific

2. Rewrite only the failing section first. Re-run scanner. Re-score.

3. If second attempt scores < 7 → archive the draft with a note in `knowledge/ERRORS.md`:
   "Draft [slug] archived after 2 failed attempts — [specific failure reason]"
