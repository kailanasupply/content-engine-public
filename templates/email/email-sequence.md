# Email Sequence Template

## Generator Instructions
<!-- Loaded by the email sequence generator. Requires a campaign brief as input.
     BEFORE WRITING: Load anti-ai-rules.md first, then load the correct voice profile.
     Emails sent from the founder personally → voice-personal.md + examples/personal/
     Emails sent from the brand/company → voice-company.md + examples/company/
     This matters: a nurture sequence from the founder reads very differently
     from a company drip sequence. Check the brief. When uncertain, ask. -->

---

## FRONTMATTER (one file per sequence, contains all emails)
```yaml
---
id: [uuid]
type: email
subtype: [welcome|nurture|launch|re-engagement]
title: [Sequence name — internal reference]
client: [client]
campaign: [campaign]
pillar: [pillar]
persona: [persona id]
platform: email
source_input: [path to campaign brief]
source_insight: [campaign key message]
status: draft
created: [timestamp]
updated: [timestamp]
email_count: [n]
notion_id: null
notion_url: null
airtable_record_id: null
model: [model]
generator_version: "1.0"
generation_notes: ""
---
```

---

## SEQUENCE STRATEGY

Before writing any emails, map the emotional arc:

```
Email 1: [Emotion/goal — e.g., "Welcome + establish trust"]
Email 2: [e.g., "Surface the core pain"]
Email 3: [e.g., "Introduce the idea / reframe the problem"]
Email 4: [e.g., "Proof — show it works"]
Email 5: [e.g., "Soft CTA — invite action"]
```

**Arc principles:**
- Early emails: broad welcome, low pressure, value delivery
- Middle emails: deepen the insight, build belief, handle objections
- Later emails: specificity, urgency, clear ask

---

## EMAIL STRUCTURE (repeat for each email)

---

### EMAIL [N] — [Internal name, e.g., "The Problem Email"]

**Subject line:**
**Subject variant 1:**
**Subject variant 2:**
**Preview text** (max 90 chars):

**Goal of this email:**
<!-- What should the reader think, feel, or do after reading this? -->

**Body:**

[OPENING — personal, specific hook]

[BODY — 100–200 words. One idea. Get in, get out.]

[CTA — one action. Clear. Low friction where appropriate, higher friction later in sequence.]

**CTA button text (if applicable):**
**CTA URL:**

**Tone note for this email:**
<!-- e.g., "More personal than usual", "Building urgency", "Peer-level conversation" -->

---

## SEQUENCE TYPES

### Welcome Sequence (3 emails, 3–5 days apart)

**Email 1 — Welcome + who you are**
- Immediate send after opt-in
- Short (100–150 words)
- Who you are, what they can expect, one quick win
- No hard sell

**Email 2 — Your core belief**
- Day 3
- The philosophical stance that everything else is built on
- Tells them what you stand for — and what you stand against
- Plant the seed of the problem you solve

**Email 3 — The offer introduction**
- Day 5–7
- Introduce what you do / what's available
- Soft CTA — no urgency yet, just awareness

---

### Nurture Sequence (5 emails, weekly)

**Email 1 — The insight email** (pure value)
**Email 2 — The story email** (proof/case study)
**Email 3 — The objection email** (handle the #1 reason they hesitate)
**Email 4 — The framework email** (give them a mental model)
**Email 5 — The CTA email** (make the ask — specific, with urgency if applicable)

---

### Launch Sequence (7 emails, 7–10 days)

**Email 1 — Pre-launch teaser** (something's coming)
**Email 2 — Problem agitation** (make the pain real)
**Email 3 — The announcement** (here's what it is)
**Email 4 — FAQ / objection handling** (answer what they're wondering)
**Email 5 — Social proof** (results, testimonials, case studies)
**Email 6 — Urgency + scarcity** (why now)
**Email 7 — Last chance** (closes with conviction, not desperation)

---

## EMAIL WRITING RULES

1. **Subject lines are 80% of the job** — if they don't open, nothing else matters
2. **First line after subject must pull them in** — don't waste it on pleasantries
3. **One idea, one CTA** — never two asks in one email
4. **150–250 words** — respect their inbox; say less, mean more
5. **Write like a human** — "Hey" not "Dear [First Name]"
6. **Never start with "I"** — start with "You" or the hook itself
7. **CTA clarity** — tell them EXACTLY what to do and what happens next

## QUALITY CHECKLIST
- [ ] `anti-ai-rules.md` self-check passed on every email in the sequence
- [ ] Correct voice profile loaded: personal (I, from the founder) or company (we, from the brand)
- [ ] Emotional arc mapped before writing — not just individual emails
- [ ] Each email has one clear goal
- [ ] Subject lines are specific and human — not corporate or newsletter-y
- [ ] Each email 150–250 words — no padding
- [ ] First line of every email hooks before the fold
- [ ] Max 1 CTA per email
- [ ] Urgency builds naturally across the sequence — not forced
- [ ] voice_profile field set in frontmatter
