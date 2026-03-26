# Team Guide
# For editors, operators, and anyone running the engine who isn't the founder.
# One page. Read this before touching anything.

---

## Your job

You run the engine. The founder approves the outputs. You never publish without their sign-off.

That's the whole job. Everything else is details.

---

## Daily workflow

**Morning (7am — automated)**
The engine runs `/morning-scan` automatically. It produces a scan report — a prioritized list of what to generate today based on yesterday's inputs and cadence rules. It does not generate content automatically.

**Your first task of the day**
1. Read the scan report
2. Send it to the founder with: "Here's today's content plan. Reply GO to generate, or tell me what to change."
3. Wait for their reply

**On GO:**
Open Claude Code in the ContentEngine directory and run:
```
/generate-campaign [the input file from the scan report]
```
Review the manifest that appears. If it matches what the founder approved — type `APPROVE`. Generation runs.

**After generation:**
Drafts land in `drafts/[client]/[channel]/`. Review each piece:
- Does it pass the quality gate? (Read `QUALITY_GATE.md`)
- Does it sound like the founder? (Check against examples in `brand/[client]/examples/`)
- If yes → change `status: draft` to `status: review` in the file's frontmatter
- If no → flag it with a note, do not forward to founder

Send `review` pieces to the founder: "Three pieces ready for your eyes."

**On founder approval:**
They change status to `approved`. You run:
```
/publish drafts/[client]/[channel]/[filename].md
```

Done.

---

## Performance logging (do this weekly)

After the founder checks analytics, ask them two questions:
1. "Which posts this week got the most traction?"
2. "Anything feel off or that you wouldn't post again?"

Log their answers:
```
/log-performance
```

After 5+ entries:
```
/synthesize-learnings
```

Send the synthesis summary to the founder for review.

---

## Commands you'll use

| Command | When |
|---------|------|
| `/generate-campaign [file]` | After founder approves scan report |
| `/process-input [file]` | When input is a recording or long notes file |
| `/review-drafts` | Structured review of everything in drafts/ |
| `/publish [file]` | After founder approves a piece |
| `/log-performance` | After analytics check |
| `/synthesize-learnings` | After 5+ performance entries logged |
| `/generate-weekly-report` | Every Friday |

---

## Rules you must never break

1. **Never publish without `status: approved`** in the file's frontmatter
2. **Never approve a piece yourself** — that's the founder's call
3. **Never run `/calibrate-voice` without the founder present** — they have to answer the questions
4. **Never generate for the wrong client** — confirm `active_client` in `config/settings.yaml` before every run
5. **Never modify voice profiles without a calibration session** — edits without the founder's input break the voice

---

## When something goes wrong

**Content sounds wrong:** Don't publish. Flag it. Run `/calibrate-voice` with the founder.

**Generation fails:** Check `config/.env` — API key may have expired. Check `config/settings.yaml` — active_client must be set.

**Publish fails:** File saves locally. Check `config/publish_errors.log`. Try again. If it keeps failing, post manually and log the URL in the content object's frontmatter.

**Founder changes the plan:** Stop. Don't generate what they didn't approve. Update the manifest, get re-approval, then generate.

---

## Files you should know

| File | What it is |
|------|-----------|
| `config/settings.yaml` | Active client, API config |
| `QUALITY_GATE.md` | Scoring rubric for every piece |
| `brand/[client]/voice-personal.md` | How the founder sounds |
| `brand/[client]/examples/personal/` | Their actual best posts |
| `drafts/[client]/` | Everything waiting for review |
| `performance/tracker.yaml` | Performance log (add data here) |

---

*If you're unsure whether to do something — don't. Ask first.*
