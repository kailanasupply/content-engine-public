# Success Metrics
# Engagement thresholds that signal when cadence.yaml should be adjusted.
# The engine reads this file during /synthesize-learnings to determine
# whether frequency should increase, hold, or decrease per channel.

---

## How this file works

After every synthesis run, the engine compares recent average performance
against the thresholds below. If a channel is consistently above threshold,
frequency can increase. Below threshold — frequency holds or drops.

The engine never adjusts cadence.yaml automatically. It proposes changes
and you confirm. This file defines the thresholds that trigger the proposal.

---

## Baseline thresholds by channel

These are starting thresholds. After 30+ data points per channel, update
these numbers to reflect your actual audience baselines.

### Personal LinkedIn

| Signal | Below baseline | At baseline | Above baseline |
|--------|---------------|-------------|----------------|
| Likes per post | < 30 | 30–100 | > 100 |
| Comments per post | < 5 | 5–20 | > 20 |
| DMs generated | 0 | 1–3/week | > 3/week |
| Leads from content | 0 | 1–2/month | > 2/month |

**Cadence rule:**
- 3 consecutive posts below baseline → reduce to 3x/week, flag for voice calibration
- Consistent above baseline → eligible for 5x/week if input volume supports it

### Company LinkedIn

| Signal | Below baseline | At baseline | Above baseline |
|--------|---------------|-------------|----------------|
| Likes per post | < 20 | 20–60 | > 60 |
| Comments per post | < 3 | 3–10 | > 10 |
| Reposts/shares | 0 | 1–5 | > 5 |
| Profile visits from post | < 10 | 10–50 | > 50 |

**Cadence rule:**
- 3 consecutive posts below baseline → hold at 2x/week, review content type mix
- Consistent above baseline → eligible for 4x/week

### Newsletter

| Signal | Below baseline | At baseline | Above baseline |
|--------|---------------|-------------|----------------|
| Open rate | < 25% | 25–45% | > 45% |
| Click rate | < 2% | 2–8% | > 8% |
| Replies received | 0 | 1–5/send | > 5/send |
| Unsubscribes/send | > 0.5% | < 0.5% | < 0.1% |

**Cadence rule:**
- Open rate below baseline for 4 weeks → pause newsletter, run calibration session
- Replies consistently above baseline → consider biweekly send, preserve quality
- Unsubscribes above 0.5% → immediate content review, do not increase frequency

### Blog

| Signal | Below baseline | At baseline | Above baseline |
|--------|---------------|-------------|----------------|
| Organic traffic/post (30-day) | < 100 | 100–500 | > 500 |
| Time on page | < 2 min | 2–4 min | > 4 min |
| Social shares | < 5 | 5–20 | > 20 |
| Leads from post | 0 | 1–3/post | > 3/post |

**Cadence rule:**
- Organic traffic below baseline after 60 days → review SEO angle approach
- Leads consistently above baseline → increase to 2x/week if input supports it

### Twitter / X

| Signal | Below baseline | At baseline | Above baseline |
|--------|---------------|-------------|----------------|
| Impressions/tweet | < 200 | 200–1000 | > 1000 |
| Engagements (likes + replies) | < 10 | 10–50 | > 50 |
| New followers/week | 0 | 1–10 | > 10 |
| Profile clicks | < 20/week | 20–100/week | > 100/week |

**Cadence rule:**
- Below baseline for 2 weeks → reduce to 3x/week, test different content types
- Above baseline consistently → maintain 7x/week max

---

## Quality signals (override frequency rules)

These signals take priority over engagement numbers:

**Increase quality gate strictness when:**
- Unsubscribe rate rises (any channel)
- You receive negative feedback on a piece ("this doesn't sound like you")
- A piece gets high engagement for the wrong reasons (controversy, not substance)
- Voice calibration session surfaces consistent complaints

**Decrease generation volume when:**
- You're not reviewing drafts — backlog > 10 unapproved pieces
- Frequency outpacing input quality (thin notes → thin content)
- The founder reports feeling disconnected from the content

---

## Auto-proposal format

When /synthesize-learnings triggers a cadence proposal, it outputs this:

```
CADENCE PROPOSAL
Based on [n] data points over the last [n] days:

Personal LinkedIn: [HOLD / INCREASE to Nx/week / DECREASE to Nx/week]
  Reason: [specific signal — e.g., "avg 47 likes/post vs 30 baseline, 3 leads generated"]

Newsletter: [HOLD / INCREASE / DECREASE]
  Reason: [specific signal]

[etc.]

Proposed cadence.yaml changes:
  personal-linkedin max_per_week: [current] → [proposed]
  newsletter cadence: [current] → [proposed]

Confirm? (yes to apply / no to hold / edit to adjust)
```

---

## Updating these thresholds

After 60–90 days of real data, your baseline numbers will be known.
Run `/update-success-metrics` (or edit this file manually) to update thresholds
to reflect your actual audience — not the generic starting points above.

The point of the thresholds is not to chase engagement. It's to catch
underperformance before it compounds and overproduction before it burns trust.

**NOTE FOR NEW CLIENTS:**
These thresholds are templates. Customize them to your audience size and engagement patterns.
A company with 5k followers will have different baseline metrics than one with 500k.
