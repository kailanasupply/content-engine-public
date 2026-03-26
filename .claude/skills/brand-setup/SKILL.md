---
name: brand-setup
description: Scaffold a new client brand context folder interactively. Use this skill when adding a new client, running /new-brand, or when brand files are missing and generation is blocked. Trigger on: "add new client", "new brand", "/new-brand [name]", "brand files missing", "scaffold brand", or any time the orchestrator cannot find brand context for a client.
---

# Brand Setup

Guided, resumable scaffolding for new client brand contexts. Creates the full `brand/[client]/` directory structure and populates it through a conversation-driven interview.

---

## What this skill creates

```
brand/[client]/
├── voice-personal.md          ← Personal voice profile (I, founder, individual)
├── voice-company.md           ← Company voice profile (We, brand, org)
├── pillars.md                 ← 3–5 content pillars with descriptions
├── personas.yaml              ← Audience personas with pain points and vocabulary
├── messaging.md               ← Positioning, differentiators, banned phrases
├── channel-notes/
│   ├── personal-linkedin.md   ← LinkedIn behavioral rules (personal)
│   ├── company-linkedin.md    ← LinkedIn behavioral rules (company page)
│   ├── newsletter.md          ← Newsletter structure and voice rules
│   ├── twitter.md             ← Twitter/X rules
│   └── blog.md                ← Blog structure and SEO approach
└── examples/
    ├── personal/              ← Drop 2+ personal-voice examples here
    └── company/               ← Drop 2+ company-voice examples here
```

---

## Running the scaffold

```bash
python .claude/skills/brand-setup/scripts/scaffold_brand.py \
  --client [name] \
  --brand-dir brand/ \
  --template-dir brand/_template \
  --state .claude/skills/brand-setup/state/[client]-setup.json
```

**What the script does:**
- Creates all directories and files from `brand/_template/`
- Replaces `[CLIENT_NAME]` placeholders with the actual client slug
- Writes a state file tracking which sections have been filled in
- Is idempotent — safe to re-run; never overwrites content already written

**After running the script:**
Load the state file to see which sections still need interview questions.

---

## Setup interview

The brand setup interview covers 6 sections. Each section maps to one or more brand files.

### Section 1: Identity
Questions → `voice-personal.md`, `voice-company.md`

Ask:
- What's the client's name and role/title?
- How do they describe what they do in plain language?
- What's the company name and what does it do in one sentence?
- Who is NOT their audience?
- What tone do they absolutely want to avoid?

### Section 2: Voice characteristics
Questions → `voice-personal.md`, `voice-company.md`

Ask:
- Give me 3 adjectives for how the personal content should sound
- Give me 3 adjectives for how the company content should sound
- What does their writing absolutely never do? (e.g., never uses buzzwords, never uses questions as CTAs)
- Are there specific words or phrases they hate seeing in their own content?
- Share 1–2 examples of writing that feels right — doesn't have to be theirs

### Section 3: Content pillars
Questions → `pillars.md`

Ask:
- What are the 3–5 recurring themes they want to be known for?
- For each pillar: what's the core belief or POV they hold on this topic?
- Which pillar is most important for audience growth right now?

### Section 4: Audience personas
Questions → `personas.yaml`

Ask:
- Who are the 2–3 types of people most likely to read their content?
- For each persona: title/role, biggest frustration, what they want to be true, vocabulary they use
- Which persona are they most trying to reach?

### Section 5: Messaging
Questions → `messaging.md`

Ask:
- What's the one thing they want to be known for?
- What makes their positioning different from the obvious alternative?
- Are there competitors or comparisons they want to avoid?
- What claims are off-limits? (things they don't want to overclaim)

### Section 6: Channel configuration
Questions → `channel-notes/[channel].md`

Ask which channels are active, then for each active channel:
- Any hard limits on format or length?
- Is there a CTA pattern they use consistently?
- Anything they've tried that bombed?
- Any channel-specific rules (e.g., "no hashtags on LinkedIn")?

---

## State tracking

The state file at `.claude/skills/brand-setup/state/[client]-setup.json` tracks progress:

```json
{
  "client": "new-client",
  "created": "2026-03-22",
  "sections": {
    "identity": "complete",
    "voice": "in_progress",
    "pillars": "pending",
    "personas": "pending",
    "messaging": "pending",
    "channels": "pending"
  },
  "active_channels": ["personal-linkedin", "company-linkedin", "newsletter"],
  "notes": ""
}
```

**Resuming an interrupted setup:**
```bash
python .claude/skills/brand-setup/scripts/scaffold_brand.py \
  --client [name] \
  --resume \
  --state .claude/skills/brand-setup/state/[client]-setup.json
```

The `--resume` flag skips sections marked `complete` and starts from the first `in_progress` or `pending` section.

---

## Quality check before marking complete

Before marking brand setup complete, verify:

- [ ] `voice-personal.md` has at least 5 rules specific to this client (not just template placeholders)
- [ ] `voice-company.md` has at least 5 rules specific to this client
- [ ] `pillars.md` has 3–5 named pillars, each with a description and POV
- [ ] `personas.yaml` has at least 2 personas with titles and pain points filled in
- [ ] `messaging.md` has banned phrases/words section populated
- [ ] Active channel-notes files have at least 3 client-specific rules each
- [ ] `examples/personal/` has at least 1 example file
- [ ] `examples/company/` has at least 1 example file (or a note that it will be added)

Run this check:
```bash
python .claude/skills/brand-setup/scripts/scaffold_brand.py \
  --client [name] \
  --check \
  --brand-dir brand/
```

Exit code 0 = all checks pass. Exit code 1 = missing sections reported.

---

## After setup is complete

1. Update state file: set all sections to `complete`
2. Add client to `config/settings.yaml` if it will be the active client
3. Add client to `config/cadence.yaml` with default cadence rules
4. Run a test generation: `/generate-campaign` with a simple brief to verify voice loads correctly
5. Archive the state file or leave it for reference — it won't interfere with generation

---

## Notes on examples

The `examples/` folders are populated manually — the script creates the directories but cannot generate examples automatically. After setup:

- Drop 2–3 real pieces from the client (or approved drafts) into `examples/personal/` and `examples/company/`
- Name them descriptively: `2026-03-ai-hiring-post.md`, `2026-03-product-launch-linkedin.md`
- These are used as few-shot reference during generation — quality here directly affects output quality
