---
name: brand-voice-enforcer
description: The voice gate. Loads the full layered voice context for the active client before any draft is written, and checks every draft against it before saving. Also use for voice calibration, rewriting off-brand content, or checking if a draft sounds right. Trigger: before any generation, "does this sound like me", "rewrite in my voice", "enforce voice", "voice check", "this doesn't sound right", or as part of the Assess phase.
triggers:
  - before any generation
  - does this sound like me
  - rewrite in my voice
  - enforce voice
  - voice check
  - this doesn't sound right
  - voice calibration
loop: runs during Work (pre-generation) and Assess (post-generation)
---

# Brand Voice Enforcer

Two jobs: load voice context before writing, and enforce it after. Every piece goes through both.

---

## Job 1: Pre-generation voice loading

Before drafting any piece, load the full layered voice context for the active client.

### Voice loading order (do not skip layers)

1. **`anti-ai-rules.md`** — the floor. Banned patterns apply regardless of client.

2. **Voice fingerprint — core voice**
   `brand/[client]/voice-personal.md` OR `brand/[client]/voice-company.md`
   (based on voice_profile of the piece being generated)

3. **Voice fingerprint — sentence rhythm**
   `.claude/skills/voice-fingerprint/[client]/sentence-rhythm.md`
   Read: how long are sentences? Where do fragments live? What's the natural pause structure?

4. **Voice fingerprint — vocabulary**
   `.claude/skills/voice-fingerprint/[client]/vocabulary.md`
   Read: which words are signature? Which are banned? What's the vocabulary temperature?

5. **Voice fingerprint — opinion patterns**
   `.claude/skills/voice-fingerprint/[client]/opinion-patterns.md`
   Read: how does this person or brand take a position? Direct? Qualified? With evidence? With story?

6. **Voice fingerprint — gotchas (highest recency weight)**
   `.claude/skills/voice-fingerprint/[client]/gotchas.md`
   Read last. These are the patterns that KEEP appearing in drafts despite other constraints. Read them most carefully.

7. **Channel notes**
   `brand/[client]/channel-notes/[channel].md`
   Read: platform-specific behavioral rules for this piece.

8. **Examples (few-shot loading)**
   `brand/[client]/examples/[personal|company]/`
   List what's available. Load 1–2 most relevant examples as reference.
   Do NOT copy structure. Use as a voice calibration reference only.

9. **Performance insights (structural guidance)**
   `performance/insights.md` — what structural choices are working right now

**After loading, state the active voice constraints:**
"Writing as: [brand] | [personal/company] | [channel]
Voice temperature: [adjective from voice file]
Banned patterns loaded: [n from anti-ai-rules + vocabulary gotchas]
Example reference: [filename]"

---

## Job 2: Post-generation voice enforcement

After a draft is written, before the adversarial-reviewer runs, run a structured voice check.

### Voice check protocol

**Step 1: Identity check**
Read the first paragraph. Cover the author's name. Could this have been written by a different person/brand?
- If yes → flag: "First paragraph does not establish distinct voice. Needs a specific owned detail."
- If no → pass

**Step 2: Vocabulary scan**
Scan for:
- Any banned words from `anti-ai-rules.md` banned list
- Any "temperature mismatch" words (too formal for a casual voice, too casual for a professional brand)
- Any vocabulary from `voice-fingerprint/vocabulary.md` that should appear but doesn't

Flag each. Do not auto-fix — list the issues for the rewrite pass.

**Step 3: Rhythm check**
Compare sentence structure to `sentence-rhythm.md`:
- Are the sentence lengths right? (fragments where expected, complex where expected)
- Are there any run-ons that the voice profile would never write?
- Does the cadence feel like this person's natural speech?

**Step 4: Gotchas scan**
Load `.claude/skills/voice-fingerprint/[client]/gotchas.md`.
Check every entry. These are the patterns that keep slipping through.
Flag any that appear in the draft.

**Step 5: Opinion structure check**
Check `opinion-patterns.md`.
Does the piece take a position in the way this brand/person takes positions?
- Over-hedged? (voice profile says "direct and confident" but draft says "it might be worth considering")
- Under-justified? (voice profile says "always grounds opinion in specific evidence" but draft is assertion-only)

---

## Voice enforcement report

After both jobs complete:

```
═══ VOICE ENFORCEMENT ════════════════════════════════
Client: [brand] | Voice: [personal/company] | Channel: [channel]

PRE-GENERATION: Voice context loaded ✓
  Core voice: [file loaded]
  Sentence rhythm: [file loaded]
  Vocabulary: [file loaded]
  Opinion patterns: [file loaded]
  Gotchas: [n patterns loaded]
  Examples: [filename]

POST-GENERATION: Voice check
  Identity check: [PASS | issue]
  Vocabulary scan: [PASS | n issues]
  Rhythm check: [PASS | issue]
  Gotchas scan: [PASS | n patterns detected]
  Opinion structure: [PASS | issue]

OVERALL: [PASS | REWRITE NEEDED]
Issues to fix before Assess phase:
  1. [specific issue]
  2. [specific issue]
════════════════════════════════════════════════════════
```

---

## Voice calibration mode

When called for calibration (`/calibrate-voice` or "this doesn't sound right"):

1. Load the current voice profile
2. Read the flagged piece
3. Identify the specific mismatch — is it:
   - Vocabulary temperature (too formal/casual)
   - Rhythm (wrong sentence structure)
   - Specificity level (too vague vs. too detailed)
   - Opinion structure (over-hedged, wrong justification style)
   - Gotcha pattern (something from gotchas.md that slipped through)

4. Propose a specific fix to the voice profile:
   ```
   PROPOSED ADDITION to .claude/skills/voice-fingerprint/[client]/gotchas.md:
   New gotcha: "[specific pattern to avoid]"
   Evidence: "[the line from the draft that triggered this]"
   ```

5. Wait for approval before updating the file.

---

## Quick reference: voice profiles by brand

**brian (personal)**
Primary: first-person, specific, earned authority, opinionated, no corporate language

**brian (company)** — for any company-voice brian content
Polished but direct, outcome-focused, professional without being stiff

**house-of-fraud**
Company voice: authoritative, practitioner-to-practitioner, no vendor speak, questions over declarations when possible

**safeguard**
Company voice: professional, evidence-focused, practitioner insurance lens, calm confidence

**sayso**
Company voice ONLY: [load from brand/sayso/voice-company.md for full profile]
No personal voice. No founder perspective in brand channels.
