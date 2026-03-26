# Social Posts Template

## Generator Instructions
<!-- Loaded by the social generator agent. One file = one insight across all platforms.
     BEFORE WRITING: Load anti-ai-rules.md, then load the correct voice profile.
     LinkedIn personal → voice-personal.md + examples/personal/
     LinkedIn company → voice-company.md + examples/company/ -->

---

## VOICE DETERMINATION (resolve before generating)

```
If platform = personal-linkedin OR this content is written as the founder/individual:
  → Load: brand/[client]/voice-personal.md
  → Load examples from: brand/[client]/examples/personal/
  → Use: I / me / my
  → Tone: raw, opinionated, personal anecdotes, specific stories

If platform = company-linkedin OR this content is written as the brand:
  → Load: brand/[client]/voice-company.md
  → Load examples from: brand/[client]/examples/company/
  → Use: we / our / the company
  → Tone: polished, brand POV, client outcomes, institutional authority
```

**If the campaign brief or content manifest does not specify — ask before generating.**

---

## FRONTMATTER
```yaml
---
id: [uuid]
type: social
subtype: [personal-linkedin-post|company-linkedin-post|twitter-thread|instagram-caption]
title: [Insight slug used as internal reference]
voice_profile: [personal|company]
client: [client]
campaign: [campaign or null]
pillar: [pillar]
persona: [persona id]
platform: [personal-linkedin|company-linkedin|twitter|instagram]
source_input: [path]
source_insight: [one sentence]
status: draft
created: [timestamp]
updated: [timestamp]
word_count: [total across all variants]
notion_id: null
notion_url: null
airtable_record_id: null
model: [model]
generator_version: "1.0"
generation_notes: ""
---
```

---

# LINKEDIN — 5 Variants

Generate 5 distinct LinkedIn posts from the same insight.
Each must be a completely different take — different hook, different angle, different structure.
Not 5 versions of the same thing. 5 genuinely different attempts to make the idea land.

---

## PERSONAL LinkedIn Rules (voice_profile = personal)

This is the founder/individual's personal account. It reads like a smart person thinking out loud — not a brand posting content.

- **Pronoun:** I / me / my — always first person singular
- **Length:** 150–400 words — personal posts can go longer when the story earns it
- **Stories:** From their actual life — a conversation they had, a mistake they made, something they noticed. Not hypotheticals.
- **Opinions:** Direct. They can be wrong. They can say "I used to think X, and I was wrong."
- **CTAs:** Soft — "Thoughts?", "What's your take?", or no CTA at all. Never "Book a demo."
- **Format:** Paragraphs and line breaks — no bullet lists. No headers. No bold text mid-post.
- **Hashtags:** 3–5 max, after a blank line. Optional for personal posts — skip if they feel forced.
- **What to avoid:** Anything that sounds like it came from a marketing team. No "We're excited to share," no "This is a reminder that," no "At [Company], we believe."

**Personal hook formulas:**
1. Start mid-scene: "Last Tuesday I was on a call with a client and she said something I can't stop thinking about."
2. Contradiction: "I've been giving advice for 5 years that I now think is wrong."
3. Uncomfortable truth: "Here's what no one in [industry] will say out loud."
4. Specific observation: "I've noticed something in the last 30 client projects that I haven't seen written about anywhere."
5. Short declarative: "Most [X] isn't bad because of [assumed reason]. It's bad because of [real reason]."

---

## COMPANY LinkedIn Rules (voice_profile = company)

This is the brand's company page. It speaks with institutional authority — polished, purposeful, and outcome-focused. Not a press release, but not a personal diary either.

- **Pronoun:** We / our / the team — always first person plural
- **Length:** 100–200 words — tighter than personal posts. Say it, support it, close it.
- **Stories:** Client outcomes and team milestones — not personal anecdotes from the founder
- **Opinions:** Brand POV — positioned, considered, and backed up. The company has a stance.
- **CTAs:** Clearer than personal — can drive to content, a demo, or a conversation
- **Format:** Clean paragraphs. Minimal formatting. One idea per post.
- **Hashtags:** 3–5, always — they matter more for company page discoverability
- **What to avoid:** Anything that sounds too personal or self-referential. The brand doesn't have bad days. The brand doesn't second-guess itself publicly. That's what the personal account is for.

**Company hook formulas:**
1. Outcome-first: "Our clients reduce [X] by [Y]. Here's why that's harder than it sounds."
2. Category claim: "Most [category] tools solve the wrong problem."
3. Client story opening: "A [persona type] came to us [time ago] with [specific problem]."
4. Counterintuitive industry take: "The [standard practice] that's costing [persona] more than they realize."
5. Announcement framed as insight: "We've spent [time] working on [thing]. What we learned changed how we think about [topic]."

---

**LinkedIn Post Rules (both profiles):**
- Strong first line — this is the hook before "see more" cuts off. It must earn the click.
- No mid-post headers or subheadings
- Run the anti-AI self-check before saving every variant

---

## LinkedIn Variant 1

[HOOK]

[BODY — 3–5 short paragraphs or punchy lines]

[CTA]

[HASHTAGS]

---

## LinkedIn Variant 2

[Different hook style from Variant 1]

[Body]

[CTA]

[HASHTAGS]

---

## LinkedIn Variant 3

[Body]

[CTA]

[HASHTAGS]

---

## LinkedIn Variant 4

[Body]

[CTA]

[HASHTAGS]

---

## LinkedIn Variant 5

[Body]

[CTA]

[HASHTAGS]

---

# TWITTER/X — Thread

Write one complete Twitter/X thread (5–8 tweets) that tells the full story of the insight.

**Twitter Thread Rules:**
- Tweet 1: The hook — must be strong enough to stand alone AND make people click "show thread"
- Tweets 2–6: Build the argument. One point per tweet. Short sentences.
- Final tweet: The takeaway. The "so what." Can include a CTA or link.
- Each tweet: max 280 characters
- Format: Number each tweet [1/n], [2/n], etc.
- No hashtags mid-thread — one optional hashtag block on the last tweet only

---

## Twitter Thread

**1/[n]**
[HOOK TWEET — most important. Should stop the scroll.]

**2/[n]**
[Point 1]

**3/[n]**
[Point 2]

**4/[n]**
[Point 3]

**5/[n]**
[Point 4]

**6/[n]**
[Point 5 — optional]

**7/[n]** (or last)
[TAKEAWAY + optional CTA]

---

# INSTAGRAM — 3 Variants

**Instagram Caption Rules:**
- 100–150 words for the caption
- Hook in first line (same rules as LinkedIn)
- Can be more personal/human than LinkedIn
- End with a question to drive comments
- Keep hashtags in a separate comment (note this in the file)
- Include a [VISUAL NOTE] describing what the image/graphic should show

---

## Instagram Variant 1

[VISUAL NOTE: Describe the image that should accompany this caption]

[CAPTION]

[QUESTION CTA]

---

## Instagram Variant 2

[VISUAL NOTE]

[CAPTION]

[QUESTION CTA]

---

## Instagram Variant 3

[VISUAL NOTE]

[CAPTION]

[QUESTION CTA]

---

## QUALITY CHECKLIST
- [ ] LinkedIn: 5 genuinely different angles (not 5 variations of the same hook)
- [ ] LinkedIn: Each post works standalone — doesn't need context from others
- [ ] Twitter: Thread hook would stop the scroll on its own
- [ ] Twitter: Each tweet fits in 280 characters
- [ ] Variants don't sound like generic AI content — they sound like the brand voice
- [ ] All content matches `brand/[client]/voice.md`
