# Founder Guide
# Your one-page reference for using the Content Engine.
# You don't need to know how it works. You need to know what it needs from you.

---

## What the engine needs from you

**Daily (2 minutes):**
Read the morning scan report. Reply `GO`, `SKIP`, or tell us what to change.

**A few times a week (5 minutes):**
Read the pieces your team flagged as `review`. Approve the ones you'd post. Archive the ones you wouldn't.

**Once a week (15 minutes):**
Tell us how this week's content performed. Rough signals are fine — "the Tuesday post got a ton of DMs" is enough.

That's it. Everything else runs without you.

---

## Your approval powers

You're the only person who can:

- Approve a content manifest (say GO to generate)
- Move a piece from `review` to `approved` (say this is ready to publish)
- Approve cadence changes (increase or decrease publishing frequency)
- Do a voice calibration session (you have to be there — it's about your voice)

Nothing publishes without you touching it. Ever.

---

## Reading a draft

Open any file in `drafts/[your-client]/`. The content is below the frontmatter (the section at the top between the `---` marks).

Read it like you'd read it as a post. Then ask yourself:
- "Would I post this exactly as is?"
- "Does this sound like me on a good day?"

If yes → change `status: review` to `status: approved` in the frontmatter (or tell your team to do it).

If no → leave a comment at the bottom of the file explaining what's off, and change `status: review` back to `status: draft`.

---

## Voice calibration (when to ask for it)

Run `/calibrate-voice` when:
- Three pieces in a row don't sound like you
- You keep editing the same thing out of every draft
- Something changed in how you think about your audience and the content isn't tracking

Takes 20 minutes. Your team leads it. You just react to what you're shown.

---

## When the business changes

Tell your team immediately when:
- You launch or kill an offer
- Your ICP shifts
- You've heard the same objection from prospects three times
- You land a significant client or lose one
- The story you're telling about what you do changes

They'll run `/update-company-context` and the engine will reflect the new reality in all future content.

---

## Performance — what to tell us

After you check LinkedIn/email/whatever:

Tell us:
1. Which posts did well (rough signal — "lots of comments," "two leads DM'd me")
2. Which posts landed flat
3. Anything you'd never post again

You don't need numbers. Your gut read is the most valuable data we have.

---

## The one thing that makes this better over time

Your examples. The posts you've written that are exactly right. Drop them in:
```
brand/[your-client]/examples/personal/
```

The engine loads those every time it generates personal content for you. The more examples in there, the closer the outputs are to your natural voice from day one.

When a generated piece is exceptional — move a copy to your examples folder. It becomes training data for the next run.

---

## What you don't need to touch

- `config/` — your team manages this
- `scripts/` — runs automatically
- `templates/` — used internally
- `performance/tracker.yaml` — your team logs this based on what you tell them
- `CLAUDE.md` — the engine's operating manual

You live in: `drafts/[your-client]/` and `brand/[your-client]/examples/`.

---

*The engine is only as good as what you put in it. Your examples, your performance gut reads, and your voice calibration sessions are what separate "AI content" from "your content."*
