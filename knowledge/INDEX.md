# Content Engine — Master Index

**Read this file first. Every run. Without exception.**

This is the central router. It tells you what exists, where to find it, and what to load for any given task. If a file isn't listed here, verify it exists before referencing it.

Last updated: [update when you configure this engine]

---

## Active State

```
Active client:     [your-client-slug]
Active brands:     [your-client] | [brand-2] | [brand-3]
Engine version:    1.1 (Plan→Work→Assess→Compound loop)
Last synthesis:    [check performance/insights.md header]
Open errors:       [check knowledge/ERRORS.md]
```

**First-time setup:** Run `python scripts/setup.py` then `/new-brand [your-client]` to populate brand context.

---

## ⚠ Pre-Flight Check (run before every session)

1. Read `knowledge/ERRORS.md` — any open errors change what you do today
2. Read `config/settings.yaml` — confirms active brands and channel restrictions
3. Check `performance/cadence-log.yaml` — confirms last generation dates per brand

If any of these files is missing or unreadable → STOP and report before proceeding.

---

## Skills (root — orchestration)

These are the high-level workflow skills. Load the relevant one before starting any task.

| Skill | File | When to use |
|-------|------|-------------|
| Morning Content Scan | `skills/morning-content-scan.md` | Daily. Start here every session. |
| Process Inspiration | `skills/process-inspiration.md` | New files in inputs/inspiration/ |
| Content Repurposer | `skills/content-repurposer.md` | No new inputs, or /repurpose-idea |
| Quality Assessor | `skills/quality-assessor.md` | After every generation. The Assess phase. |
| Synthesize Learnings | `skills/synthesize-learnings.md` | Weekly. After 5+ perf entries. The Compound phase. |
| Multi-Brand Router | `skills/multi-brand-router.md` | Before any generation decision. Channel enforcement. |
| Brand Voice Enforcer | `skills/brand-voice-enforcer.md` | Pre- and post-generation voice gate. |
| Skill Creator | `skills/skill-creator.md` | Building or improving skills. |

---

## Technical Skills (.claude/skills — tools and scripts)

| Skill | Path | What it does |
|-------|------|--------------|
| Anti-AI Scanner | `.claude/skills/anti-ai-scanner/` | Deterministic banned pattern scanner. Run before saving ANY draft. |
| Voice Fingerprint | `.claude/skills/voice-fingerprint/` | Layered voice context per client. Load before generating. |
| Adversarial Reviewer | `.claude/skills/adversarial-reviewer/` | Cold read for voice drift and specificity gaps. Runs after scanner. |
| Performance Intelligence | `.claude/skills/performance-intelligence/` | Parses tracker + cadence data into insight files. |
| Generation Log | `.claude/skills/generation-log/` | Append-only log of every generated piece. Query tool included. |
| Brand Setup | `.claude/skills/brand-setup/` | Scaffolds new client brand context folders. |
| Evergreen Miner | `.claude/skills/evergreen-miner/` | Scores archive candidates for repurpose potential. |
| Publish Validator | `.claude/skills/publish-validator/` | Pre-publish frontmatter and status gate. |

---

## Slash Commands (.claude/commands)

| Command | File | Purpose |
|---------|------|---------|
| /morning-scan | `morning-scan.md` | Daily scan → uses morning-content-scan skill |
| /process-input | `process-input.md` | Process a specific raw input file |
| /process-inspiration | `process-inspiration.md` | Process inputs/inspiration/ → uses process-inspiration skill |
| /generate-campaign | `generate-campaign.md` | Full generation pipeline for a brief or input |
| /repurpose-idea | `repurpose-idea.md` | Repurpose specific archived idea → uses content-repurposer skill |
| /monthly-evergreen-scan | `monthly-evergreen-scan.md` | Full archive scan → uses content-repurposer skill |
| /review-drafts | `review-drafts.md` | Structured review session for drafts/ |
| /publish | `publish.md` | Push approved draft to Notion + Airtable |
| /log-performance | `log-performance.md` | Log real results for published content |
| /synthesize-learnings | `synthesize-learnings.md` | Compound: update insights + ERRORS.md |
| /calibrate-voice | `calibrate-voice.md` | Fix voice drift → uses brand-voice-enforcer skill |
| /update-company-context | `update-company-context.md` | Log business/positioning changes |
| /new-brand | `new-brand.md` | Add new client → uses brand-setup skill |
| /switch-brand | `switch-brand.md` | Change active_client in settings.yaml |
| /generate-weekly-report | `generate-weekly-report.md` | Weekly performance summary |

---

## Brand Context Files

> **Before first run:** populate each section below by running `/new-brand [client-slug]`.
> Update the status column as you complete each file.

### [your-client] — personal brand
| File | Path | Status |
|------|------|--------|
| Voice (personal) | `brand/[your-client]/voice-personal.md` | ⚠ run /new-brand first |
| Voice (company) | `brand/[your-client]/voice-company.md` | ⚠ run /new-brand first |
| Channel notes | `brand/[your-client]/channel-notes/` | ⚠ run /new-brand first |
| Examples (personal) | `brand/[your-client]/examples/personal/` | ⚠ add 2–5 examples |
| Examples (company) | `brand/[your-client]/examples/company/` | ⚠ add 2–5 examples |
| Voice fingerprint | `.claude/skills/voice-fingerprint/[your-client]/` | ⚠ populate 5 layers |

### [brand-2] — (add additional brands as needed)
| File | Path | Status |
|------|------|--------|
| Voice (company) | `brand/[brand-2]/voice-company.md` | ⚠ not set up |
| Channel notes | `brand/[brand-2]/channel-notes/` | ⚠ not set up |
| Examples | `brand/[brand-2]/examples/` | ⚠ not set up |
| Voice fingerprint | `.claude/skills/voice-fingerprint/[brand-2]/` | ⚠ not set up |

