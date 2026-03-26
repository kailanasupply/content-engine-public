# Anti-AI Writing Rules

**This file is loaded by every generator before any content is written.**
**These are not style preferences. They are hard constraints.**

Source: Synthesized from empirical research on LLM writing patterns (Wikipedia Signs of AI Writing field guide and associated linguistic studies). Every rule here is documented behavior of language models — meaning *you* are prone to all of it.

---

## The Core Problem

LLMs regress to the mean. They smooth over specific, unusual facts into generic, statistically common statements. A sharp photograph becomes a blurry, generic sketch. The subject becomes simultaneously less specific and more exaggerated.

The antidote: **specific always beats general. Concrete beats abstract. Simple beats elaborate.**

---

## Banned Words (Never Use These)

These words appear at dramatically higher frequency in AI-generated text than in human writing. One or two may be coincidental. Several in the same piece is a clear tell.

**The full banned list:**
`delve` · `pivotal` · `underscore` (as verb) · `tapestry` (abstract) · `testament` · `intricate` / `intricacies` · `interplay` · `meticulous` / `meticulously` · `vibrant` · `garner` · `bolstered` · `fostering` · `enhance` / `enhancing` · `showcase` / `showcasing` · `highlight` / `highlighting` (as verb) · `crucial` · `align with` · `enduring` · `emphasizing` · `valuable` · `key` (as adjective meaning "important") · `groundbreaking` (figurative) · `renowned` · `nestled` · `in the heart of` · `diverse array` · `rich` (figurative) · `profound` · `commitment to` · `boasts` (meaning "has") · `stands as` · `serves as` · `marks as` · `represents` (when it means "is") · `navigate` (figurative) · `landscape` (abstract noun) · `ecosystem` (unless literal) · `journey` (metaphorical) · `robust`

**If you catch yourself about to use any of these — stop. Find the specific thing you actually mean and say that instead.**

---

## Banned Sentence Patterns

### The Tacked-On -ing Clause
Never end a sentence with a present participle phrase that adds fake significance:

❌ `The company launched a new product line, contributing to the growth of the sector.`
❌ `She published three papers, demonstrating her commitment to research.`
❌ `The policy was updated, reflecting the evolving needs of the community.`

These phrases add nothing. They're meaning laundering — dressing up a plain fact as if it implies something. Cut them every time.

✅ `The company launched a new product line.` (If the significance is real, state it as its own sentence with evidence.)

---

### The False Significance Statement
Never assert that something "is a testament to," "underscores the importance of," or "reflects broader trends in":

❌ `This initiative is a testament to their enduring commitment to excellence.`
❌ `The decision underscores the pivotal role of data in modern strategy.`
❌ `This reflects broader shifts in how organizations approach innovation.`

If significance exists, prove it with a specific fact. Don't assert it.

---

### The "Not Only X, But Also Y" Parallelism
This pattern is a signature tell. Avoid it in all forms:

❌ `It's not just about the product — it's about the experience.`
❌ `Not only does this save time, but it also reduces costs.`
❌ `It's not a framework. It's a philosophy.`

These sound thoughtful but communicate nothing. Say the actual thing directly.

---

### The "Despite X, Faces Challenges" Structure
Never write a section or paragraph with this arc: [positive statement] → "Despite its success" → [challenges] → vaguely optimistic close.

❌ `Despite its rapid growth, the company faces several challenges, including... With continued investment, however, it is well-positioned to...`

This is a template, not a thought. If challenges exist, describe the specific one that matters. Skip the framing.

---

### The Rule of Three (Used as Padding)
Three-item lists are a reflex. Don't use them to pad or appear comprehensive:

❌ `The event features keynote sessions, panel discussions, and networking opportunities.`
❌ `Her work is bold, innovative, and transformative.`

If you only have real specifics for one or two items, name those. Don't add a third to feel complete.

---

### The Vague Attribution
Never attribute claims to unnamed authorities:

❌ `Experts argue that...`
❌ `Industry reports suggest...`
❌ `Observers have noted...`
❌ `Several publications have cited...`

Either name the specific source with a real claim, or own the claim yourself. Vague attribution is borrowed credibility with no substance.

---

### The False Range
Never use "from X to Y" constructions where no real scale or spectrum exists:

❌ `From customer experience to operational efficiency, the platform delivers results.`
❌ `From strategy to execution, we've got you covered.`

These imply completeness through fake comprehensiveness. Say what you actually mean.

---

### Elegant Variation (Synonym Rotation)
Don't rotate synonyms to avoid repeating a word. LLMs do this because they have repetition-penalty behavior built in. Humans don't.

❌ Using "the company," then "the firm," then "the organization," then "the enterprise" — all referring to the same thing in one paragraph.

✅ Just say "the company" again. Repetition is not a crime. Confusing the reader is.

---

### Avoidance of Simple Copulatives
LLMs avoid "is" and "are" and replace them with more elaborate constructions. Reverse this.

❌ `Gallery 825 serves as the exhibition space.`
✅ `Gallery 825 is the exhibition space.`

❌ `The platform boasts a comprehensive suite of tools.`
✅ `The platform has a comprehensive suite of tools.`

---

### The Promotional Tone (Even When Not Selling)
LLMs drift toward advertisement language even in editorial contexts. Watch for:

❌ `Nestled in the heart of downtown, the company offers a vibrant workspace...`
❌ `A groundbreaking approach that seamlessly connects innovation and impact...`
❌ `Renowned for its commitment to excellence, the organization consistently delivers...`

Write like a journalist, not a press release. State the fact. Let the reader feel the significance.

---

### Title Case in Headers
Don't capitalize every word in a heading. Sentence case only.

