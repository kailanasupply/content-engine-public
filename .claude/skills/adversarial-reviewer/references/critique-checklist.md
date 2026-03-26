# Critique Checklist

Reference this during the line-level critique pass. Every category below represents a failure mode that routinely slips through self-review. Work through each category systematically.

---

## Category 1: Banned words

Scan the full text for every word on this list. One hit is a flag. Flag it, don't skip it.

`delve` · `pivotal` · `underscore` · `tapestry` · `testament` · `intricate` · `meticulous` · `vibrant` · `garner` · `bolstered` · `fostering` · `enhance` · `showcase` · `highlight` (as verb) · `crucial` · `align with` · `enduring` · `valuable` · `key` (as adjective for "important") · `groundbreaking` · `renowned` · `nestled` · `diverse array` · `rich` (figurative) · `profound` · `commitment to` · `boasts` · `stands as` · `serves as` · `marks as` · `represents` (when it means "is") · `navigate` (figurative) · `landscape` (abstract) · `ecosystem` (non-literal) · `journey` (metaphorical) · `robust`

**Em dashes (—) are also banned.** Flag every one.

---

## Category 2: Sentence pattern violations

### The Tacked-On -ing Clause
A sentence that ends with a present participle phrase adding fake significance.

Look for: sentences that end in "...`-ing` [something]" where the -ing clause doesn't add new information — it just annotates the main clause with implied significance.

❌ "The team launched the feature, demonstrating their commitment to..."
❌ "She built the program from scratch, positioning the company as..."

Test: remove the -ing clause. Does the sentence still make the main point? If yes — cut the clause.

---

### False Significance
Any sentence that asserts importance rather than proving it.

Look for: "is a testament to" / "underscores the importance of" / "reflects broader trends in" / "marks a significant shift" / "highlights the need for"

These assert that something matters. Good writing proves it matters with a specific fact.

---

### "Not Only X But Also Y"
In any form. The pattern sounds like it's making a nuanced point. It isn't.

❌ "It's not just a tool — it's a philosophy."
❌ "Not only does this save time, but it also changes how teams think."
❌ "It's not about the feature. It's about the trust."

---

### The Despite/Challenges Arc
A paragraph structured as: [success] → "Despite..." → [challenges] → [optimistic pivot]

This is a template, not a thought. Flag any paragraph with this arc.

---

### The Rule of Three (as padding)
Three-item lists used to appear comprehensive rather than because three genuinely specific things exist.

Test: Can you name a fourth? Can you remove one and the piece is stronger? If yes to either — the list is padding.

---

### Vague Attribution
"Experts say" / "industry reports suggest" / "observers have noted" / "research shows" — without naming the specific expert, report, or study.

These borrow credibility without providing any. Every attribution must name its source or be replaced with "I think" / "In my experience."

---

### Elegant Variation (Synonym Rotation)
The piece refers to the same thing using different words to avoid repetition — "the company," "the firm," "the organization," "the enterprise" — all in the same piece.

Humans repeat words when precision matters. LLMs rotate synonyms because of repetition penalty. Flag synonym rotation.

---

### Copulative Avoidance
"Serves as" instead of "is." "Stands as" instead of "is." "Represents" instead of "is." "Acts as" instead of "is."

Flag every one. Replace with "is."

---

## Category 3: Voice drift

These are the patterns that are hardest to catch because they don't violate any single rule — they just accumulate until the piece no longer sounds like the person.

### Generic LinkedIn founder voice
The piece could have been written by any thoughtful operator in any industry. Nothing in it is specific to this person's actual experience, opinions, or industry knowledge.

Test: replace the author with any other founder/operator in this space. If the piece works — it's generic.

Signs of generic founder voice:
- "I've learned that..." followed by a universal lesson
- The hook is a relatable frustration, not a specific moment
- The body is principles, not specifics
- The ending is an inspirational summary

### The explained ending
The piece makes its point, and then explains the point. The last sentence should be the compressed version of the whole idea. Instead it's a paraphrase of what just happened, a lesson statement, or a pivot to "What do you think?"

Look for: final sentences that start with "The lesson here..." / "What this taught me..." / "The takeaway is..." / "I'd love to hear..." / "Drop a comment..."

### Overdone staccato
Short sentences used as rhythm device, but so frequently that the rhythm becomes mechanical rather than deliberate. Brian uses short sentences strategically. When every sentence is three words, it's no longer stylistic — it becomes a tic.

Flag: blocks of more than 4 consecutive single-clause sentences unless there's a clear structural reason.

### The generic hook
Opens with context or scene-setting rather than the thing itself.

❌ "I've been thinking a lot about fraud leadership lately."
❌ "Here's something I see constantly in this space."
❌ "If you work in fraud, you know the pressure."

These open a door without walking through it. The hook should be the thing itself — the specific claim, the specific moment, the specific counter-intuitive fact.

---

## Category 4: Structural problems

### One piece, two ideas
The piece has two distinct points and tries to land both. By the end, neither has landed cleanly.

Test: what is the one sentence the whole piece is arguing? If you can't write it — the piece has two ideas.

### Body goes generic after a strong hook
The hook is specific. The body retreats into abstraction. The ending is generic wisdom.

This is extremely common. The generator uses the specific hook (drawn from input) and then fills the body with its own knowledge instead of the input's specifics.

### Voice blend
A "personal" (I-voice) piece with we/our language, or a "company" (we-voice) piece with I-voice. Even a single sentence can trigger this flag.

---

## Category 5: Specificity gaps

**Important:** "Insider audience" or "voice profile match" does not excuse specificity gaps. A piece can sound like the right person while still lacking the concrete details that prove it. Voice accuracy and specificity are scored separately. Flag both independently.

### The abstract claim with no proof
A claim is made about results, outcomes, or behavior — without a number, a name, a date, or a specific example.

❌ "This approach consistently reduces false positive rates."
✅ "This approach dropped our false positive rate 22% in six weeks."

This is a mandatory flag if the piece has NO concrete elements anywhere — no numbers, no named clients, no specific tools, no dates, no dollar amounts. "Insider language" (using correct fraud terminology) is not the same as specificity. An AI can generate insider language. Only a human with lived experience can cite the specific client, the specific result, the specific tool.

### The "real" experience that could be invented
A story or anecdote that's plausible but not anchored by any specific detail — no name, no date, no dollar amount, no company, no tool, nothing that couldn't have been invented.

Test: is there any detail in this story that only the author could know? If no — the story is generic. File the flag. Do not excuse it.

**The insider audience escape hatch is not valid.** Fraud professionals in the audience also know the difference between "I've seen teams do this" (could be invented) and "Three companies I worked with in 2024 had this exact gap." Experienced insiders are more skeptical of unanchored claims, not less.

---

## Final check: the NEVER/ALWAYS card

After running all categories, do a final pass against the NEVER/ALWAYS quick-reference card from `anti-ai-rules.md`. This is the last catch before writing the report.
