# /calibrate-voice
# Structured voice calibration session.
#
# Run this when:
# - Generated content keeps missing your voice
# - You've published 10+ pieces and want to update the voice profile
# - Something about your writing style has changed
# - You're onboarding a new client and want to build voice profiles from examples
#
# Usage: /calibrate-voice
# Optional: /calibrate-voice --personal | --company | --channel=[channel-name]

---

## Step 1: Determine calibration scope

Ask: "What are we calibrating?"
Options:
1. Personal voice (how you sound as an individual)
2. Company voice (how the brand sounds)
3. A specific channel (LinkedIn, newsletter, Twitter, blog)
4. All of the above — full calibration session

---

## Step 2A: Calibration via generated content review (if pieces exist)

If the client has published content in `output/[client]/`:

"Let's look at 5 pieces that were recently generated. For each one, I'll ask you two things:
1. Does this sound like you? (yes / close / not really / no)
2. What specifically is off — or what specifically nails it?"

Load the 5 most recent pieces for the selected scope.
Present each piece body (no frontmatter) one at a time.
For each:
- Show the piece
- Ask the two questions
- On "not really" or "no" — ask: "What would you have written instead?"
- On "close" — ask: "What's the thing that almost works but doesn't?"

Record all feedback in structured notes.

---

## Step 2B: Calibration via example ingestion (if few pieces exist or for new clients)

If fewer than 5 generated pieces exist for this client:

"Let's train the engine on examples you provide. Paste 3-5 pieces of your actual writing — LinkedIn posts, emails, anything that sounds like you."

For each example pasted:
- Identify: voice profile (personal / company), channel, approximate date
- Extract: sentence rhythm, vocabulary choices, opening style, closing style
- Note: anything unusual or distinctive about this piece

After all examples are analyzed:
Present a voice profile summary:
"Based on these examples, here's what I'm picking up about your voice..."
[List specific observations, not generic descriptors]

Ask: "What's right? What's wrong? What did I miss?"

---

## Step 3: Identify specific corrections

Based on the calibration session, compile a corrections list:

```
VOICE CORRECTIONS — [date]

Things to do differently:
1. [Specific change — e.g., "Don't use em-dashes as a structural element"]
2. [Specific change]
3. [Specific change]

Things to keep doing:
1. [Specific keeper — e.g., "The conversational 'you know what I mean?' style is right"]
2. [Specific keeper]

Phrases that are dead wrong for this voice:
- "[example]"
- "[example]"

Phrases that are spot-on:
- "[example]"
- "[example]"
```

---

## Step 4: Update the voice profiles

Ask: "Should I update your voice profiles with these corrections? (yes / show me first)"

If yes:
- Apply corrections to `brand/[client]/voice-personal.md` and/or `voice-company.md`
- Apply channel-specific corrections to relevant `channel-notes/` file
- Add a calibration session log entry to `learning/voice-calibration-log.md`

Present a diff of what changed before writing.

---

## Step 5: Test the calibration

Optional — ask: "Want to test the new calibration with a quick generation?"

If yes:
- Ask for a topic or angle (one sentence)
- Generate a short piece (LinkedIn post) using the just-updated voice profile
- Present it and ask: "Better?"

If not better → repeat Step 2-4 on the specific issue
If better → confirm and close the session

---

## Step 6: Close

Output:
"Voice calibration complete.

**Changes made:**
- [File]: [what changed]
- [File]: [what changed]

**Calibration logged:** `learning/voice-calibration-log.md`

The engine will use these updated profiles in all future generation.
Next step: run /morning-scan or /generate-campaign to see the difference."
