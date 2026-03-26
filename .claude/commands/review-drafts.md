# /review-drafts
# Structured review session for everything currently in drafts/.
# Run this to systematically clear the drafts queue.
# Can be run by an editor (moves pieces to 'review') or by the founder (moves to 'approved').
#
# Usage: /review-drafts
# Optional: /review-drafts --client=[name] --channel=[channel] --reviewer=[editor|founder]

---

## Step 1: Load context

Load:
1. `QUALITY_GATE.md` — scoring rubric (you're re-checking the engine's score)
2. `anti-ai-rules.md` — NEVER/ALWAYS card for quick re-scan
3. `brand/[client]/voice-personal.md` and `voice-company.md` — to check voice accuracy
4. `brand/[client]/examples/personal/` and `examples/company/` — reference for voice comparison
5. `config/settings.yaml` — active client

---

## Step 2: Inventory the drafts queue

Scan `drafts/[client]/` for all files with `status: draft` or `status: review`.

Group by:
- Channel (personal-linkedin, company-linkedin, newsletter, blog, etc.)
- Age (days since created)
- Quality score (from frontmatter)

Present an inventory:

```
DRAFTS QUEUE — [client] — [date]

Personal LinkedIn: [n] pieces
  - [filename] — quality: [score] — [n] days old
  - [filename] — quality: [score] — [n] days old

Newsletter: [n] pieces
  - [filename] — quality: [score] — [n] days old

[etc.]

Total: [n] pieces waiting for review
Oldest draft: [n] days old
```

Flag any pieces older than 14 days: "⚠ These pieces are aging — consider archiving if no longer relevant."

---

## Step 3: Determine reviewer role

Ask: "Are you reviewing as the editor (moves to 'review') or as the founder (moves to 'approved')?"

- **Editor:** Checks quality gate, voice accuracy, and basic sanity. Moves clean pieces to `review`.
- **Founder:** Reads for "would I post this?" Makes the call. Moves to `approved` or `archived`.

If a founder is reviewing, skip the mechanical quality re-check (editor already did it) and go straight to the "would I post this?" test.

---

## Step 4: Review each piece

Present pieces one at a time, ordered by:
1. Channel priority (personal LinkedIn first, then company LinkedIn, then newsletter, etc.)
2. Age (oldest first within channel)

For each piece, show:
- The full content body (no frontmatter)
- Current quality score and notes from frontmatter
- Channel it's for

**If reviewing as editor, ask:**
"Does this pass? (yes / fix / archive)"

- **yes** → change `status: draft` to `status: review` in frontmatter
- **fix** → identify the specific issue. Options:
  - Re-run anti-AI scrub → fix mechanical issues → re-score
  - Voice drift → reload voice profile → revise the problematic section → re-score
  - Specificity fail → add one concrete detail from the source input → re-score
- **archive** → move file to `archive/content/[client]/[channel]/` → rename with `_ARCHIVED_[date]` suffix

**If reviewing as founder, ask:**
"Would you post this exactly as written? (yes / tweak / no)"

- **yes** → change `status: review` to `status: approved`
- **tweak** → founder reads, makes the specific edits themselves or describes them → engine makes the change → re-present → re-confirm
- **no** → ask "What's wrong with it?" → note the issue in voice-calibration-log.md → move to archive

---

## Step 5: Handle stale drafts

For any draft flagged as older than 14 days:

"This draft is [n] days old. Is the topic still timely and relevant?"

- **Yes** → continue reviewing normally
- **No** → archive immediately, log the reason: "Topic no longer timely as of [date]"

For any draft older than 30 days with no action taken:
"This draft is [n] days old and hasn't been reviewed. Recommend archiving — the topic has likely passed."

---

## Step 6: End-of-session report

After reviewing all pieces:

```
REVIEW COMPLETE — [date]

Reviewed: [n] pieces
  → Approved: [n]
  → Moved to review: [n]
  → Fixed and re-scored: [n]
  → Archived: [n]
  → Still in draft (needs attention): [n]

Approved pieces ready to publish:
  - [filename] — run /publish [filename] when ready
  - [filename]

Notes for next generation:
[Any patterns from review that suggest voice calibration or strategy changes]
```

---

## Step 7: Voice calibration trigger

If 3 or more pieces were archived or sent back for voice issues:

"[n] pieces had voice problems. This pattern suggests a calibration session is needed.
Run `/calibrate-voice` to update the voice profile with what you're catching in review."