> Copy the `brand/_template/` folder for each new brand. Then run `/new-brand [brand-slug]` to scaffold and populate.

---

## Knowledge Files

| File | Purpose | Load when |
|------|---------|-----------|
| `knowledge/INDEX.md` | **This file.** Master router. | Always first. |
| `knowledge/ERRORS.md` | Drift log, open issues, resolved errors. | Always second. |
| `knowledge/FREQUENCY_GUIDE.md` | Cadence philosophy — human-readable. | During planning. |
| `knowledge/QUALITY_GATE.md` | 0–10 scoring rubric. | Before scoring any draft. |
| `knowledge/CLIENT_ONBOARDING.md` | New client setup guide. | When running /new-brand. |
| `knowledge/TEAM_USAGE.md` | Team workflow guide. | When others are using the engine. |
| `anti-ai-rules.md` | Banned patterns. Hard constraints. | Before every generation. |
| `QUALITY_GATE.md` (root) | Scoring rubric (canonical copy). | Before scoring. |
| `SUCCESS_METRICS.md` | Performance baselines per channel. | During synthesis. |

---

## Performance & Learning Files

| File | Purpose | Updated by |
|------|---------|-----------|
| `performance/insights.md` | Synthesized performance patterns. | /synthesize-learnings |
| `performance/tracker.yaml` | Published content + engagement data. | /log-performance |
| `performance/cadence-log.yaml` | Generation history per brand/format. | Every generation run |
| `performance/WEEKLY_REPORT.md` | Latest weekly report. | /generate-weekly-report |
| `learning/voice-calibration-log.md` | Voice correction history. | /calibrate-voice |
| `learning/company-evolution.md` | Business context changes. | /update-company-context |
| `learning/case-studies/` | Client results for use as proof. | Manual |
| `learning/research/` | Data and findings for content. | Manual |
| `.claude/skills/generation-log/log/generations.jsonl` | Every generated piece. | Every generation run |
| `.claude/skills/performance-intelligence/insights/` | Script-generated insight files. | After /synthesize-learnings |

---

## Inputs

| Location | Content | Processing |
|----------|---------|------------|
| `inputs/recordings/` | Audio files (mp3, m4a) | /process-input → transcribe.py |
| `inputs/notes/` | Text notes (.md, .txt) | /process-input |
| `inputs/briefs/` | Campaign briefs (.yaml) | /generate-campaign |
| `inputs/inspiration/` | Liked posts, ideas, screenshots | /process-inspiration |
| `inputs/processed/` | Processed transcripts + inspiration queues | Used by /morning-scan |

---

## Drafts & Output

| Location | Content |
|----------|---------|
| `drafts/[client]/[channel]/` | All generated pieces (status: draft) |
| `output/[client]/[channel]/` | Published pieces (status: published) |

**Naming convention:** `YYYY-MM-DD_[voice]_[channel]_[slug].md`

---

## Config

| File | Purpose |
|------|---------|
| `config/settings.yaml` | Active client, all brands, channel restrictions, API settings |
| `config/cadence.yaml` | Machine-readable frequency rules |
| `config/.env` | API keys (never commit) |

---

## Archive

| Location | Content |
|----------|---------|
| `archive/YYYY-MM/` | Processed input files, date-prefixed |
| `archive/evergreen-candidates/` | Ideas tagged for repurpose potential |

---

## Global Instructions (paste into Cowork Settings)

```
Always read knowledge/INDEX.md first. Then check knowledge/ERRORS.md for open issues.
Enforce my exact voice per brand and channel using the voice-fingerprint skill.
Apply QUALITY_GATE.md before saving any output — minimum score 7, target 8+.
Follow Plan → Work → Assess → Compound on every task.
Run synthetic persona assessment (Skeptical Reader, Ideal ICP, Platform Fit) before finalizing any draft.
Never create AI-slop. If a draft fails the anti-ai-scanner or scores below 7, rewrite or discard.
Log all errors and drift to knowledge/ERRORS.md.
```

---

## MCP Connector Notes (for auto-inputs)

See `CLAUDE.md` § "MCP Connectors" for full setup instructions.

| Connector | What it enables | Status |
|-----------|----------------|--------|
| Gmail MCP | Auto-pull client emails as raw inputs | ⚠ not connected |
| Notion MCP | Push drafts directly to Notion content calendar | ⚠ not connected |
| Slack MCP | Pull notes/ideas from Slack to inputs/notes/ | ⚠ not connected |
| Google Drive MCP | Access recordings, docs, briefs from Drive | ⚠ not connected |

To connect: see Cowork Settings → Connectors, or install via the plugin marketplace.

---

## Setup Checklist (first-time install)

- [ ] Update `Active State` section above with your client slug and brands
- [ ] Run `python scripts/setup.py` — verifies dependencies and folder structure
- [ ] Edit `config/settings.yaml` — set `active_client`, fill in any API keys
- [ ] Run `/new-brand [your-client]` — scaffolds brand context folder
- [ ] Populate `brand/[your-client]/voice-personal.md` and `voice-company.md`
- [ ] Add 2–5 examples to `brand/[your-client]/examples/personal/` and `examples/company/`
- [ ] Populate `.claude/skills/voice-fingerprint/[your-client]/` — all 5 layers
- [ ] Fill in `brand/[your-client]/channel-notes/` for each active channel
- [ ] Update Brand Context Files table above — change ⚠ to ✅ as each file is populated
- [ ] Run first `/morning-scan` to confirm everything is wired up
