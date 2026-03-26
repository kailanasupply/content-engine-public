# Newsletter Template

## Generator Instructions
<!-- Loaded by the newsletter generator. One issue = one insight. Tight, personal, direct.
     BEFORE WRITING: Load anti-ai-rules.md first, then load the correct voice profile.
     Personal newsletter (from the founder) → voice-personal.md + examples/personal/
     Company newsletter (from the brand) → voice-company.md + examples/company/
     When uncertain which applies, check the campaign brief or ask. -->

---

## FRONTMATTER
```yaml
---
id: [uuid]
type: newsletter
subtype: [weekly|campaign|special-edition]
title: [Subject line]
title_variants:
  - [variant 1]
  - [variant 2]
preview_text: [max 90 chars — complements subject line, adds intrigue]
voice_profile: [personal|company]
client: [client]
campaign: [campaign or null]
pillar: [pillar]
persona: [persona id]
platform: [personal-email|company-email]
source_input: [path]
source_insight: [one sentence]
status: draft
created: [timestamp]
updated: [timestamp]
word_count: [n]
reading_time_minutes: [n]
notion_id: null
notion_url: null
airtable_record_id: null
model: [model]
generator_version: "1.0"
generation_notes: ""
---
```

---

## SUBJECT LINE
Write the subject line. Then write 2 variants.

**Rules:**
- 40–60 characters ideally (some email clients cut longer)
- Specific is better than clever
- Personal tone — like an email from a friend, not a brand
- Avoid: "Newsletter #47", "Weekly Update", anything that sounds like a mass email

**Subject line:**

**Variant 1:**

**Variant 2:**

**Preview text** (max 90 chars — visible in inbox before opening):

---

## NEWSLETTER BODY

**Target length: 300–600 words. Tight. One idea. Done.**

---

### Opening — Personal Hook (50–100 words)
Start with something personal, specific, and human.
A moment, an observation, something that happened recently.
This is what makes newsletters different from blog posts — the personal angle.

The reader should feel like they're getting a note from someone they know,
not a piece of content from a brand.

[OPENING]

---

### The Insight (150–250 words)
Transition from the personal hook to the core idea.
Explain it clearly. Make it useful.

Unlike a blog post: don't build up slowly. Get to the point fast.
The reader opted in — they're ready. Respect their time.

Use a real example if possible. Not hypothetical — actual.

[INSIGHT]

---

### So What? (50–100 words)
The implication. What does the reader now understand, believe, or know how to do?
Make this actionable but not listicle-y.
One thing they can do or think about. Not five.

[SO WHAT]

---

### Close (50–100 words)
End with one of:
- A question for the reader ("What's your take on this?")
- A simple CTA ("If this resonated, here's where to go next: [link]")
- A memorable closing line that echoes the opening

**Do NOT close with:** "Thanks for reading!", a generic sign-off, or a list of links.

One CTA maximum. Make it feel natural, not bolted on.

[CLOSE]

---

### Sign-off
Keep it consistent with brand voice.

[SIGN-OFF NAME]
[Optional one-line tagline or "reply to this email" prompt]

---

## QUALITY CHECKLIST
- [ ] `anti-ai-rules.md` self-check passed — no banned words, no -ing clauses, no fake significance
- [ ] Correct voice profile loaded and applied (personal = I, company = we)
- [ ] Subject line is specific — not newsletter-y or generic
- [ ] Preview text adds intrigue, doesn't repeat subject line
- [ ] Opens with something specific and concrete — not a generic setup
- [ ] 300–600 words total
- [ ] One central idea — doesn't meander into two topics
- [ ] Actionable close — reader knows what to do with this
- [ ] voice_profile field set in frontmatter
- [ ] Voice matches `brand/[client]/voice.md` — conversational register
- [ ] Maximum 1 CTA
