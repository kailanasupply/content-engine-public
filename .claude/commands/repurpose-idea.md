# /repurpose-idea [path-or-keyword]
# Takes an archived idea and generates new drafts using current voice, templates, and cadence.
# Works with a file path OR a keyword search across the archive.
#
# Usage:
#   /repurpose-idea archive/evergreen-candidates/2026-02-14-fraud-trust-analogy-[EVERGREEN].md
#   /repurpose-idea trust
#   /repurpose-idea 2026-01

---

## Step 1: Locate the source idea

**If a file path was provided:**
- Read the file at the given path directly.
- If the file doesn't exist, report: "File not found: [path]. Check `archive/` for the correct path."

**If a keyword was provided:**
- Search `archive/` recursively for files whose names or content contain the keyword.
- Show a numbered list of matches (up to 10):
  ```
  Found [n] matches for "[keyword]":
  1. archive/evergreen-candidates/2026-02-14-fraud-trust-[EVERGREEN].md
  2. archive/2026-01/2026-01-20-fraud-stats-post.md
  3. ...
  ```
- Ask: "Which one? (enter number, or 'all' to repurpose all matches)"
- Wait for response. Do not proceed until the user selects.

---

## Step 2: Load context

Before generating anything, load in this order:

1. `anti-ai-rules.md`
2. `QUALITY_GATE.md`
3. `config/settings.yaml` — get `active_client` and its `active_channels` / `blocked_channels`
4. `config/cadence.yaml` — check what formats are eligible today for the active client
5. `brand/[active_client]/voice-personal.md` (if personal voice is available for this client)
6. `brand/[active_client]/voice-company.md` (if company voice is available for this client)
7. `brand/[active_client]/pillars.md`
8. `brand/[active_client]/personas.yaml`
9. `brand/[active_client]/channel-notes/` — load relevant channel notes based on eligible formats
10. `brand/[active_client]/examples/personal/` and `/company/` — load 1 example per relevant voice
11. `performance/tracker.yaml` — check what topics have been covered in the last 30 days
12. `performance/insights.md` — load any structural guidance

---

## Step 3: Extract the core idea

Read the archived file and extract:

1. **Original type:** liked post | quick idea | client question | competitor content | news/data | voice memo | other
2. **Core insight:** What is the original observation or idea? (one sentence — be specific)
3. **Original source signal:** What made it worth saving? The hook angle? The topic? The structure?
4. **Evergreen themes present:** Dad-life / fraud / building / trust / leadership / other
5. **Original date:** Pull from filename prefix

Report this summary before proposing angles:
```
SOURCE IDEA SUMMARY
File: [filename]
Archived: [date from filename]
Core insight: [one sentence]
Original type: [type]
Themes: [list]
```

---

## Step 4: Apply the freshness test

Before proposing anything, check `performance/tracker.yaml`:
- Has this topic been published in the last 30 days for `[active_client]`?
- If yes: flag it — "Similar topic published [X days ago]. Proposed angles will need clear differentiation."
- If the exact same angle was used: suggest skipping unless the user wants to try a meaningfully different frame.

---

## Step 5: Propose repurpose angles

Generate 2–4 content angles from the core idea, using the current brand context and eligible channels.

**Rules:**
- Each angle must be meaningfully different from the original piece (new hook, new frame, new format)
- Each angle must map to an eligible channel for `[active_client]` (check `active_channels` and `blocked_channels`)
- Each angle must pass the cadence check (format eligible today?)
- No angle may blend voice profiles (personal vs. company stays clean)

**Format for each proposal:**
```
REPURPOSE PROPOSAL [n]
Brand: [active_client]
Format: [channel]
Voice: personal | company
Angle: "[The specific take — not 'a post about X' but the actual POV]"
Why this works now: [one sentence — what's fresh about this vs. the original]
Freshness delta: "[What changed: new frame / new format / new hook]"
Hook draft: "[One-sentence opening attempt]"
Cadence check: [last generated in this format: X days ago — eligible / not eligible]
```

Present all proposals. Ask:
"Which angles should I generate? (enter numbers, 'all', or 'none')"

Wait for user response.

---

## Step 6: Generate approved drafts

For each approved angle:

1. Load the correct voice profile + channel-notes file for the specific format
2. Load 1–2 examples from the matching examples folder as few-shot reference
3. Write the full draft — apply all anti-AI rules, use the specific hook draft as a starting point
4. Run the anti-AI self-check before saving:
   - No banned words
   - No -ing clause openers
   - No vague attribution ("many people", "some say")
   - No blended voices
   - One clear POV, not a list
5. Score against `QUALITY_GATE.md` rubric (0–10)
6. Apply scoring rules: ≥7 → save | 5–6 → flag for human review | <5 → do not save

---

## Step 7: Save drafts

Save each qualifying draft to:
```
drafts/[active_client]/[channel]/[YYYY-MM-DD]_[voice]_[channel]_[slug].md
```

Include in YAML frontmatter:
```yaml
---
id: [uuid]
type: [social | newsletter | blog | email | sales]
subtype: [channel]
voice_profile: personal | company
title: [draft title]
client: [active_client]
repurposed_from: [original archive file path]
repurpose_date: [today YYYY-MM-DD]
original_archive_date: [date from original filename]
pillar: [relevant pillar]
persona: [target persona]
platform: [platform]
status: draft
quality_score: [n]
quality_notes: [specific note for reviewer]
created: [ISO timestamp]
word_count: [n]
---
```

---

## Step 8: Report completion

```
REPURPOSE RUN COMPLETE — [date]
Source idea: [filename]
Core insight: [one sentence]
Active brand: [active_client]

Drafts generated: [n]
  ✅ [channel] — "[angle]" — Score: [n]/10 → saved to drafts/[path]
  ✅ [channel] — "[angle]" — Score: [n]/10 → saved to drafts/[path]
  ⚠ [channel] — "[angle]" — Score: [n]/10 → flagged for review

Drafts flagged (score 5–6): [n]
Drafts not saved (score <5): [n]

Next: Run /review-drafts to approve or edit before publishing.
```
