---
name: multi-brand-router
description: Enforces channel restrictions and brand routing rules across all 4 brands. The single source of truth for "can this content be made for this brand on this channel?" Must be consulted before any generation decision. Critically: SaySo = X + Company LinkedIn ONLY. No newsletter. No personal voice. No email. No blog. Trigger: before any generation, "what channels can I use for [brand]", "is [format] allowed for [brand]", routing decisions.
triggers:
  - before any generation
  - what channels can I use for
  - is [format] allowed for
  - channel check
  - brand routing
  - can I make a [format] for [brand]
loop: consulted during Plan phase of every skill
---

# Multi-Brand Router

The routing authority. Before any content is proposed or generated, this skill confirms the brand × channel × voice combination is legal. When in doubt, check here.

---

## Master routing table

| Brand | Personal LinkedIn | Company LinkedIn | Twitter/X | Newsletter | Blog | Email Seq | Sales |
|-------|:-----------------:|:----------------:|:---------:|:----------:|:----:|:---------:|:-----:|
| brian | ✅ primary | ✅ | ✅ | ✅ | 🚫 | ✅ | ✅ |
| house-of-fraud | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| safeguard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| sayso | 🚫 NEVER | ✅ only | ✅ only | 🚫 NEVER | 🚫 NEVER | 🚫 NEVER | 🚫 NEVER |

---

## Brand × Voice matrix

| Brand | Personal voice | Company voice |
|-------|:--------------:|:-------------:|
| brian | ✅ (primary) | ✅ |
| house-of-fraud | ✅ | ✅ (primary) |
| safeguard | ✅ | ✅ |
| sayso | 🚫 NEVER | ✅ only |

**SaySo has no personal voice.** There is no founder voice for SaySo content. All SaySo content is brand/company attribution. If a personal post is needed from someone at SaySo → route to `brian` personal LinkedIn instead.

---

## Routing rules per brand

### brian
- Primary channel: personal-linkedin (most frequent, personal voice)
- Blog: blocked (brian's long-form goes to newsletter or LinkedIn articles)
- All other channels: open
- Voice note: personal voice is the core. Company voice only for company-page content.

### house-of-fraud
- All channels open
- Primary voice: company for all brand channels; personal available for thought leadership
- Newsletter is flagship content — highest quality bar

### safeguard
- All channels open
- Context: B2B practitioner insurance product — voice is professional, outcome-focused
- Email sequences and sales assets are high priority

### sayso ⚠
**Hard restrictions (never override):**
- 🚫 Personal LinkedIn — not an active channel
- 🚫 Newsletter — SaySo has no email newsletter
- 🚫 Blog — no standalone blog; long-form goes to X threads or LinkedIn articles
- 🚫 Email sequences — no email marketing
- 🚫 Sales assets — not managed through this engine for SaySo
- 🚫 Personal voice — no personal/founder voice for SaySo brand channels

**Active channels:**
- ✅ X (Twitter) — primary, 1–3x/day when active
- ✅ Company LinkedIn — 2–3x/week, outcome-focused brand voice

---

## Routing decision tree

When routing any content proposal:

```
1. What brand does this belong to?
   → Check config/settings.yaml brands section

2. Is the proposed format in active_channels for that brand?
   → If not → BLOCKED. Log in ERRORS.md. Do not generate.

3. Is the proposed voice profile available for that brand?
   → If personal voice for SaySo → BLOCKED. Route to brian personal instead.

4. Does the brand have the required brand context files?
   → brand/[brand]/voice-[profile].md
   → brand/[brand]/channel-notes/[channel].md
   → If missing → BLOCKED. Run /new-brand [brand] first.

5. Is the channel currently within cadence limits?
   → Check config/cadence.yaml + performance/cadence-log.yaml
   → If over limit → DEFER. Log in scan report deferred section.

6. CLEAR → proceed to generation.
```

---

## Error responses

When a routing block is hit:

| Situation | Response |
|-----------|----------|
| Newsletter for SaySo | "⚠ Newsletter is not an active channel for SaySo. Redirecting insight to X thread if applicable." |
| Personal LinkedIn for SaySo | "⚠ SaySo has no personal voice. If this is a founder perspective, route to brian personal LinkedIn." |
| Blog for brian | "⚠ Blog is blocked for brian. If this is long-form, use newsletter or LinkedIn article format." |
| Missing brand context | "⚠ Brand context missing for [brand]. Run /new-brand [brand] before generating." |
| Cadence over limit | "⚠ [Format] was generated [n] days ago for [brand] (min gap: [n] days). Defer or override." |

All routing blocks are logged to `knowledge/ERRORS.md` automatically.

---

## SaySo special handling — detailed

SaySo is the most restricted brand. When processing any SaySo input:

**Before generating anything:**
1. Read `brand/sayso/channel-notes/CHANNEL_RESTRICTIONS.md`
2. Confirm: proposed format ∈ {twitter, company-linkedin}
3. Confirm: voice = company (never personal)
4. If any other format is requested → log the block, redirect or skip

**When a blocked format is requested:**
→ Check if the core insight can be adapted to X or company-linkedin
→ If yes: propose the adaptation
→ If no: skip and note "SaySo: insight doesn't adapt to active channels — skipping"

**Content calendar for SaySo:**
- X/Twitter: 1–3 posts/day when inputs exist
- Company LinkedIn: 2–3 posts/week
- Never more than 3 X posts/day (noise prevention)

---

## Multi-brand content (same insight, multiple brands)

When a single input could serve multiple brands:

1. Generate separate brand-specific angles — never cross-contaminate voice
2. Each piece must independently pass quality assessment
3. SaySo version must be re-routed to company-voice X/LinkedIn regardless of the other brand's format

Example:
- Input: "Fraud AI benchmark data"
- brian → personal LinkedIn, personal voice, "what this means for how I evaluate vendors"
- house-of-fraud → newsletter, company voice, "what the benchmark means for fraud teams"
- sayso → X thread, company voice, brand-specific angle from SaySo's ICP lens