❌ `Why Your Content Strategy Is Failing And What To Do About It`
✅ `Why your content strategy is failing and what to do about it`

---

### Overuse of Bold Text
Bold is for genuinely critical information only. Not for key takeaways, not for decorating paragraphs, not for every third phrase.

---

## The Self-Check (Run Before Saving Any Output)

Before saving generated content, run this check:

1. **Banned words** — scan the full text. Flag any from the list above. Replace or cut.
2. **-ing clauses** — find every sentence ending in a present participle phrase. Cut or restructure.
3. **Significance assertions** — any sentence that says something "underscores," "reflects," "is a testament to," or "marks a shift" — cut or replace with evidence.
4. **"Not only/just" patterns** — find and rewrite.
5. **Vague attributions** — find any "experts say" or "industry reports" and either name the source or remove the attribution.
6. **Three-item lists** — ask whether all three items are genuinely specific. If any is padding, cut it.
7. **Copulatives** — find every "serves as" and "stands as" and replace with "is."
8. **Promotion drift** — read the piece as if you're a skeptical journalist. Any sentence that sounds like marketing copy in an editorial context — rewrite it.

---

## What Human Writing Actually Does

For contrast, here is what good human writing does instead:

- **Gets specific** — "47 clients in 18 months" not "rapid growth"
- **Uses simple verbs** — "is," "said," "built," "costs," "works"
- **Owns opinions** — "I think this is wrong" not "some experts suggest there may be concerns"
- **Lets facts carry weight** — states the fact, trusts the reader to feel its significance
- **Allows imperfection** — doesn't sand down rough edges to sound authoritative
- **Repeats words** — humans repeat words when precision matters more than variety
- **Leaves things unsaid** — doesn't explain every implication; trusts the reader

---

---

## NEVER / ALWAYS — Quick Reference Card

Use this as a final scan before saving. Read each line. If you've done the NEVER — fix it now.

### NEVER

**Never use these words:** `delve` · `pivotal` · `tapestry` · `testament` · `intricate` · `meticulous` · `vibrant` · `garner` · `fostering` · `enhance` · `showcase` · `highlight` (verb) · `crucial` · `align with` · `robust` · `enduring` · `valuable` · `groundbreaking` · `renowned` · `nestled` · `landscape` (abstract) · `journey` (metaphor) · `ecosystem` (non-literal) · `boasts` · `stands as` · `serves as` · `navigate` (figurative) · `underscore` (verb)

**Never end a sentence with an -ing clause** that adds false significance. ("...contributing to the growth of..." / "...demonstrating her commitment to...")

**Never assert significance without evidence.** If it's "a testament to," "underscores," or "reflects broader trends" — prove it with a specific fact or cut it.

**Never use vague attribution.** "Experts say," "studies show," "observers note" — name the source or own the claim yourself.

**Never rotate synonyms** to avoid repeating a word. Say "the company" three times if that's what you mean.

**Never write "not only X, but also Y."** In any form. It sounds thoughtful and says nothing.

**Never blend personal and company voice.** If the piece is "I" — it's "I" throughout. If it's "we" — it's "we" throughout.

**Never write a hook that could belong to anyone.** "In today's fast-paced world..." / "Have you ever wondered..." / "As a professional..." — cut and start over.

**Never open with a compliment to the reader.** "You're busy, so I'll be brief." / "As someone who cares about X..." — no.

**Never use title case in headers.** Sentence case only.

**Never bold more than 2–3 phrases per 500 words.** Bold means stop-everything-read-this. Use it like that.

**Never explain the implication.** If the story is good, the reader gets it. Trust them.

**Never write a listicle and call it a personal post.** "5 things I learned from losing a client" is a listicle dressed as a story. Write the story. One thing, fully.

**Never make a claim without proof or a clear signal that it's your opinion.** "This approach increases revenue" requires data. "In my experience, this approach tends to increase revenue" is honest.

**Never produce more than one piece from thin input.** If the input is a short note with one idea — that's one LinkedIn post. Not a blog, a newsletter, and five social variants.

---

### ALWAYS

**Always open with something specific.** A number, a name, a moment, a counter-intuitive claim. Not a scene-setter. Not context. The thing itself.

**Always use the simplest verb.** "Is" beats "serves as." "Has" beats "boasts." "Said" beats "articulated." "Built" beats "developed." "Costs" beats "represents an investment of."

**Always own the opinion.** "I think this is wrong" is stronger than "some would argue this may be suboptimal."

**Always write one idea per piece.** One LinkedIn post, one insight. One newsletter, one point. If you have two ideas — you have two pieces.

**Always load examples before generating.** Voice profiles describe. Examples show. When they conflict, examples win.

**Always run the self-check before saving.** Every piece. Even the short ones. The scrub takes 60 seconds and catches half the problems.

**Always ask: could only this person have written this?** If the answer is no — find what's uniquely theirs and add it. A specific client name. A specific result. A specific belief they hold. Something that doesn't apply to everyone.

**Always let the ending land.** The last sentence is the whole piece compressed. Don't explain it. Don't add a lesson. Don't add a question. Let it land and stop.

**Always match the voice profile to the content type.** Personal LinkedIn = "I." Company LinkedIn = "we." Not sometimes. Always.

**Always prefer the shorter version.** If the sentence works without the last clause — cut it. If the paragraph works without the last sentence — cut it. Writing is what's left after you've removed everything that isn't necessary.

---

*These rules apply to every content type: blog, social, newsletter, email, sales. No exceptions. The goal is text that reads like a specific human being wrote it — not like a model optimized for average quality across all possible inputs.*
