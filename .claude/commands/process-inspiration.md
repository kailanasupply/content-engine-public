# /process-inspiration
# Reads everything in inputs/inspiration/ and routes ideas to the correct brands.
# Extracts the content angle from each item, assigns it to a brand, proposes formats.
# Never auto-generates — produces proposals for the next morning scan or manual approval.
#
# Usage: /process-inspiration
# Optional: /process-inspiration --brand=[name] to process inspiration for one brand only

---

## Step 1: Load context

**⚠ Load these FIRST:**
1. `knowledge/INDEX.md` — master router and active brand list
2. `knowledge/ERRORS.md` — check for open routing errors
3. `skills/process-inspiration.md` — full processing logic. Follow that skill's loop.

Then load:
4. `anti-ai-rules.md`
5. `QUALITY_GATE.md`
6. `config/settings.yaml` — all registered brands and their channel restrictions
7. `config/cadence.yaml` — brand-specific channel rules (especially blocked channels for sayso)
8. For each active brand: `brand/[brand]/pillars.md` and `brand/[brand]/personas.yaml`

---

## Step 2: Scan the inspiration folder

Scan `inputs/inspiration/` for any files NOT in `inputs/inspiration/processed/`.

Supported types:
- `.md` / `.txt` — text notes, pasted post content, ideas
- `.png` / `.jpg` — screenshots (read the visual content)
- `.yaml` / `.json` — structured idea notes
- Any file with text content

For each file, extract:
1. **Type:** liked post | quick idea | client question | competitor content | news/data | voice memo | other
2. **Core content:** What is the actual idea or observation?
3. **Source signal:** If it's a liked post — what made it worth noting? (the angle, the structure, the hook, the topic?)
4. **Applicable brands:** Which of the 4 brands (brian / safeguard / house-of-fraud / sayso) could this idea serve?
5. **Content angle:** What is the specific content angle this could become?

---

## Step 3: Route to brands

For each inspiration item, determine which brand(s) it belongs to:

**Routing logic:**
- If the idea is about Brian's personal experience → route to `brian` (personal voice)
- If the idea is about fraud/security industry topics → route to `house-of-fraud` or `safeguard`
- If the idea is about SaySo's category or ICP → route to `sayso` (Twitter/LinkedIn only)
- If ambiguous → route to `brian` by default and flag for clarification
- If the idea clearly belongs to multiple brands → duplicate the routing, with different angles per brand

**SaySo restriction check:**
Before routing any item to SaySo, confirm the proposed format is X (Twitter) or Company LinkedIn.
If the best format would be a newsletter or blog → route to a different brand or skip SaySo routing.

---

## Step 4: Propose content formats

For each routed item, propose 1–3 specific content pieces:

```
INSPIRATION ITEM: [filename]
Type: [liked post / quick idea / etc.]
Core insight: [one sentence]

→ BRAND: brian
   Format: personal-linkedin
   Angle: "[Specific angle — not 'a post about X' but the actual take]"
   Why this works: [one sentence]
   Hook draft: "[One-sentence hook attempt]"

→ BRAND: sayso (if applicable and not blocked)
   Format: twitter
   Angle: "[Company-voice angle on the same insight]"
   Why this works: [one sentence]
```

---

## Step 5: Apply the noise test

Before adding any proposal to the queue, check:
- Has this topic been covered in the last 30 days for this brand? (check `performance/tracker.yaml`)
- Is the proposed angle genuinely different from recent content on this topic?
- Does the angle have a clear content reason (insight / opinion / story / announcement / education / proof)?

If it's a duplicate angle → flag it: "Similar to [previous piece] — consider differentiating or skipping."
If it fails the content reason test → hold it, don't propose.

---

## Step 6: Present the inspiration report

Output a structured report:

```
INSPIRATION PROCESSING COMPLETE — [date]
Items found: [n]
Items routed: [n]
Items skipped (noise/duplicate): [n]

---

PROPOSALS FOR NEXT SCAN:

BRIAN — [n] proposals
  1. [Format] — "[Angle]" — Source: [filename]
     Hook: "[draft hook]"
  2. ...

SAFEGUARD — [n] proposals
  ...

HOUSE OF FRAUD — [n] proposals
  ...

SAYSO (X + LinkedIn only) — [n] proposals
  ...

---

SKIPPED:
  - [filename]: [reason]
```

---

## Step 7: Queue approved proposals

Ask: "Add these to tomorrow's morning scan queue? (yes / select / no)"

- **yes** → write approved proposals to `inputs/processed/inspiration-queue-[date].yaml` for the morning scan to pick up
- **select** → show numbered list, user picks which ones to queue
- **no** → save proposals to `inputs/inspiration/processed/[filename]-proposals.md` for reference, don't queue

---

## Step 8: Move processed files

Move all processed inspiration files to `inputs/inspiration/processed/`:
- Rename: `[original-filename]_PROCESSED_[date].[ext]`
- This prevents re-processing in future runs

Leave `inputs/inspiration/README.md` and any unprocessed files in place.
