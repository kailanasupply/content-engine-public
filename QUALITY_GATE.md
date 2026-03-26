# Quality Gate — Root
# 0–10 scoring rubric. Every generated piece is scored before saving.
# A piece must score ≥ 7 to be saved as status: draft.
# A piece scoring < 5 is archived, not saved.
# Score 5–6 triggers a human flag — don't auto-save, surface for decision.
#
# This file supersedes knowledge/QUALITY_GATE.md.
# Both exist — this is the scoring rubric, knowledge/ is the checklist detail.

---

## MANDATORY LOAD ORDER
Before running this gate on any piece, confirm you have loaded:
1. `anti-ai-rules.md`
2. `knowledge/QUALITY_GATE.md` (the checklist detail)
3. `knowledge/FREQUENCY_GUIDE.md`
4. `SUCCESS_METRICS.md` (to calibrate what "good" means for this channel)
5. The correct voice profile for this piece

---

## The 0–10 Rubric

Score each dimension 0–2. Total = quality score out of 10.

---

### Dimension 1: Voice accuracy (0–2)
*Does this sound like the specific person/brand it was written for?*

**2 — Strong match**
Read the piece cold. It sounds like them. Specific vocabulary, sentence rhythm, opinions stated with their level of confidence. A reader who knows this person would not think "AI wrote this."

**1 — Partial match**
Mostly sounds right but has 1–2 sentences or phrases that break the illusion. The structure is correct but one section drifted generic.

**0 — Voice failure**
The piece could have been written by anyone. No specific markers. Reads like a generic professional on LinkedIn, not like this specific human being.

**Automatic 0 triggers:**
- Any banned word from anti-ai-rules.md present
- Personal and company voice blended in the same piece
- Hook that could belong to any founder/brand ("In today's world...", "Have you ever...")

---

### Dimension 2: Specificity (0–2)
*Does the piece contain at least one detail that could only come from this person's actual experience?*

**2 — Highly specific**
Contains a real number, a named client or person (where appropriate), a specific date, a named tool, a specific dollar amount, or a concrete outcome. Not made up — drawn from the input.

**1 — Partially specific**
Has one concrete element but the rest is abstracted. The hook is specific but the body goes generic.

**0 — No specificity**
Everything could apply to any company in any industry. No numbers, no names, no moments, no proof.

**Test:** Replace "the company" with any competitor's name. If it still reads fine — it's a 0.

---

### Dimension 3: Single clear point of view (0–2)
*Does the piece argue one specific, arguable position?*

**2 — Clear POV**
The piece makes a claim someone could disagree with. It doesn't hedge to cover all bases. By the end, the reader knows exactly what the writer thinks about the topic.

**1 — Implied POV**
The piece has a direction but doesn't commit. It presents the idea without quite asserting it. "Many people find that..." instead of "I've found that..."

**0 — No POV**
The piece is informational without perspective. It describes what exists instead of arguing for what's true. Could be Wikipedia.

---

### Dimension 4: Hook quality (0–2)
*Would the target persona stop scrolling for this opening?*

**2 — Stops the scroll**
Opens with something that creates immediate tension, curiosity, or recognition. Specific. Counter-intuitive. A moment. A number. Something the persona has thought but hasn't seen said this clearly.

**1 — Decent hook**
Opens with something relevant but not compelling. Gets to the topic without making the reader need to know what comes next.

**0 — Failed hook**
Opens with context, setup, or a question the reader has seen a hundred times. "I've been thinking about..." / "As a founder, you know..." / "Content is changing."

---

### Dimension 5: Ending (0–2)
*Does the piece end or does it just stop?*

**2 — Lands**
The last sentence carries the weight of the whole piece. The reader feels it. No explanation. No summary. No pivot to CTA that undercuts the emotion. It ends at the right moment.

**1 — Decent close**
The ending is fine. It wraps up without being brilliant. Might have a soft CTA that makes sense.

**0 — Fails to land**
The piece explains its own lesson. Ends with a question to boost engagement. Has a generic CTA that could be on any post. Trails off. Summarizes what just happened.

---

## Scoring table

| Score | Status | Action |
|-------|--------|--------|
| 9–10 | ✅ EXCEPTIONAL | Save as `draft` — flag as priority for review |
| 7–8 | ✅ PASS | Save as `draft` |
| 5–6 | ⚠️ FLAG | Do not auto-save — surface for human decision with specific notes |
| 3–4 | 🔄 REWRITE | Identify lowest-scoring dimension(s), regenerate those sections, re-score |
| 0–2 | 🚫 ARCHIVE | Do not save — log in archive/rejected.md with reason |

---

## Scoring protocol

1. Generate the piece
2. Run the anti-AI scrub from `anti-ai-rules.md` (NEVER/ALWAYS checklist)
3. Score each dimension (write score as a comment in your working context)
4. Sum the scores
5. Apply the action from the table above
6. If rewriting: note which dimension(s) failed, fix only those, re-score

**Never round up.** Score what's there, not what you intended.

---

## Recording the score

Every saved draft includes the quality score in frontmatter:

```yaml
quality_score: 8
quality_notes: "Strong voice and POV. Hook is good. Ending is slightly explained — cut the last sentence before publishing."
```

This lets reviewers know what the engine already assessed and what to look at.

---

## Tie to SUCCESS_METRICS.md

Quality scores feed the performance learning loop:

- Pieces scoring 9–10 that also score `high` on performance → extract as new voice examples
- Pieces scoring 7–8 that score `low` on performance → likely a cadence/topic issue, not voice
- Pieces scoring 5–6 that pass human review → flag the rubric miss for calibration
- Systematic low scores on one dimension → trigger `/calibrate-voice`
