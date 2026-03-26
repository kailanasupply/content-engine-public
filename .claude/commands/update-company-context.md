# /update-company-context
# Update the company evolution log when the business changes.
#
# Run this when:
# - Positioning shifts
# - New offer launches or old one is retired
# - ICP evolves
# - You've heard a new objection 5+ times and need to update messaging
# - The story you're telling has changed
# - Significant win or loss that changes the narrative
#
# Usage: /update-company-context
# Optional: /update-company-context --client=[name]

---

## Step 1: Load current context

Load:
- `learning/company-evolution.md` — current state
- `brand/[client]/voice-company.md` — brand character and messaging
- `brand/[client]/messaging.md` — current positioning

---

## Step 2: Ask what changed

"What's changed? You can describe it in plain language — I'll figure out where it goes."

Accept free-form input. The user might say:
- "We stopped doing social media management"
- "We just landed our biggest client ever — a Fortune 500"
- "Three prospects this week said the same objection: too expensive for what you do"
- "We're repositioning from X to Y"
- "Our ICP has shifted — we're not going after SMBs anymore, we're going enterprise"

---

## Step 3: Classify the change

Determine what kind of change this is:
- **Offer change** → update "What we're selling right now" in company-evolution.md
- **Positioning change** → update "Who we are right now" + "What story we're telling"
- **ICP change** → update "Who we serve right now"
- **Messaging signal** (objection, confusion, resonance) → add to "Messaging signals from the field"
- **Off-limits change** → update "What we're NOT talking about right now"
- **Multiple** → update all relevant sections

---

## Step 4: Check content implications

Based on the change, identify any current-state content that may now be out of date:

- Does this change affect the brand's messaging.md positioning statement?
- Does this change affect any pillar focus areas in pillars.md?
- Does this change mean any recent content should be archived or updated?
- Does this change create new content opportunities?

---

## Step 5: Update files

Update `learning/company-evolution.md`:
- Add a dated change log entry
- Update the "Current state" section to reflect the new reality

If the change is significant enough:
- Flag updates needed in `brand/[client]/messaging.md`
- Flag updates needed in `brand/[client]/pillars.md`
- Ask: "Should I update your messaging.md and pillars.md too?"

---

## Step 6: Confirm

Output:
"Company context updated.

**What changed:**
[Summary of the change]

**What this means for content:**
[Specific implication — e.g., 'Stop writing about X. Lead with Y instead.']

**Files updated:**
- learning/company-evolution.md

**Files that may need review:**
- [List if any were flagged]

The engine will reflect this context in the next morning scan."
