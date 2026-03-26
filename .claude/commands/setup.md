# /setup — Content Engine Onboarding Wizard

Interactive setup for first-time configuration. Run this once when setting up the engine for a new client.

The wizard walks through client information, brand discovery, channel setup, and cadence — then scaffolds all the brand files and updates configuration.

---

## What This Command Does

1. Collects basic information (client name, founder name, etc.)
2. Guides through brand voice discovery via targeted questions
3. Sets up which channels are active
4. Configures initial cadence
5. Creates brand folder structure
6. Scaffolds voice profiles with answers
7. Updates `config/settings.yaml`
8. Gives next steps

---

## Running the Wizard

```
/setup
```

The wizard is conversational. Read each prompt carefully and provide your answers.

---

## Phase 1: Client Configuration (5 questions)

**Question 1: Client Slug**
"What's the short name for this client? (Use lowercase and hyphens. Example: 'meridian', 'acme-corp', 'founder-jane')"

Input: `[slug]`
- Used in all file paths: `brand/[slug]/`, `drafts/[slug]/`, etc.
- Cannot contain spaces or special characters
- Be concise: 1–2 words max

**Question 2: Display Name**
"What's the full name? (Example: 'Meridian', 'Acme Corporation', 'Jane Smith — Founder')"

Input: `[name]`
- Used in voice profiles and messaging
- Can be the founder's name or company name

**Question 3: Active Channels**
"Which channels are in scope? (Select all that apply)"

