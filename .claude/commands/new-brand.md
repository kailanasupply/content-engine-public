# /new-brand

Set up a new brand context folder for a new client (or for yourself).

## Usage
```
/new-brand [client-name]
/new-brand brian
/new-brand acme-corp
```

## Instructions

You are the **Brand Setup Agent** for the Content Ecosystem Engine.

---

**Step 1 — Create the folder structure**

Create these files/folders:
```
brand/[client-name]/
├── voice-personal.md    (copy from brand/_template/voice-personal.md)
├── voice-company.md     (copy from brand/_template/voice-company.md)
├── pillars.md           (copy from brand/_template/pillars.md)
├── personas.yaml        (copy from brand/_template/personas.yaml)
├── messaging.md         (copy from brand/_template/messaging.md)
└── examples/
    ├── personal/        (personal-voice content samples — founder/individual)
    └── company/         (company-voice content samples — brand content)
```

**Step 2 — Clarify the setup context**

Before asking brand questions, first ask:

```
Is [client-name] a person, a company, or both?

1. A person (founder/individual) — I'll set up their personal voice profile
2. A company — I'll set up the company brand voice profile
3. Both — I'll set up both profiles (most common for founder-led businesses)
```

For most clients the answer will be "both" — a founder who posts personally AND a company that publishes content. Set up both profiles. They share pillars, personas, and messaging — but have separate voice files.

**Step 3 — Interactive brand discovery**

Ask questions conversationally — one or two at a time, not a form dump.

**For the PERSONAL voice profile, ask:**

```
Let's start with [person name]'s personal voice.

First: How would you describe how [name] sounds when they write?
Not how they want to sound — how they actually sound.
Think about their best posts, emails, or messages. What's the feel?
```

Then gather:
1. Personal voice in one sentence — their actual character, not aspirational
2. What do they genuinely believe that others in their field don't?
3. What makes them angry or frustrated about their industry?
4. How do they open content — scenes, provocations, questions, data?
5. How personal do they get — do they share failures, family, doubts?
6. Words/phrases they use naturally and things they'd cringe at
7. CTA style — do they make soft asks, hard asks, or no asks?

**For the COMPANY voice profile, ask:**

```
Now let's set up [company name]'s brand voice.
This is how the company sounds — separate from how [founder] sounds personally.

What's the core belief that drives everything this company does?
(Not the mission statement — the actual animating conviction behind the work)
```

Then gather:
1. Brand voice in one sentence — the company's character
2. Who does the brand speak to (peer? student? client? partner?)
3. What does the company stand against, not just for?
4. How does the company handle proof — specific results, client names, data?
5. What topics belong only on the company page vs. personal page?
6. CTA style for the company — demo, discovery call, trial, content?

**For shared context (pillars, personas, messaging), ask:**

1. What are the 4–6 content pillars? (main strategic themes)
2. Who are 1–3 distinct audience personas?
3. What problem does the company solve, and what's the "before/after"?
4. What makes it different from alternatives?
5. Any proof points, stats, or results to reference?

As the user answers, fill in both voice files and all shared files accordingly.

**Step 4 — Examples folder prompt**

After completing setup:
```
✓ Brand context created for: [client-name]

Now the most important step — examples.

The engine uses real examples of content to match voice.
Without examples, output will be technically correct but generic.
With examples, it sounds like the actual person/brand.

Add content to these two folders:

  brand/[client-name]/examples/personal/
  → 3–5 of [person's] best personal LinkedIn posts, newsletter issues,
    or any writing that sounds most like them

  brand/[client-name]/examples/company/
  → 3–5 of the best company LinkedIn posts, blog posts, or emails
    that represent the brand at its best

Any .md or .txt file. Name them whatever you want.
The better and more specific the examples, the better everything generates.
```

**Step 5 — Optional: set as active client**

```
Set [client-name] as the active client in settings.yaml? (yes/no)
```

If yes, update `active_client` in `config/settings.yaml`.

**Step 6 — Summary**

```
✅ Brand setup complete: [client-name]

Files created:
  brand/[client-name]/voice-personal.md  ← Personal/founder voice
  brand/[client-name]/voice-company.md   ← Company/brand voice
  brand/[client-name]/pillars.md
  brand/[client-name]/personas.yaml
  brand/[client-name]/messaging.md
  brand/[client-name]/examples/personal/ ← Add personal content samples here
  brand/[client-name]/examples/company/  ← Add company content samples here

Next: Add examples, then drop an input file in /inputs/ and run /process-input.
```
