# Freshness Rubric

Used by the evergreen miner to score archived ideas. Each criterion is scored 0–2. Maximum total score: 10.

Score ≥ 7 → strong candidate (surface immediately)
Score 5–6 → needs work (surface with a "requires refresh" note)
Score < 5 → skip this cycle

---

## Criterion 1: Timelessness (0–2)

How tied is the core insight to a specific moment in time?

- **0** — The idea is inseparable from a news event, product launch, or moment that has passed. Would feel dated if published now.
- **1** — Core insight is mostly timeless, but one element (a stat, a reference, a comparison) would need updating before publishing.
- **2** — The insight holds regardless of when it's published. Could go live today or in a year without any changes.

---

## Criterion 2: Pillar fit (0–2)

How well does this idea fit the client's active content pillars?

- **0** — Off-pillar. The idea doesn't connect to any established theme the client wants to own.
- **1** — Adjacent. It connects to a pillar but isn't a core expression of it — would need framing to land in the right territory.
- **2** — On-pillar. This idea is a direct expression of a content pillar the client actively publishes in.

---

## Criterion 3: Narrative hook strength (0–2)

Does the idea have a specific, story-able hook?

- **0** — The idea is a topic or theme, not a story. "Fraud leadership is important" is not a hook.
- **1** — There's a hook but it's generic — something another person could have written. "When I changed how I thought about fraud" is a hook but a weak one.
- **2** — The hook is specific and owned. A real moment, a real observation, a real number. Something only this person could say. "The day I realized our 97% approval rate was actually hurting us."

---

## Criterion 4: Angle freshness (0–2)

Has this specific angle been used recently in generated or published content?

Check against `generation-log` and `performance/tracker.yaml`.

- **0** — This exact angle has been used in a published or approved piece in the last 90 days.
- **1** — The topic has been covered recently, but from a different angle. The specific angle in this idea is still fresh.
- **2** — Neither this topic nor this angle has appeared in recent content. Completely fresh territory.

---

## Criterion 5: Audience match (0–2)

How well does this idea speak to the client's primary target persona right now?

Load `brand/[client]/personas.yaml` to check.

- **0** — This idea speaks to the wrong audience. The pain point or vocabulary doesn't match any active persona.
- **1** — Partial match. The idea is relevant to one persona but not the most important one, or needs reframing to land with the right audience.
- **2** — Direct match. This idea speaks the exact language of the primary persona and addresses a pain point they're actively experiencing.

---

## Scoring examples

**Score 9/10** — "The 18-month rule for fraud programs"
- Timelessness: 2 (permanently true)
- Pillar fit: 2 (fraud leadership pillar)
- Hook strength: 2 (specific rule, specific timeframe)
- Angle freshness: 2 (used this exact post for personal-linkedin but another angle available)
- Audience match: 1 (speaks to fraud leaders but also accessible to adjacent audience)

**Score 5/10** — "AI will change fraud operations"
- Timelessness: 1 (true but needs a fresh angle now)
- Pillar fit: 2 (fraud + AI pillar)
- Hook strength: 0 (no hook — pure theme)
- Audience match: 2 (directly relevant to fraud ops)
- Angle freshness: 0 (this angle has been done recently)

---

## Notes

- When in doubt, score conservatively. A score of 7 you're confident in is better than a speculative 9.
- Hook strength is the single most predictive criterion for content performance. Weight it accordingly when reviewing borderline candidates.
- Pillar fit matters more for company-voice content than personal-voice content. Personal posts can flex outside pillars when the story is strong enough.