Options:
- [ ] Personal LinkedIn (founder's personal account)
- [ ] Company LinkedIn (company page)
- [ ] Newsletter (personal or company — which?)
- [ ] Blog
- [ ] Twitter / X
- [ ] Email sequences (sales or nurture)
- [ ] Sales assets (one-pagers, decks, etc.)

Selected: `[channels]`

**Question 4: Blocked Channels**
"Any channels that are explicitly OFF-LIMITS? (E.g., 'Never Twitter', 'No TikTok')"

Input: `[channels]`
- Used to ensure generators don't propose blocked channels

**Question 5: Active Client Confirmation**
"Should '[slug]' be set as the active client? (yes/no)"

Input: `[yes|no]`
- If yes: updates `config/settings.yaml` to make this client active
- If no: adds to available clients but doesn't activate yet

---

## Phase 2: Brand Voice Discovery (8 questions)

The wizard asks questions to discover the founder's natural voice and fills in `voice-personal.md` with the answers.

**Question 1: Voice in One Sentence**
"In one sentence, how does [founder-name] sound when they're being exactly themselves?"

Example response: "They write like someone who figured something out the hard way and can't help telling you about it."

Used for: `voice_in_one_sentence` field

**Question 2: Core Belief**
"What do they believe about their industry that most people don't? (One distinct viewpoint)"

Example response: "Operations isn't destiny — it's a series of choices about what to measure and automate."

Used for: "What they believe" section

**Question 3: Core Frustration**
"What makes them genuinely frustrated or angry about their field?"

Example response: "The obsession with optimization theater — companies that implement systems to seem sophisticated, not because they solve real problems."

Used for: "What makes them frustrated" section

**Question 4: Sentence Structure**
"How do they naturally write? (Short and punchy? Long and flowing? Lots of fragments?)"

Example response: "Short, declarative sentences that move fast. Then occasionally a longer one that builds an idea out."

Used for: Paragraph style guidance

**Question 5: How They Open**
"How do they typically open a post? (A claim? A story? A number? A question?)"

Example response: "Drops into a specific situation or moment. 'I was in a meeting where...' is how they begin, not 'have you ever wondered.'"

Used for: Opening style guidance

**Question 6: How They Close**
"How do they end? (Punchline? Direct ask? Hard truth? Question to the reader?)"

Example response: "Ends with either a hard truth or a question that makes the reader uncomfortable."

Used for: Ending style guidance

**Question 7: Words They Use (That Feel Native)**
"What words or phrases do they use that feel native to them? (Pull from their actual writing — things they actually say)"

Example response: "The thing is", "What actually happens", "Watched this happen", "When you finally look at the data"

Used for: Vocabulary section

**Question 8: Comfort With Personal Sharing**
"How comfortable are they sharing personal stories vs. keeping it professional? (1=very protective, 5=open book)"

Example response: "4 — Selectively personal. Will share stories about getting it wrong or failing. Doesn't share family life. Personal stories always have a professional lesson."

Used for: Personal disclosure section

---

## Phase 3: Channel Setup (4 questions)

**Question 1: Primary Platform Focus**
"Which platform is most important? (LinkedIn / Newsletter / Blog / Other?)"

Input: `[platform]`
- This becomes the priority for initial content generation

**Question 2: LinkedIn Post Length**
"If LinkedIn is active — what length performs best for them? (Choose one)"

Options:
- Under 200 words
- 200–350 words
- 350+ words

Used for: `channel-notes/personal-linkedin.md`

**Question 3: LinkedIn CTA Style**
"How do they ask for things on LinkedIn? (Do they have CTAs? Questions? None?)"

Example response: "Posts end with genuine questions. No sales-style CTAs. 'What's slowing your team down that nobody's measuring?' not 'DM me for a free audit.'"

Used for: CTA style guidance

**Question 4: Any Channel-Specific Rules**
"Any channel-specific behaviors to know? (E.g., 'Never uses hashtags', 'Always threads on Twitter', 'Newsletter only, no LinkedIn')"

Input: `[rules]`

Used for: Individual channel-notes files

---

## Phase 4: Cadence Setup (2 questions)

**Question 1: LinkedIn Posting Frequency**
"How often should they post on LinkedIn? (Daily / 3x week / Weekly / As input allows)"

Input: `[frequency]`

Used for: `config/cadence.yaml`

**Question 2: Newsletter in Scope**
"Is a newsletter planned? (Yes — set frequency / No — skip for now / Maybe later)"

If yes:
- Input frequency: `[Weekly / Biweekly / Monthly]`
- Used for: `config/cadence.yaml` and channel-notes

---

## Phase 5: Output & Next Steps

The wizard:

1. **Creates folder structure:**
   - `brand/[slug]/`
   - `brand/[slug]/channel-notes/`
   - `brand/[slug]/examples/{personal,company}/`
   - `drafts/[slug]/[channel]/` for each active channel

2. **Scaffolds voice files:**
   - Fills `voice-personal.md` with Q&A responses
   - Creates blank `voice-company.md` (to be filled separately)
   - Creates blank channel-notes files for active channels

3. **Updates config:**
   - Adds client to `config/settings.yaml`
   - Sets as active if confirmed

4. **Prints completion summary:**

```
✅ Setup Complete!

Created:
- brand/[slug]/ — all brand files
- brand/[slug]/examples/{personal,company}/ — ready for examples

Configured:
- Active channels: [list]
- Posting frequency: [frequency]
- Active client: [slug]

NEXT STEPS (before first generation):

1. **Add voice examples** (critical for quality)
   - 2–3 of [founder-name]'s best personal posts → brand/[slug]/examples/personal/
   - 2–3 company page or blog posts (if company content active) → brand/[slug]/examples/company/

2. **Fill in company voice** (if company content is in scope)
   - Edit brand/[slug]/voice-company.md
   - Same format as voice-personal.md

3. **Complete messaging framework**
   - Edit brand/[slug]/messaging.md
   - Fill in positioning, value props, proof points

4. **Review channel-notes**
   - Each active channel has a channel-notes file ready for you to customize

5. **Ready to generate**
   - Run /morning-scan to create today's content plan
   - Or run /process-input [file] to start with a specific input

Questions? Check CLAUDE.md for the full system guide.
```

---

## Important Notes

- **Examples are critical:** The more specific examples you provide, the better the outputs. Add your best work to the examples folders before running `/morning-scan`.

- **Voice profiles aren't permanent:** Run `/calibrate-voice` if generated content keeps missing the mark. The wizard is a starting point, not the final word.

- **Cadence is flexible:** You can adjust posting frequency anytime in `config/cadence.yaml`.

- **You can run setup again:** If you need to add a new client, just run `/setup` again. It creates a new client folder without affecting existing ones.
