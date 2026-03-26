# /generate-campaign

Run the full content generation pipeline from a processed insight file or campaign brief.
This command orchestrates the content manifest, gets your approval, then generates everything.

## Usage
```
/generate-campaign [insight-file-or-brief-path]
/generate-campaign inputs/processed/2026-03-11-strategy-session-insights.yaml
/generate-campaign inputs/briefs/q2-launch.yaml
```

## Instructions

You are the **Content Orchestrator** for the Content Ecosystem Engine.

---

### Phase 1: Load Context

**⚠ Load these FIRST — before reading the input, before anything else:**

1. **`knowledge/INDEX.md`** — master router. Confirms active brands, file locations, open errors.
2. **`knowledge/ERRORS.md`** — check for open issues before starting generation.
3. **`skills/multi-brand-router.md`** — load and apply routing rules before building the manifest.
4. **`skills/brand-voice-enforcer.md`** — load voice context for the active client.

Then load:
5. **`anti-ai-rules.md`** — writing rules and banned patterns. Every piece generated this run must pass the self-check at the end of this file.
6. **`knowledge/QUALITY_GATE.md`** — the 4-level scoring rubric. Every piece must pass all four levels before being saved.
7. **`knowledge/FREQUENCY_GUIDE.md`** — cadence logic and noise prevention philosophy. Use this to sanity-check the manifest before presenting it.

If any of these files are missing, stop and report the error. Do not generate without them.

2. Read the input file at `$ARGUMENTS`

3. Read `config/settings.yaml` — get `active_client` and model settings

4. Load shared brand context for the active client:
   - `brand/[client]/pillars.md`
   - `brand/[client]/personas.yaml`
   - `brand/[client]/messaging.md`

5. Load BOTH voice profiles — you'll need to know both before planning:
   - `brand/[client]/voice-personal.md` — for personal content
   - `brand/[client]/voice-company.md` — for brand content
   - List examples in `brand/[client]/examples/personal/` and `brand/[client]/examples/company/`

6. Check which voice profiles exist. If only one exists, note it and only generate for that profile.

If required brand files are missing, stop and tell the user:
```
⚠ Brand context incomplete for client: [name]
Missing: [list of missing files]
Run /new-brand [client-name] to set up brand context first.
```

**Voice profile selection rule — apply per content piece in the manifest:**

| Content type | Voice profile | Examples folder |
|---|---|---|
| Personal LinkedIn post | personal | examples/personal/ |
| Personal newsletter | personal | examples/personal/ |
| Personal/founder email | personal | examples/personal/ |
| Ghostwritten essay, op-ed | personal | examples/personal/ |
| Company LinkedIn post | company | examples/company/ |
| Brand blog post | company | examples/company/ |
| Company email sequence | company | examples/company/ |
| Sales one-pager, deck | company | examples/company/ |
| Company newsletter | company | examples/company/ |

When the brief does not specify personal vs. company for a content type (e.g., just says "LinkedIn posts"), **ask the user before generating** — do not guess.

---

### Phase 2: Build the Content Manifest

Analyze the input against the brand context. Produce a **Content Manifest**:

```yaml
# Content Manifest
# Generated: [timestamp]
# Input: [source file]
# Client: [client]

campaign: [campaign name or "ad-hoc-[date]"]
client: [client]
source_input: [file path]

insights:
  - id: insight_1
    insight: "[The core idea in one sentence]"
    pillar: "[assigned content pillar]"
    persona: "[assigned persona ID]"
    evidence: "[key quote or data from input]"
    generates:
      - type: blog
        voice_profile: company          # personal = founder byline, company = brand blog
        angle: "[Specific angle — NOT just 'a blog post about X']"
        title_suggestion: "[Working headline]"

      - type: social
        voice_profile: personal         # personal = founder LinkedIn, company = brand page
        platforms: [personal-linkedin, twitter]
        count: 5
        angle: "[Hook angle and specific take for social]"

      - type: social
        voice_profile: company
        platforms: [company-linkedin]
        count: 3
        angle: "[Brand POV angle — different from personal take above]"

      - type: newsletter
        voice_profile: personal         # or company — specify per brief
        angle: "[Newsletter-specific angle — more intimate than blog]"

  - id: insight_2
    insight: ""
    pillar: ""
    persona: ""
    evidence: ""
    generates:
      - type: social
        voice_profile: personal
        platforms: [personal-linkedin]
        count: 5
        angle: ""

total_content_pieces: [n]
estimated_generation_time: "[n] minutes"
```

**Rules for manifest generation:**
- **Every generate item must specify voice_profile** — personal or company. No exceptions.
- When the same insight generates both personal AND company social content, they get separate entries with different angles — not the same post in two profiles
- Each insight should map to at minimum 1 content format
- Don't create redundant pieces — if two insights overlap, merge them
- Blog posts require strong, specific angles — not summaries
- Social posts need platform-specific angles, not just rephrasing
- A newsletter should only come from the single strongest insight

---

### Phase 3: Present Manifest for Approval

**STOP HERE.** Display the manifest clearly and ask:

```
📋 Content Manifest Ready

I found [n] insights worth building content around.
Here's what I'll generate:

[Display each insight with its generates list]

Total: [n] pieces of content

Does this look right? Any changes before I generate?
- Type APPROVE to proceed
- Type EDIT + your changes to adjust the manifest
- Type CANCEL to stop
```

**Do not proceed until the user types APPROVE.**

---

### Phase 4: Generate Content

On approval, run each generator. For each item in the manifest:

1. Confirm the `voice_profile` from the manifest item — personal or company
2. Load the appropriate template from `templates/[type]/`
3. Load the correct voice profile:
   - `voice_profile: personal` → `brand/[client]/voice-personal.md` + `examples/personal/`
   - `voice_profile: company` → `brand/[client]/voice-company.md` + `examples/company/`
4. Load 1–2 examples from the correct examples subfolder
5. Generate the content following the generator rules in CLAUDE.md
6. **Run the anti-AI self-check** (from `anti-ai-rules.md`) on the generated content before saving:
   - Scan for banned words — fix any found
   - Find -ing clause endings — cut or restructure
   - Check for significance assertions — replace with evidence or cut
   - Check for "not only/just" patterns — rewrite
   - Check that the voice profile (I vs. we) is consistent throughout
7. Create a content object with proper YAML frontmatter — include `voice_profile` field
8. Save to `outputs/[type]/[YYYY-MM-DD]_[voice_profile]_[type]_[slug].md`
   - e.g., `outputs/social/2026-03-11_personal_linkedin_content-calendars.md`
   - e.g., `outputs/social/2026-03-11_company_linkedin_content-calendars.md`

**Parallel generation:** Run generators for different content types simultaneously when possible. Sequential within each type (variants 1–5 for social, etc.).

---

### Phase 5: Report Completion

```
✅ Generation Complete

Generated [n] pieces of content:

BLOG (company voice)
  ✓ outputs/blog/2026-03-11_company_blog_[slug].md — "[title]"

SOCIAL — Personal LinkedIn (I / founder)
  ✓ outputs/social/2026-03-11_personal_linkedin_[slug].md — 5 variants

SOCIAL — Company LinkedIn (we / brand)
  ✓ outputs/social/2026-03-11_company_linkedin_[slug].md — 3 variants

SOCIAL — Twitter
  ✓ outputs/social/2026-03-11_twitter_[slug].md — 5 variants (thread format)

NEWSLETTER
  ✓ outputs/newsletter/2026-03-11_newsletter_[slug].md — "[subject line]"

Next steps:
  Review outputs → update status to 'approved' → run /publish [file] to push to Notion
```
