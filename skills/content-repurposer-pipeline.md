---
name: content-repurposer-pipeline
description: Take one fresh source (URL, file path, or inline text) and generate all eligible platform formats simultaneously. Each format is written natively from scratch — not adapted. Constraints are baked INTO generation, not applied after. Trigger: /repurpose [source]
triggers:
  - /repurpose
  - /repurpose-from-url
  - repurpose this idea
  - turn this into content
loop: Ingest → Plan → Generate → Assess → Output
---

# Content Repurposer Pipeline

Turn any fresh source into finished, multi-platform content in one pass. Each format is a native piece — not an adaptation of another format.

---

## Phase 1: INGEST

### Step 1a: Accept the source

The pipeline accepts three input types:

**Type 1: URL**
- Pass a full URL: `https://[site]/[article]`
- The skill fetches and extracts main content (headline, body, subheadline if present)
- Rejects paywalls and access-restricted content — ask user to paste excerpts instead

**Type 2: File path**
- Pass an absolute path: `/sessions/.../inputs/notes/client-call.md` or `drafts/brian/twitter/[draft].md`
- The skill reads the file and extracts main content

**Type 3: Inline text**
- Paste the raw text directly in your message (for short thoughts, quotes, transcripts, ideas)

### Step 1b: Extract the core argument and POV

Read the source and extract in writing:

1. **Core argument** (1 sentence max) — the main claim or insight
   - "Fraud detection models trained on historical data will fail on novel attack patterns."
   - "Waiting for the risk conversation to end before you enter it costs you influence."
   - NOT a summary. The actual position.

2. **Key proof/story** (1 specific example max) — the most interesting concrete evidence
   - A number, a client result, a specific scenario, a named tool, a decision, a moment
   - "In week two, the team had mapped 47 threat categories. By week four, we'd classified 30 of them as novel."
   - NOT "Teams discovered many novel threats." The specific evidence.

3. **POV layer** (the opinion being expressed) — what does the author believe about this?
   - "Fraud leaders who don't enter the risk conversation early don't influence strategy."
   - "The first 90 days running fraud are the only ones that matter."

### Step 1c: Validation gate

**Reject if the source:**
- Is purely informational with no position (news article, explainer, listicle without opinion)
- Has no clear proof or story (bare claim with no evidence)
- Is entirely promotional (pitch deck, sales material, press release with no real insight)
- Lacks an angle specific enough to anchor multiple formats

**In reject cases:** Report to user: "This source is [reason]. To repurpose it, please clarify: What's the specific insight or POV? What's the one concrete example that proves it?" Then wait for clarification and restart.

**In accept cases:** Proceed to Phase 2.

---

## Phase 2: PLAN

### Step 2a: Load mandatory context

In this order:

1. `anti-ai-rules.md` — hard constraints on word choices, sentence patterns
2. `config/settings.yaml` — get `active_client` (brand slug)
3. `config/cadence.yaml` — check eligible formats and channel restrictions for this brand
4. `.claude/skills/voice-fingerprint/[active_client]/core-voice.md` — core voice rules
5. `.claude/skills/voice-fingerprint/[active_client]/gotchas.md` — highest recency weight (load last)
6. `brand/[active_client]/examples/personal/` — load 1 most relevant example
7. `performance/insights.md` — if it exists, synthesis of what's working structurally

### Step 2b: Determine which formats to generate

Check `config/cadence.yaml` under `brand_overrides: [active_client]:` — which formats are `active: true`?

For each active format, ask:
1. **Is the source rich enough?** (see `minimum_input_richness` in cadence.yaml)
   - Single-sentence idea → skip blog, newsletter; do LinkedIn + Twitter + Slack
   - Interview transcript or long essay → all formats eligible
2. **Is the brand restricted?** (SaySo = twitter + company-linkedin ONLY)
3. **Is the format eligible today?** Check `cadence` field:
   - `daily` → always eligible if source is new
   - `weekly` → check `last_generated` in cadence-log.yaml; skip if generated in last 6 days
   - `on_demand` → skip unless explicitly requested in user command

Build a working list of eligible formats:

| Format | Eligible? | Voice | Notes |
|---|---|---|---|
| Personal LinkedIn | ? | personal | 150–300 words, opens specific |
| X/Twitter thread | ? | personal | 3–6 tweets, native rhythm |
| Email teaser | ? | personal | 80–120 words, newsletter opening |
| Company LinkedIn | ? | company | 100–180 words, outcome-first |
| Slack one-liner | ? | personal | 1–2 sentences, shareable |

### Step 2c: Present the plan to user

Show this format:

