# ERRORS.md — Drift Log & Issue Tracker

**Read this file second, after INDEX.md, before every generation run.**

This file is the engine's memory for what has gone wrong. Every drift, every routing block, every failed quality assessment, every proposed system fix lives here. It is how the engine learns from its own mistakes.

Auto-updated by: morning-content-scan, process-inspiration, quality-assessor, synthesize-learnings, multi-brand-router
Manually add: any pattern you notice that keeps recurring

---

## Format

```
[DATE] [STATUS] [CATEGORY] — Description
  → What happened
  → Proposed fix (if any)
  → Resolved: [date] — [what was changed]
```

**Status tags:** `[OPEN]` | `[RESOLVED]` | `[PATTERN]` | `[PROPOSED FIX]`

**Categories:** `VOICE_DRIFT` | `CHANNEL_BLOCK` | `QUALITY_FAIL` | `ROUTING_ERROR` | `CADENCE_VIOLATION` | `SYSTEM` | `BRAND_CONTEXT`

---

## Open Issues

*No open issues at engine initialization. Issues will be logged here as the engine runs.*

---

## Resolved Issues

*No resolved issues yet.*

---

## Recurring Patterns

*Patterns are logged here when the same issue appears 2+ times. They trigger a system-level fix proposal.*

---

## System Fix Proposals

*Proposed changes to CLAUDE.md, voice profiles, cadence rules, or config based on error patterns.*

---

## How to use this file

### As a user
When content doesn't sound right, or a generation run produced something off-brand:
1. Note the specific issue here under Open Issues
2. Include the draft filename and what was wrong
3. Run `/calibrate-voice` to address the root cause

### As the engine (automatic)
Every skill logs errors here in its Compound phase:

**Morning scan:** Logs every SaySo channel block, every cadence violation flagged, every input that was ambiguously routed.

**Quality assessor:** Logs every draft that scored < 7, every anti-ai-scanner violation found, every adversarial reviewer flag.

**Process inspiration:** Logs duplicate angle detections, ambiguous brand routing decisions, ideas archived without queuing.

**Synthesize learnings:** Resolves errors that have been addressed, promotes patterns to system fix proposals.

### Promotion rules
- Same error appears 2x → promoted to `[PATTERN]`
- Pattern appears 3x → triggers `[PROPOSED FIX]`
- Fix implemented → status changes to `[RESOLVED: date]`

---

## Quarterly cleanup

At the end of each quarter:
1. Archive all `[RESOLVED]` entries older than 90 days to `archive/YYYY-MM/errors-resolved-[quarter].md`
2. Review all `[PATTERN]` entries — have the system fixes been implemented?
3. Update `[PROPOSED FIX]` entries that have been waiting more than 30 days

---

## Error quick-reference (most common)

These are the error types you'll see most often. Knowing them speeds up triage:

**VOICE_DRIFT:** Generated content doesn't sound like the brand/person. Usually caused by loading wrong voice profile, missing gotchas layer, or insufficient few-shot examples. Fix: `/calibrate-voice`.

**CHANNEL_BLOCK (SaySo):** Something was proposed for a blocked SaySo channel. Usually a routing error. Fix: check multi-brand-router skill, update routing in process-inspiration or morning-scan.

**QUALITY_FAIL:** Draft scored < 7. Usually too generic, weak hook, or banned patterns. Fix: quality-assessor rewrite protocol.

**ROUTING_ERROR:** Input was assigned to wrong brand. Usually happens when brand isn't stated in input frontmatter. Fix: add `client:` field to input files.

**CADENCE_VIOLATION:** Format was proposed too soon after last generation. Fix: check cadence-log, adjust cadence.yaml if the rule is wrong.

**BRAND_CONTEXT:** Voice file, channel notes, or examples folder missing for a brand. Fix: `/new-brand [brand]` or populate the missing file.
