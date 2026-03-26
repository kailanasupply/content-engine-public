# Sales Assets Template

## Generator Instructions
<!-- Loaded by the sales asset generator. Requires a campaign brief or specific prospect context.
     BEFORE WRITING: Load anti-ai-rules.md first. Sales assets use voice-company.md always —
     they speak from the brand, not the individual. Load examples/company/ for reference.
     Exception: personal outreach emails (cold email from the founder) → voice-personal.md -->

---

## ONE-PAGER

### FRONTMATTER
```yaml
---
id: [uuid]
type: sales
subtype: one-pager
title: [Asset name — e.g., "ContentOS One-Pager for Marketing Agencies"]
client: [client]
campaign: [campaign or null]
pillar: [pillar]
persona: [persona id]
platform: null
source_input: [path]
source_insight: [key value prop this asset leads with]
status: draft
---
```

### Structure

**HEADLINE**
The value prop — specific and outcome-focused.
Not "Introducing [Product Name]" — that's about you.
"[Specific result] for [specific audience] — without [specific obstacle]"

**THE PROBLEM (50–75 words)**
Paint the "before" state vividly. Use the persona's actual language.
Make them feel understood before you pitch anything.

**THE SOLUTION (75–100 words)**
What you do and how it addresses the problem.
Not a feature list — a description of the transformation.
Connect it directly to the problem you just described.

**HOW IT WORKS (50–75 words)**
3 steps or phases — simple process overview.
Make it feel easy, not complex.

**PROOF (50–75 words)**
One result, one client story, or one specific outcome.
Specific beats general: "47% faster" beats "significantly faster"

**CTA**
One clear next step. Specific action + what happens next.
"Book a 20-minute demo" not "Learn more"

---

## OUTREACH EMAIL (Cold)

### FRONTMATTER
```yaml
---
id: [uuid]
type: sales
subtype: outreach-email
title: [Sequence name — e.g., "Cold outreach — Marketing Agency CMOs"]
client: [client]
campaign: [campaign or null]
persona: [persona id]
---
```

### Structure

**Subject line:**
Personal, specific, no buzz words.
Reference something real about them or their situation.
Under 50 characters.

**Subject variant 1:**
**Subject variant 2:**

---

**Email body (75–100 words max — no exceptions):**

[First line — the trigger. Why you're emailing THIS person, NOW. Specific.]

[Second section — the observation. What you've noticed about their situation.]

[Third section — the connection. Why that maps to what you do.]

[CTA — one question or one soft ask. Not "let me know if you're interested."]

---

**Rules for outreach emails:**
- 75–100 words. Not 101. Brevity = respect.
- Specific trigger in line 1 (a post they wrote, a company announcement, a mutual connection)
- Never pitch features — pitch the problem you solve
- CTA = one low-friction ask ("Worth a 15-min call this week?" or "Relevant?")
- No "I hope this finds you well" or "My name is X and I work at Y"

---

## DECK OUTLINE

### FRONTMATTER
```yaml
---
id: [uuid]
type: sales
subtype: deck-outline
title: [e.g., "ContentOS Agency Pitch Deck Outline"]
client: [client]
campaign: [campaign or null]
persona: [persona id]
slide_count: [n]
---
```

### Structure

**Slide 1 — Title**
Headline + one-line description of what this deck is about.

**Slide 2 — The Problem**
Make the audience feel understood. Their world, their pain. Not your solution yet.
3 bullet points or one powerful statement.

**Slide 3 — Why Now**
Why is this problem more acute or urgent today than it was 2 years ago?
Market forces, technology shifts, competitive pressure.

**Slide 4 — The Failed Alternatives**
What have they tried? Why did it not work?
This differentiates you without naming competitors.

**Slide 5 — Introducing [Solution]**
The what — one sentence.
The how — 3 points.
The outcome — one sentence.

**Slide 6 — How It Works**
The process. 3 steps max. Visual-first thinking.
Each step: title + one sentence description.

**Slide 7 — Proof**
Results, case study, or social proof.
Real numbers. Real outcomes. Real client if possible.

**Slide 8 — Who It's For**
The ICP. Be specific — helps prospects self-select.

**Slide 9 — Pricing / Offer / Next Step**
Clear. Simple. What's included, what it costs, what happens next.

**Slide 10 — CTA**
One ask. Schedule a call, start a trial, sign here.

---

## QUALITY CHECKLIST
- [ ] `anti-ai-rules.md` self-check passed — sales assets are the most prone to AI puffery
- [ ] voice_profile = company for all assets except personal outreach emails
- [ ] Leads with the problem/outcome, not the product
- [ ] Uses prospect/persona language, not internal jargon
- [ ] All claims are evidenced (no "we help companies succeed")
- [ ] One CTA throughout — consistent and clear
- [ ] Voice matches `brand/[client]/voice-company.md` (or `voice-personal.md` for founder outreach)
- [ ] Outreach email is under 100 words (count them)