```
━━━ REPURPOSE PLAN ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: [title or URL]
Core argument: [1 sentence]
Key proof: [1 specific example]

Formats to generate:
  ✓ Personal LinkedIn (150–300 words, specific opening)
  ✓ X thread (3–6 tweets, hook + proof + POV)
  ✓ Email teaser (80–120 words, newsletter style)
  ✗ Company LinkedIn (brand voice not needed for this source)
  ✓ Slack one-liner (1–2 sentences)

Ready to generate? Reply "yes" or "modify [format names]"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Wait for user confirmation before proceeding to Phase 3.**

---

## Phase 3: GENERATE

Generate all confirmed formats **simultaneously** — write each natively from scratch, not by adapting another format.

### 3.1 Personal LinkedIn Post

**Constraints baked in:**
- 150–300 words
- Opens with: specific moment, specific number, contrarian observation, or direct claim
- Never: "In today's X landscape..." / "Have you ever wondered..." / "Let me share..."
- One POV. No listicles.
- Voice: Brian's rules (specific over general, states positions directly, no em dashes)
- Structure: Opens on the claim → elaborates with proof/story → lands on the implication
- Ends when the thought ends. No question. No soft CTA. The landing IS the post.

**Write as if:** This is a post someone sends because they had a specific realization they need to say out loud. Not because they want engagement. Not because they're being productive. Because the thing was real.

**Check while drafting:**
- Is the first sentence about the actual insight? Or am I setting a scene?
- Did I use a specific number, name, or moment? Or am I gesturing at one?
- Does every sentence advance the argument? Or am I padding?
- Is the last line the actual landing? Or did I add commentary after?

### 3.2 X/Twitter Thread

**Constraints baked in:**
- 3–6 tweets total (not more unless the idea sustains it)
- Tweet 1: Hook + main claim (under 220 characters, complete thought)
- Tweets 2–N: Each tweet = one self-contained proof point, implication, or story beat
- Final tweet: The POV or "the thing most people miss" — the insight that changes how the reader sees the problem
- Voice: Brian's voice adapted for Twitter brevity (direct, specific, no hedging)
- No filler tweets. If the idea doesn't fill 4+ substantial tweets, make it a thread of 3.
- Each tweet must stand alone (be readable on its own) but flow to the next

**Write as if:** Each tweet is a complete thought. You're not building suspense. You're not asking for retweets. You're stating a series of related facts and ending with the belief they add up to.

**Check while drafting:**
- Does tweet 1 grab? Or does it explain?
- Is each tweet a real point? Or am I using tweets as line breaks?
- Does the thread end with the insight? Or with a question/CTA?
- Can I cut a tweet? If yes, cut it.

### 3.3 Email Teaser (Newsletter Opening)

**Constraints baked in:**
- 80–120 words
- Written as if this is the opening 2 paragraphs of the House of Fraud weekly newsletter
- Paragraph 1: The question, tension, or observation that makes the reader care
- Paragraph 2: Why it matters right now, ends with an incomplete thought or question to pull reader in
- No CTA. No "read on." This is a teaser that makes the reader want to open the full newsletter.
- Voice: Conversational, direct, assumes the reader knows what House of Fraud is
- Structure: Start in the middle of the idea (not at the beginning). End mid-thought.

**Write as if:** The reader opened their email, saw the teaser, and either deleted it or clicked to read the full email. You're the first 2 sentences that determine which one.

**Check while drafting:**
- Does the first line make the reader wonder? Or explain?
- Is there a reason to keep reading? Or could they predict the rest?
- Does it end mid-thought? Or wrapped up?

### 3.4 Company LinkedIn Post

**Constraints baked in:**
- 100–180 words
- Opens with outcome or observation (not story, not context)
- Voice: Company voice ("we"), not founder diary
- Structure: Observation → insight → why it matters → soft CTA
- Audience: "People interested in fraud prevention, risk management, or company work"
- No personal anecdote. This is the company's POV, not the founder's.

**Write as if:** The company has learned something or built something. You're announcing it without being promotional about it.

**Check while drafting:**
- Is the voice "we" throughout? Not "I"?
- Does it lead with an outcome or fact? Not a story?
- Is there false significance? (Cut any "reflects broader trends" or "underscores the importance")

### 3.5 Slack One-Liner

**Constraints baked in:**
- 1–2 sentences max
- Feels like something you'd text to a colleague who works in fraud
- No jargon. No "delve into." Direct, specific, human.
- The core idea as the most shareable version

**Write as if:** You're in a Slack thread and you just thought of the one thing that encapsulates the whole idea. You say it and move on.

**Check while drafting:**
- Could I say this in a sentence? If yes, it should be one.
- Does it feel like marketing? Or like what you'd actually say?

---

## Phase 4: ASSESS

Run each generated piece through this sequence:

### 4.1 Anti-AI Self-Check

Scan for violations of `anti-ai-rules.md`:

1. **Banned words** — does the text use any from the list?
   - Scan for: `delve`, `pivotal`, `testament`, `intricate`, `meticulous`, `vibrant`, `garner`, `fostering`, `showcase`, `highlight` (verb), `crucial`, `robust`, `landscape` (abstract), `navigate` (figurative), `boasts`, `serves as`, `stands as`, `underscore` (verb), `em dashes (—)`
   - If found: rewrite immediately.

2. **Banned patterns** — are there:
   - Sentences ending in -ing clauses that add false significance? ("...contributing to the growth of...")
   - "Not only X, but also Y" structures in any form?
   - Vague attribution? ("Experts say..." "Studies show...")
   - False significance assertions? ("underscores," "reflects broader trends," "is a testament to")
   - Em dashes anywhere?
   - If found: rewrite immediately.

3. **Voice check** — does it sound like it was written FOR that platform natively?
   - LinkedIn post: Does it sound like a person had a thought? Or like a press release?
   - Twitter thread: Does each tweet feel like Twitter? Or like a blog post cut into pieces?
   - Email teaser: Does it feel like the opening of a newsletter? Or like a sales email?
   - Company LinkedIn: Does it sound like the company is speaking? Or like marketing copy?
   - Slack: Does it feel like a real thing someone said? Or formal?
   - If not: rewrite the piece entirely. Don't patch it.

4. **Cadence check** — is each format eligible per cadence.yaml?
   - If a format is `active: false` or `blocked: true` for this brand, flag it (don't include in output)
   - If a format has a `min_gap_days` rule and it was generated in the last N days, flag it (don't include in output)

### 4.2 Run the anti-ai-scanner (Python check)

```bash
python .claude/skills/anti-ai-scanner/scripts/scan_draft.py [file-path]
```

- Exit code 0 = pass
- Exit code 1 = violations found. Fix all hard bans and re-scan.

### 4.3 Adversarial reader review (cold read)

Load `.claude/skills/adversarial-reviewer/SKILL.md` and run mentally:
- Would a skeptical reader believe this is specifically from this person? Or could any fraud leader have written it?
- Are there concrete details? Or gestures at details?
- Is every claim supported? Or asserted?
- Does it land? Or does it feel like it's explaining itself?

If the adversarial reader scores it below 6/9 on specificity + voice fit + landing, rewrite before saving.

### 4.4 Final check: Is this a finished piece?

Ask yourself:
- Would this person send this to a colleague? Or does it need another pass?
- Does every sentence do work? Or am I padding?
- Is it specific to this source? Or generic enough that it could be from anything?

If the answer to any of these is "it needs another pass" — do another pass now. Don't save something that's not done.

---

## Phase 5: OUTPUT

### 5.1 Present all formats in a clean block

Format:

```
━━━ REPURPOSE RUN — [YYYY-MM-DD] ━━━━━━━━━━━━━━━━━━━━━━━━
Source: [title or URL]
Core argument: [1 sentence]
Formats generated: [list, comma-separated]
Quality check: All formats passed anti-AI scan and voice fit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 PERSONAL LINKEDIN
[full draft]

