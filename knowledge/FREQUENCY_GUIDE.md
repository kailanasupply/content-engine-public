# Frequency Guide
# Human-readable guide to content cadence — what to make, how often, and why.
# The machine rules live in config/cadence.yaml. This file explains the thinking.
# Loaded by generators and morning scan to inform prioritization decisions.

---

## The core philosophy

More content is not better content. The goal is not to fill a calendar.
The goal is to publish things worth reading, at a pace that builds trust without burning out.

Every format has a natural frequency. Violate it and the channel suffers.
Post personal LinkedIn daily when you have nothing to say — your audience trains itself to ignore you.
Send a newsletter every week that says nothing new — your open rates crater.

**The engine will not generate content to fill a gap. It generates content because something worth saying exists.**

---

## Format-by-format guide

### Personal LinkedIn
**Frequency: 3–5x per week when active input exists**
**Never: more than once per day | Never: without a real insight**

This is your highest-frequency channel and your most personal one. Each post needs a specific observation, story, or opinion — not a rephrased article you read, not a generic tip.

The posts that perform are the ones that could only come from you. If someone else could have written the same thing, it's not ready.

When to skip: if your notes from the past 24 hours are only logistics, meetings, or admin — skip the post. An absent day is better than a filler post.

When to post more: a strong insight from a client call, a surprising result from a decision you made, a mistake worth sharing.

---

### Company LinkedIn
**Frequency: 2–3x per week**
**Never: repurposing personal posts with "we" swapped in**

The company page has a different job than your personal page. It's proof, not personality. Client outcomes, product thinking, brand POV, team announcements.

The company page underperforms when it becomes a megaphone for the founder's personal takes. Keep the voices separated.

When to skip: when there's no client result, no real company news, and no genuine brand POV — don't manufacture a post.

---

### Twitter / X
**Frequency: daily to 2x/day if active**
**Never: threads for ideas that don't need threads**

Twitter is the fastest-feedback channel. Short, specific, one point. Use it to test an idea before you build it into a LinkedIn post or blog. The constraint forces clarity.

Threads are for arguments that have logical steps — not for turning a LinkedIn post into a numbered list.

When to skip: when you're just rephrasing something you posted on LinkedIn.

---

### Newsletter
**Frequency: weekly**
**Hard cap: once per week. Never twice. Never skip more than 2 weeks without a note to your list.**

The newsletter is the most intimate channel. Your readers gave you permission to show up in their inbox. Honor that by only showing up when you have something worth saying.

A good newsletter is one idea, explored well. Not a content roundup. Not "here's everything I did this week."

Skipping a week: if you have nothing to say this week — say that briefly, with something honest about why. Don't manufacture content to maintain the streak.

---

### Blog
**Frequency: 1x per week max | More realistically: 2x per month**
**Never: without a specific angle. "A blog post about X" is not an angle.**

Blog posts do two jobs: they rank for search terms your audience is already using, and they establish your thinking on topics you own. A post that does neither is a vanity exercise.

Good blog inputs are long recordings, deep note sessions, or fully-formed opinions. Thin inputs → skip the blog → do a LinkedIn post instead.

When to produce more: when there's a keyword gap worth owning, when a topic comes up repeatedly with clients, when you have strong proof to back up a bold claim.

---

### Email sequences
**Frequency: campaign-triggered only**
**Never: in the daily scan | Never: without a full brief**

An email sequence is infrastructure, not content. It exists to carry someone from awareness to decision over time. It requires a campaign brief, a defined audience, and a clear arc.

Don't produce email sequences speculatively. Build them when there's a real reason — a product launch, a new audience segment, a nurture flow for a specific lead type.

---

### Sales assets
**Frequency: on-demand only**
**Never: automatically generated**

One-pagers, decks, outreach emails — these are built for a specific prospect or situation. They require context that only comes from a real sales conversation or a brief.

The morning scan will never queue a sales asset. These always start with a human decision.

---

## The noise prevention logic

The morning scan applies four filters before anything gets queued:

**1. Is there new, unprocessed input?**
No input → no generation. Full stop.

**2. Is the input rich enough for the format?**
A blog needs a recording or detailed notes (500+ words of substance).
A LinkedIn post can come from a short, sharp observation.
Thin input → fewer formats, shorter formats, or no generation.

**3. Has this topic been covered recently?**
Same angle published in the last 30 days → skip or significantly differentiate.
Topic covered 3+ times in the last 30 days → flag as saturated, deprioritize.

**4. Does the proposed piece have a real reason to exist?**
Required: one of (insight / opinion / story / announcement / education / proof).
If none applies clearly → hold for human judgment, don't auto-generate.

---

## The weekly rhythm (suggested)

| Day | Typical output |
|-----|---------------|
| Monday | Personal LinkedIn (from weekend thinking / new week framing) |
| Tuesday | Company LinkedIn (client result, or brand POV) |
| Wednesday | Personal LinkedIn + Twitter activity |
| Thursday | Newsletter (sent Thursday morning) |
| Friday | Personal LinkedIn (week-end reflection or bold take) |
| Weekend | Notes drop in inputs/ — engine picks them up Monday 7am |

This is a rhythm, not a rule. Some weeks produce more. Some weeks produce one strong piece. Follow the signal, not the schedule.

---

## For client builds

When building this engine for a client:
- Adjust frequency caps in `config/cadence.yaml` based on their realistic capacity
- If they can't maintain daily LinkedIn — set `max_per_week: 3` and build for quality over volume
- A client who publishes 3 strong posts a week consistently beats one who publishes 5 mediocre ones
- The engine should match their real capacity, not an aspirational one they'll abandon in month 2
