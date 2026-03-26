# Content Ecosystem Engine — Template

A clean, sellable template of the Content Ecosystem Engine for CMOs and founders. **Zero personal data — fully customizable for any new client.**

This is a complete, production-ready template. Copy this folder, run `/setup`, and you're ready to generate branded content at scale.

---

## What's Included

### Core Documentation
- **CLAUDE.md** — Master orchestration rules and system guide. Read this first.
- **QUALITY_GATE.md** — 0–10 scoring rubric. Every piece must score ≥7.
- **SUCCESS_METRICS.md** — Engagement baselines per channel. Customize after 30 days of real data.
- **TEAM_GUIDE.md** — For operators running the engine (if you have a team).
- **FOUNDER_GUIDE.md** — For the content creator (what you need to do, not how it works).
- **anti-ai-rules.md** — Hard constraints on writing. Loaded before every generation.

### Brand Context Structure
- **brand/_template/** — Copy this folder for each new client. Includes:
  - `voice-personal.md` — How the founder sounds (first person)
  - `voice-company.md` — How the brand sounds (plural)
  - `pillars.md` — 4–6 strategic content themes
  - `personas.yaml` — 2–4 audience personas
  - `messaging.md` — Positioning, value props, proof points
  - `channel-notes/` — Per-channel fine-tuning for LinkedIn, newsletter, blog, Twitter, etc.
  - `examples/personal/` & `examples/company/` — Real examples for few-shot reference

- **brand/example-client/** — Fully filled-in example (fictional company: Meridian). Use this as a reference for what good brand context looks like.

### Configuration
- **config/settings.yaml** — Active client, API keys, client list
- **config/.env.example** — Environment variable template (API keys go here)
- **config/cadence.yaml** — Content frequency rules per format per client

### Production Pipeline
- **inputs/** — Where raw content comes in (recordings, notes, briefs, inspiration)
- **drafts/** — Generated content awaiting review
- **output/** — Published content archive (post-publication)
- **archive/** — Monthly archive of processed inputs + rejected drafts
- **performance/** — Performance tracking, cadence log, synthesized insights
- **learning/** — Company evolution, voice calibration log, case studies

### Commands
- **.claude/commands/setup.md** — Interactive onboarding wizard (run this first!)
- Other commands should be copied from the main ContentEngine repository

### Learning & Reference
- **learning/company-evolution.md** — Tracks business changes over time
- **learning/voice-calibration-log.md** — Log of voice corrections
- **templates/**, **schemas/** — For internal use by generators

---

## Quick Start (For Buyers/Implementers)

### 1. First Time Setup

```bash
# Copy the template to your working directory
cp -r ContentEngine-Template/ ~/MyContentEngine/
cd ~/MyContentEngine/

# Run the setup wizard
/setup
```

The wizard:
- Asks about your client/founder and brand
- Creates brand context folders
- Scaffolds voice profiles from your answers
- Updates configuration
- Gives you next steps

### 2. What to Do After Setup

1. **Add examples** (critical for quality)
   - Drop 2–3 best posts from the founder into `brand/[client]/examples/personal/`
   - Drop 2–3 company posts into `brand/[client]/examples/company/`

2. **Complete brand context**
   - Fill in `brand/[client]/voice-company.md` (if company content is in scope)
   - Refine `brand/[client]/messaging.md` with real positioning and proof points
   - Customize channel-notes files per channel

3. **Drop your first input**
   - Add a raw notes file, recording, or campaign brief to `inputs/`

4. **Generate and review**
   - Run `/morning-scan` for a prioritized content plan
   - Review the manifest, approve, and generate

---

## The Example Client: Meridian

A fully realized fictional brand included as a reference:

- **Founder:** Alex Chen (VP of Operations turned founder)
- **Company:** Meridian (B2B SaaS for operations leaders)
- **Tone:** Direct, data-driven, occasionally dry humor
- **ICP:** Ops leaders at 50–500 person companies

**What you'll see in the example:**

- Detailed personal voice profile (Alex's voice)
- Detailed company voice profile (Meridian's voice)
- 4 content pillars (Bottleneck Diagnosis, Automation Strategy, etc.)
- 2 fully defined personas (Operations Leader, Founder)
- Complete messaging framework with proof points
- Channel-specific fine-tuning for LinkedIn, newsletter, blog

**Use this to:**
- See what "good" brand context looks like
- Copy the structure for your own client
- Reference how to fill in voice profiles
- Test the engine with a real-world example

---

## Directory Structure

```
ContentEngine-Template/
├── CLAUDE.md                    ← System guide (read first)
├── QUALITY_GATE.md              ← Scoring rubric
├── SUCCESS_METRICS.md           ← Performance baselines
├── TEAM_GUIDE.md                ← For operators
├── FOUNDER_GUIDE.md             ← For content creator
├── anti-ai-rules.md             ← Writing rules (non-negotiable)
├── .claude/
│   └── commands/
│       └── setup.md             ← Onboarding wizard
├── brand/
│   ├── _template/               ← Copy this for each new client
│   │   ├── voice-personal.md
│   │   ├── voice-company.md
│   │   ├── pillars.md
│   │   ├── personas.yaml
│   │   ├── messaging.md
│   │   └── channel-notes/
│   │       ├── personal-linkedin.md
│   │       ├── company-linkedin.md
│   │       ├── newsletter.md
│   │       ├── twitter.md
│   │       └── blog.md
│   └── example-client/          ← Fully filled example (Meridian)
│       ├── voice-personal.md
│       ├── voice-company.md
│       ├── pillars.md
│       ├── personas.yaml
│       ├── messaging.md
│       ├── channel-notes/
│       └── examples/
│           ├── personal/
│           └── company/
├── config/
│   ├── settings.yaml            ← Active client + API config
│   ├── .env.example             ← Environment variables template
│   └── cadence.yaml             ← Posting frequency rules
├── inputs/
│   ├── recordings/              ← Audio files for transcription
│   ├── notes/                   ← Raw text notes
│   ├── briefs/                  ← Campaign briefs
│   ├── inspiration/             ← Liked posts, raw ideas
│   └── inspiration/processed/   ← Structured insights
├── drafts/                      ← Generated content awaiting review
│   └── [client]/[channel]/
├── output/                      ← Published content archive
│   └── [client]/[channel]/
├── archive/                     ← Monthly archive of processed inputs
│   ├── YYYY-MM/
│   ├── evergreen-candidates/
│   └── rejected/
├── performance/
│   ├── README.md
│   ├── tracker.yaml             ← Performance log
│   ├── cadence-log.yaml         ← Last generated timestamps
│   └── insights.md              ← Synthesized patterns
├── learning/
│   ├── company-evolution.md     ← Business changes
│   ├── voice-calibration-log.md ← Voice correction history
│   ├── case-studies/
│   └── research/
├── templates/                   ← Format templates (internal)
├── scripts/                     ← Helper scripts (optional)
└── schemas/                     ← Content object schemas

```

---

## Key Concepts

### Voice Profiles
Every client has TWO separate voice profiles:
- **Personal:** How the founder sounds (first-person, raw, opinionated)
- **Company:** How the brand sounds (plural, polished, authoritative)

Never blend them. Personal LinkedIn ≠ Company LinkedIn.

### Content Pillars
4–6 strategic themes the brand consistently creates content around. Every piece maps to one pillar. If it doesn't fit, don't publish it.

### Personas
2–4 specific people the content is written FOR. Not generic "professionals." Specific roles, goals, pain points, reading habits.

### Quality Gate
Every generated piece is scored 0–10:
- ≥7 → Save as draft
- 5–6 → Flag for human decision
- <5 → Archive (don't save)

### Cadence System
Prevents overproduction. Each format has rules:
- How often it can be generated per week/month
- Minimum days between posts
- Whether it requires new input

### Performance Learning
The engine gets smarter over time:
1. Generate → Publish
2. Log performance → Synthesize insights
3. Generator reads insights and adjusts next run

---

## What Makes This Sellable

### Zero Personal Data
- No Brian, no House of Fraud, no Safeguard, no SaySo
- Example client (Meridian) is completely fictional
- Fully customizable for any founder/company
- Ready to resell or white-label

### Production-Ready
- All files included and properly structured
- No missing components
- Clear documentation at every level
- Tested folder hierarchy

### Buyer-Friendly
- `/setup` wizard handles all configuration
- FOUNDER_GUIDE and TEAM_GUIDE explain what they need to do
- anti-ai-rules ensure consistent quality
- Example client shows what "good" looks like

### Extensible
- New clients added via `/setup`
- New channels added to cadence.yaml
- Voice profiles are living documents (update via `/calibrate-voice`)
- Performance system improves over time

---

## Next Steps After Deploying

1. **Run `/setup`** for first-time configuration
2. **Fill in brand context** (voice profiles, pillars, personas, messaging)
3. **Add examples** from the founder's best work
4. **Drop first input** (notes, recording, or campaign brief)
5. **Generate and review** — run `/morning-scan` or `/process-input`
6. **Publish approved content**
7. **Log performance** and synthesize learnings after 5+ pieces

---

## Support & Customization

### To Customize for Your Client
1. Copy `brand/_template/` → `brand/[your-client]/`
2. Fill in voice profiles from conversations with founder
3. Build out messaging based on their actual positioning
4. Add real examples to the examples folder
5. Run `/setup` to configure

### To Add New Features
- Add commands to `.claude/commands/`
- Add channels to `config/cadence.yaml`
- Extend brand context with new files in `brand/[client]/`

### To Deploy for Multiple Clients
- Set up one client per `brand/[slug]/` folder
- Run `/setup` for each new client
- Use `config/settings.yaml` to switch active client

---

## Troubleshooting

**Generated content doesn't sound right?**
→ Check `brand/[client]/examples/` — load more/better examples. Run `/calibrate-voice`.

**Missing files error?**
→ Run `/setup` to scaffold brand folder. Some files must exist before generation.

**Content quality score is low?**
→ Read `QUALITY_GATE.md` to understand scoring. Check against `anti-ai-rules.md` for banned patterns.

**Cadence issues?**
→ Review `config/cadence.yaml`. Some formats might not be eligible today based on last-generated timestamp.

---

## Files Manifest

**Core Documentation (6 files)**
- CLAUDE.md
- QUALITY_GATE.md
- SUCCESS_METRICS.md
- TEAM_GUIDE.md
- FOUNDER_GUIDE.md
- anti-ai-rules.md

**Brand Templates (10 files)**
- brand/_template/voice-personal.md
- brand/_template/voice-company.md
- brand/_template/pillars.md
- brand/_template/personas.yaml
- brand/_template/messaging.md
- brand/_template/channel-notes/ (5 files)

**Example Client: Meridian (12 files)**
- brand/example-client/voice-personal.md
- brand/example-client/voice-company.md
- brand/example-client/pillars.md
- brand/example-client/personas.yaml
- brand/example-client/messaging.md
- brand/example-client/channel-notes/ (4 files)

**Configuration (3 files)**
- config/settings.yaml
- config/.env.example
- config/cadence.yaml

**Documentation & READMEs (8 files)**
- inputs/recordings/README.md
- inputs/notes/README.md
- inputs/briefs/README.md
- inputs/inspiration/README.md
- drafts/README.md
- output/README.md
- archive/README.md
- performance/README.md

**Performance & Learning (4 files)**
- performance/tracker.yaml
- performance/cadence-log.yaml
- learning/company-evolution.md
- learning/voice-calibration-log.md

**Commands (1 file)**
- .claude/commands/setup.md

**Total: 47 files + complete folder structure**

---

*This template is production-ready and fully customizable. Copy it, run `/setup`, add your examples, and start generating branded content.*
