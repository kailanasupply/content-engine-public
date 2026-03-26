# Team Usage Guide
# How to use the Content Engine when more than one person is working with it.

---

## The fundamental problem with team content engines

When one person runs this engine for themselves, feedback loops are tight.
When a team uses it — a founder, an editor, a social media manager — the loops break.

The biggest failure modes:
1. Multiple people generating in parallel and stepping on each other's output
2. No shared understanding of which pieces are approved vs. draft
3. Voice calibration sessions happening without the subject's involvement
4. Performance data logged inconsistently by different people

This guide addresses all four.

---

## Roles and ownership

**The subject** (founder / individual)
- Owns voice profile calibration — only they can say "this sounds like me"
- Approves every manifest before generation runs
- Does the final review of personal-voice content before it publishes
- Logs the performance gut-reads ("did this feel right?" not just numbers)

**The engine operator** (you, or a team member managing the system)
- Runs the morning scan and presents it to the subject
- Processes inputs, generates manifests
- Logs quantitative performance data (likes, comments, etc.)
- Runs synthesize-learnings and reports findings to the subject
- Manages active_client settings when working across multiple clients

**The editor** (if you have one)
- Reviews output/ drafts against the quality gate
- Changes status from `draft` to `review` when a piece is ready for the subject's eyes
- Never changes `review` to `approved` — that's the subject's call

**No one publishes without** `status: approved` in the content object frontmatter.

---

## Workflow for team generation

1. **Engine operator** runs `/morning-scan` and sends the scan report to the subject
2. **Subject** reviews and replies `go`, `edit`, or `skip`
3. **Engine operator** runs generation on approved items
4. **Editor** reviews drafts — marks `status: review` on pieces that pass their read
5. **Subject** reads `review` pieces — marks `status: approved` on pieces they'd post verbatim
6. **Engine operator** runs `/publish` on approved pieces

No step skips the subject's approval. No step.

---

## Conventions for multi-person use

### File naming
Generated files include `voice_profile` in the filename:
`2026-03-15_personal_linkedin_client-story.md`

Never rename these files. The naming convention is how the system tracks what's what.

### Status field (YAML frontmatter)
Every content object has a status field. Honor it:
- `draft` — generated, passed quality gate, not yet human-reviewed
- `review` — editor has read it, ready for subject's approval
- `approved` — subject approved, ready to publish
- `published` — live; do not edit

Only the subject moves a piece from `review` to `approved`.
Only `/publish` moves a piece from `approved` to `published`.

### Who logs performance
- Quantitative data (numbers, engagement stats): engine operator or editor
- Qualitative data (what worked, what felt off, would you repeat it): subject

Both types of data matter. The engine learns more from the qualitative column than from the numbers.

---

## Running this for clients as a service

If you're building and running this engine for paying clients:

### What the client does
- Completes the initial voice profile setup session (required — you can't do this for them)
- Reviews and approves every manifest before generation
- Reviews final drafts before publishing
- Provides performance gut-reads monthly
- Flags when the business is changing via `/update-company-context`

### What you do
- Runs the morning scan and sends the report
- Processes all inputs
- Manages the generation pipeline
- Handles Notion/Airtable integration
- Runs synthesize-learnings and presents findings in a monthly report
- Manages calibration sessions (with client present)

### What to never do for a client
- Never approve a manifest on their behalf — they must see and approve every plan
- Never mark personal-voice content as approved — that's always their call
- Never update the voice profile without a live calibration session with them
- Never change active_client settings without confirming which client you're generating for

---

## Suggested slash command upgrades for team use

These aren't built yet — they're improvements worth adding when you're running this for multiple clients or with a team.

### `/review [file]`
Opens a content object for editorial review. Pre-loads the quality gate, voice profile, and channel notes for that piece. Walks through each level systematically. Changes status to `review` on pass.

Currently: reviewers open files manually and check against quality gate themselves.
Upgrade: makes the review structured and consistent across team members.

### `/status [client]`
Shows current pipeline status for a client: how many pieces are in draft, review, approved, and published. What was last generated and when.

Currently: you'd manually scan the output/ folder.
Upgrade: one command gives you the full picture.

### `/weekly-report [client]`
Generates a weekly summary for a client: what was published, rough performance, what's in the queue, any cadence flags.

Currently: assembled manually from performance/tracker and output/.
Upgrade: one command produces a shareable PDF or Notion page.

### `/approve [file]`
Marks a specific content object as `status: approved` with a timestamp and approver note. Validates that the status is currently `review` before promoting.

Currently: editing frontmatter manually.
Upgrade: prevents accidental approval of `draft` pieces and logs who approved.

### `/switch-client [name]`
Changes active_client in settings.yaml, loads that client's brand context, and confirms what just changed. Prevents generating for the wrong client.

Currently: editing settings.yaml manually.
Upgrade: one command, confirmation prompt, no silent errors.

---

## Multi-client best practices

If you're running this engine for multiple clients simultaneously:

- **One ContentEngine folder per client is an option** — clean separation, no risk of cross-contamination
- **One ContentEngine folder for all clients is also fine** — the `brand/[client]/` and `output/[client]/` structure keeps everything separated
- Either way: always confirm `active_client` before generating

The riskiest moment is when you're switching between clients in the same session. The engine will generate for whoever is set as active_client. Double-check before every manifest run.