🐦 X THREAD
Tweet 1: [text]
Tweet 2: [text]
[...]

📧 EMAIL TEASER
[full draft]

🏢 COMPANY LINKEDIN
[full draft]

💬 SLACK ONE-LINER
[text]

━━━ SAVE THESE? ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply:
  • "save all" — save all formats to drafts/
  • "save [format names]" — e.g., "save personal-linkedin twitter email-teaser"
  • "skip" — discard all
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.2 Save the formats the user approves

For each format, save to: `drafts/[active_client]/[platform]/[YYYY-MM-DD]_[voice]_[platform]_[slug].md`

Include YAML frontmatter for each:

```yaml
---
id: [uuid]
type: social | email | newsletter
subtype: [personal-linkedin | company-linkedin | twitter | email-teaser | slack]
voice_profile: personal | company
title: [auto-generated: source title + format + date]
client: [active_client from settings.yaml]
campaign: null
pillar: [auto-tag from source if clear; otherwise "general"]
persona: [target persona from brand config; or "general audience"]
platform: personal-linkedin | company-linkedin | twitter | email | slack
status: draft
created: [ISO timestamp]
word_count: [n]
quality_score: 8
quality_notes: "Generated from [source]. Passed anti-ai scan and voice fit. Ready for review."
notion_id: null
airtable_record_id: null
---
[content]
```

