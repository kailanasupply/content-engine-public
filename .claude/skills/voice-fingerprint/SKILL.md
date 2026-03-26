---
name: voice-fingerprint
description: Load layered voice context for a specific client before generating or reviewing content. Use this skill any time you are about to write a draft, check a draft's voice accuracy, or calibrate content to sound like a specific person or brand. Trigger on: "write a post for Brian", "does this sound like Brian", "generate HOF content", "check this against Brian's voice", "voice fingerprint", "load voice context", or any generation request where a specific client's voice must be matched. This skill should be loaded BEFORE any draft is written — not after. If you're generating personal LinkedIn content, a newsletter, or any content written AS a specific person, load this skill first.
---

# Voice Fingerprint

Layered voice context per client. Load the right layers at the right time. Do not load everything at once.

---

## Why this exists

`voice-personal.md` and `voice-company.md` hold comprehensive profiles, but loading them as monolithic files creates two problems: (1) everything is equally weighted — the most critical constraints share space with background context, (2) there's no room for the "gotchas" layer — the specific patterns that slip through even when the profile is loaded.

This skill solves both problems. It splits voice context into layers and tells you when to read each one.

---

## Active clients

```
brian/          → Personal voice (LinkedIn, newsletter, ghostwriting)
house-of-fraud/ → HOF company voice (brand blog, company LinkedIn, HOF newsletter)
```

Both clients are currently active. Point at the correct folder based on the voice profile required. See the Voice System table in CLAUDE.md if unsure which to use.

---

## Loading order — follow this exactly

### Layer 1: Core rules (load first, always)
`[client]/core-voice.md`

5 non-negotiable rules that cannot break. Load these before anything else. They override everything in the layers that follow. Short file — read the whole thing.

### Layer 2: Writing mechanics (load before drafting)
`[client]/sentence-rhythm.md`
`[client]/vocabulary.md`

Read both before you write a single sentence. These define how the client writes, not just what they write about. Rhythm shapes the sentence structure. Vocabulary defines the words that feel native vs. the ones that would never appear.

### Layer 3: Opinion architecture (load before drafting opinion-based content)
`[client]/opinion-patterns.md`

How this client states a position. How they hedge (or don't). What directness looks like for them specifically. Load this when the piece takes a stance — which is most of Brian's content and all good HOF content.

### Layer 4: Gotchas (load last — highest recency matters)
`[client]/gotchas.md`

The most important layer. Built from actual voice drift events in generated content — patterns that passed the rules but broke the voice. Load this **immediately before drafting** so it's the freshest thing in context. If you load it too early and layer other context on top, its recency advantage disappears.

### Layer 5: Reference (load on demand only)
`[client]/reference/rhythm-examples.md` — read when uncertain about a specific sentence structure
`[client]/reference/opener-library.md` — read when uncertain whether an opening approach is correct

Do not load these proactively. They're heavy. Load them only when you need a specific reference check — "does this sentence rhythm match Brian's?" or "is this opener type one Brian uses?"

---

## When checking an existing draft against the fingerprint

Load in this order:
1. `core-voice.md` — establish the hard rules
2. `gotchas.md` — the patterns most likely to be present
3. `sentence-rhythm.md` + `vocabulary.md` — for detailed line-level checks

You do not need `opinion-patterns.md` unless the feedback is specifically about how a position is stated.

---

## Adding to this skill over time

When a voice calibration session identifies a new drift pattern:
1. Add it to `[client]/gotchas.md` with the exact ❌ slip and ✅ correction
2. If it's a rhythm issue, add an example pair to `[client]/reference/rhythm-examples.md`
3. If it changes a fundamental rule, update `[client]/core-voice.md`

The gotchas file is the institutional memory of this skill. It gets more valuable with every generation run.

---

## What this skill does NOT replace

- `anti-ai-rules.md` — load that separately. Voice fingerprint is about sounding like the client. Anti-AI rules are about not sounding like a language model. Both apply.
- `anti-ai-scanner` — still runs before saving. Voice accuracy and rule compliance are different checks.
- `adversarial-reviewer` — still runs after. The fingerprint helps you generate better. The adversarial reviewer catches what you still missed.
