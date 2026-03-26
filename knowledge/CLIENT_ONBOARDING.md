# Client Onboarding Guide
# Use this when setting up the Content Engine for a new client.
# Follow it in order. Skipping steps produces worse outputs.

---

## Before you start

Answer these questions before touching any files:

1. **Personal, company, or both?**
   - Personal only → build `voice-personal.md` + personal channel notes
   - Company only → build `voice-company.md` + company channel notes
   - Both → build both, treat them as separate voices with a shared context

2. **Which channels are active?**
   - Personal LinkedIn? Company LinkedIn? Newsletter? Twitter? Blog?
   - Only build channel notes for channels they actually use
   - Don't set up Twitter for a client who isn't on Twitter

3. **What's their realistic publishing frequency?**
   - Be honest here. "Daily LinkedIn" sounds good but most clients can't sustain it
   - Set `config/cadence.yaml` caps to what they'll actually maintain
   - Under-promise on frequency, over-deliver on quality

4. **Do they have existing content you can use as examples?**
   - Best posts, best emails, any writing they've done that felt right
   - These are critical. Without examples the voice profile is a guess.

5. **What are the off-limits topics?**
   - Competitors they don't name, clients they don't reference, personal topics they keep private
   - Better to get this upfront than generate something they can't publish

---

## Step 1: Create the client folder

```bash
cd ~/Desktop/ContentEngine
cp -r brand/_template brand/[client-name]
```

Then create the examples directories:
```bash
mkdir -p brand/[client-name]/examples/personal
mkdir -p brand/[client-name]/examples/company
```

---

## Step 2: Run the brand setup command

In Claude Code (from the ContentEngine directory):
```
/new-brand [client-name]
```

This walks through every brand file interactively. Complete all sections — don't leave placeholders. The engine treats empty sections as missing context and defaults to generic output.

---

## Step 3: Fill in voice profiles (the most important step)

Open `brand/[client-name]/voice-personal.md` and fill in every section. Don't write generic descriptors.

**Bad voice profile:**
> "Authentic, conversational, uses humor occasionally. Likes to share insights. Writes in a clear, approachable way."

**Good voice profile:**
> "Opens with a failure or a number — never a question. Uses 'I' heavily and doesn't hedge opinions with 'I think' or 'in my view.' Short sentences after long ones. Never ends a LinkedIn post with a question. Comfortable naming specific clients and amounts when they've given permission. Humor is dry, never self-deprecating."

The more specific the voice profile, the less post-generation editing is required.

---

## Step 4: Load examples — this is not optional

**Minimum:** 2 examples per voice profile. **Ideal:** 3–5.

Examples go in:
- `brand/[client-name]/examples/personal/` — their actual best personal posts/emails
- `brand/[client-name]/examples/company/` — their actual best company content

Name them descriptively:
- `linkedin-failure-story-2025.md`
- `newsletter-client-win-jan2026.md`

Format: paste the full text in a `.md` file. No frontmatter needed. Just the content.

**Why examples matter more than voice profiles:**
A voice profile describes the voice in words. Examples show it. The generator loads both — but when they conflict, examples win. A great example is worth 10 adjectives in a voice profile.

---

## Step 5: Fill in channel notes

Open each relevant file in `brand/[client-name]/channel-notes/` and complete it.

Minimum to complete for each active channel:
- Post length range (their actual range from examples, not a generic recommendation)
- Hook style (what their actual best openers look like)
- What they never do on this channel
- 1–2 priority examples to load (filenames from their examples folder)

For newsletter: also complete the structure section (recurring sections, send day, what makes readers reply).

---

## Step 6: Set active client and test

In `config/settings.yaml`:
```yaml
active_client: [client-name]
```

Then run a test generation:
```
/generate-campaign inputs/briefs/_template-campaign-brief.yaml
```

Review the manifest and approve one piece. Read the output and ask:
- Does this sound like them?
- Would they post this without editing?

If yes → you're set. If no → go back to voice profiles and examples. Add specificity.

---

## Step 7: Calibration session (first week)

After the first 3–5 real generations, run:
```
/calibrate-voice
```

This structured review session catches what the initial setup missed. It's normal that the first outputs need adjustment — the calibration session locks in those corrections so they don't repeat.

Expect to run 2–3 calibration sessions in the first month. By month 2, outputs should need minimal editing.

---

## Step 8: Set up performance tracking

Explain the loop to the client:
1. Every time they check their analytics, log it: `/log-performance`
2. After 5+ entries, synthesize: `/synthesize-learnings`
3. The engine adjusts future generation based on what's actually working for their audience

This is the difference between an engine that gets better and one that stays generic.

---

## Step 9: Configure publishing (optional)

If the client wants Notion integration:
- Create a Notion integration and share their content database
- Add the database ID to `config/settings.yaml`
- Test with: `/publish [output-file]`

If the client wants Airtable content calendar:
- Set up the Airtable base with the required columns
- Configure `config/settings.yaml` field mapping
- Test with a publish run

---

## Ongoing client management

**Monthly:** Run `/update-company-context` when the client reports business changes.

**After every analytics check:** Encourage `/log-performance` — even rough signals help.

**When outputs start drifting:** Run `/calibrate-voice` — voice drift happens as the business evolves and the profile doesn't.

**When switching to a new campaign focus:** Update `brand/[client-name]/pillars.md` and run `/update-company-context`.

---

## Client handoff checklist

If handing this engine off to a client to run themselves:

- [ ] Voice profiles complete and verified with calibration session
- [ ] Channel notes complete for all active channels
- [ ] 3+ examples in each examples folder
- [ ] `config/settings.yaml` active_client set to their name
- [ ] `config/.env` has their API keys
- [ ] They understand the three commands they'll use daily: `/morning-scan`, `/generate-campaign`, `/log-performance`
- [ ] They know to run `/calibrate-voice` when something feels off
- [ ] They know to run `/update-company-context` when the business changes
- [ ] Walkthrough session completed: showed them a full generation run live

---

## Common setup mistakes

**Mistake 1: Generic voice profiles**
Symptom: outputs sound like every other AI content.
Fix: add specificity to the voice profile. Pull real phrases from examples.

**Mistake 2: No examples loaded**
Symptom: outputs sound technically correct but tonally wrong.
Fix: add 3+ examples per voice profile. This is the fastest fix.

**Mistake 3: Wrong active client**
Symptom: generated content has the wrong voice, wrong pillars, wrong audience.
Fix: check `config/settings.yaml` — confirm `active_client` is set correctly.

**Mistake 4: Skipping calibration**
Symptom: the same problems keep appearing in generated content.
Fix: run `/calibrate-voice`. The session corrects what setup missed.

**Mistake 5: Not logging performance**
Symptom: the engine keeps making the same structural choices even when they're not working.
Fix: log performance after every 3–4 published pieces. Give it data to learn from.