### 5.3 Update logs after save

After saving, run these updates (or log for later manual run):

1. Update `performance/cadence-log.yaml`:
   - Set `last_generated: [YYYY-MM-DD]` for each format that was generated

2. Append to `.claude/skills/generation-log/log/generations.jsonl`:
   ```json
   {
     "id": "[uuid-from-frontmatter]",
     "date": "[YYYY-MM-DD]",
     "client": "[active_client]",
     "source": "[original-source-url-or-filename]",
     "formats": ["format1", "format2"],
     "file_paths": ["path/to/file1.md", "path/to/file2.md"],
     "voice_profile": "personal|company",
     "quality_score": 8,
     "created_at": "[ISO timestamp]"
   }
   ```

3. Log to `knowledge/ERRORS.md` if any formats were flagged or skipped (with reason)

---

## Edge Cases & Escalation

### If the source is too thin

**Source:** "AI is changing fraud. Here's why."
**Action:** Ask user: "What's the specific insight here? Are you saying detection models trained on historical data won't work on novel attacks? Or that AI is making attacks faster? Pick one and I'll repurpose it."

### If multiple formats would be redundant

**Example:** User wants both "personal LinkedIn" and "email teaser" from a short thought.
**Action:** Flag it: "Email teaser needs ~100 words and builds on newsletter rhythm. Personal LinkedIn is 150–300 and stands alone. This source is [X words]. Both would feel thin. Which format matters more — LinkedIn or email?"

### If the source contradicts brand guidelines

**Example:** User repurposing a LinkedIn article about AI for the SaySo brand.
**Action:** Flag it: "SaySo is X + Company LinkedIn only. This source would work as: X thread (personal voice). Company LinkedIn would need brand POV instead of author's POV. Generate just the X thread?"

### If the source is too promotional

**Example:** A startup blog post that's essentially a pitch deck in prose.
**Action:** Reject and ask: "This reads like a company pitch. If I repurpose it, every version will sound promotional, which violates anti-ai-rules.md. What's the underlying insight (not the product pitch)? Help me separate the POV from the marketing."

---

## LOOP: Ingest → Plan → Generate → Assess → Output

**Every run follows this sequence without shortcuts.**

**Ingest:** Read the source, extract argument + proof, validate for repurposing potential.

**Plan:** Load context, check cadence, determine eligible formats, present plan to user for approval.

**Generate:** Write all approved formats natively from scratch, constraints baked in.

**Assess:** Run anti-AI self-check, anti-ai-scanner, adversarial reader review, voice fit check.

**Output:** Present all formats, wait for save approval, save approved formats with frontmatter, update logs.

---

## Quality Gate

All repurposed content must score ≥7 on the `QUALITY_GATE.md` rubric before saving:

- **Voice fit:** Does this sound natively from/for that platform? (0–3)
- **Specificity:** Is it rooted in the source's concrete details? (0–3)
- **Landing:** Does it end when the thought ends? (0–2)
- **Anti-AI compliance:** Passed scan + no banned patterns? (automatic if yes; 0 if fails)

**Scoring:**
- 8+ = save as-is
- 7 = save with flag "minor touch-up may be needed"
- 6 = rewrite or skip
- <6 = archive, don't save

If any format scores below 7, rewrite it entirely or skip it — don't save weak work.

---

## Files Loaded / Updated

**Read (load once at start of Phase 2):**
- `anti-ai-rules.md`
- `config/settings.yaml`
- `config/cadence.yaml`
- `.claude/skills/voice-fingerprint/[active_client]/core-voice.md`
- `.claude/skills/voice-fingerprint/[active_client]/gotchas.md`
- `brand/[active_client]/examples/personal/` (1 example)
- `performance/insights.md` (if exists)

**Write (after save approval in Phase 5):**
- `drafts/[active_client]/[platform]/[YYYY-MM-DD]_[voice]_[platform]_[slug].md` (all approved formats)
- `performance/cadence-log.yaml` (update `last_generated`)
- `.claude/skills/generation-log/log/generations.jsonl` (append entries for each saved format)
- `knowledge/ERRORS.md` (log if formats were flagged/skipped)

---

## Skill State

**Triggers:**
- `/repurpose [source]` where source is a URL, file path, or "this" (inline text)
- `repurpose this idea`
- `turn this into content`

**Loop:** Ingest → Plan → Generate → Assess → Output

**Output:** Ready-to-save drafts in `drafts/[client]/[platform]/` with full YAML frontmatter, plus updated cadence + generation logs.

**No file deletion.** No archival. Pure generation → save → log.
