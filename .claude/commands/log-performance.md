# /log-performance
# Log real-world performance data for a published piece.
#
# Run this whenever you check your analytics and want to capture what you saw.
# You don't need exact numbers — rough signals are enough.
# The point is to feed the engine's learning loop over time.
#
# Usage: /log-performance
# Optional: /log-performance [content-filename] to pre-select a piece

---

## Step 1: Identify the piece

If a filename was passed as argument, use that.

Otherwise, list the 10 most recently published pieces from:
- `output/[client]/` (sorted by date, status = published)
- `performance/tracker.yaml` entries without a `performance_signal`

Ask the user which piece they're logging performance for.
Present options as a numbered list.

---

## Step 2: Collect performance data

Ask these questions, one at a time (not all at once):

**1. Performance signal**
"How did this perform overall?"
Options:
- `high` — well above what you normally see
- `medium` — about average for this channel
- `low` — below average
- `none` — no notable response
- `too early` — just published, not ready to evaluate

**2. What you actually saw** (skip if signal is "too early")
"What did you see? (rough numbers are fine — or just describe it)"
Accept free text. Examples:
- "300 likes, 40 comments, 5 DMs"
- "Way more shares than usual, a few leads reached out"
- "Nothing. Crickets."
- "One comment from a potential client — that's worth more than 1000 likes"

**3. What worked** (skip if signal is low/none)
"What do you think worked about this piece? Be specific."
Accept free text.
Prompt if blank: "Was it the angle? The opening? The format? The timing?"

**4. What didn't work** (ask regardless of signal)
"Anything you'd do differently?"
Accept free text. Optional — user can say "nothing" or skip.

**5. Would you repeat this?**
"Would you write another piece in this same style/angle?"
Yes / No / Maybe

**6. Notes** (optional)
"Anything else worth recording? (leads generated, specific responses, unexpected reaction)"

---

## Step 3: Write the entry to tracker.yaml

Add a new entry to `performance/tracker.yaml`:

```yaml
- id: [existing content object id from the file's frontmatter]
  client: [client]
  date_published: [from content object]
  date_logged: [today's date]
  format: [from content object]
  voice_profile: [from content object]
  pillar: [from content object]
  title: [from content object title]
  performance_signal: [from step 2]
  engagement:
    raw: "[free text from step 2]"
  what_worked: "[from step 3]"
  what_didnt: "[from step 4 — or null]"
  would_repeat: [true/false/maybe]
  notes: "[from step 6 — or null]"
```

---

## Step 4: Check if a learning synthesis is due

Count entries in tracker.yaml without a `synthesized: true` flag.

If there are 5 or more unanalyzed entries:
→ Say: "You have [n] entries that haven't been synthesized yet. Run /synthesize-learnings to update your performance insights."

---

## Step 5: Confirm

Output:
"Logged. [piece title] — [performance signal].

[If signal was high]: This is a strong data point. The angle/format is worth repeating.
[If signal was none/low]: Good to know. The engine will weight against this angle/format.

Your tracker now has [total] entries."
