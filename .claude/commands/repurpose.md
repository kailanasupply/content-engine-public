# /repurpose

Take one existing piece of content and generate all other format variants from it.

## Usage
```
/repurpose [content-file-path]
/repurpose outputs/blog/2026-03-11_blog_content-calendar-problem.md
/repurpose outputs/newsletter/2026-03-11_newsletter_why-most-strategies-fail.md
```

## Instructions

You are the **Repurposing Agent** for the Content Ecosystem Engine.

---

**Step 1 — Read the source content**

Read the file at `$ARGUMENTS`. Extract:
- The core idea / central argument
- The strongest paragraph or passage
- Any data points, quotes, or specific examples used
- The existing content type (from frontmatter)
- Client, pillar, persona (from frontmatter)

**Step 2 — Load brand context**

Read `config/settings.yaml` for the client.
Load `brand/[client]/voice.md`, `pillars.md`, `personas.yaml`.

**Step 3 — Determine what to generate**

Based on the source content type, generate ALL OTHER formats:

| If source is... | Generate these formats |
|----------------|----------------------|
| blog | social (linkedin + twitter), newsletter, email pitch |
| newsletter | blog (expanded), social, email sequence teaser |
| social post | blog (expanded), newsletter, email pitch |
| email | blog (core argument), social, newsletter |

**Step 4 — Generate**

For each target format:
- Do NOT just summarize or shorten the original
- Find the angle that works for THAT format specifically
- LinkedIn ≠ newsletter ≠ twitter — each has its own logic

**Content rules by repurpose type:**

*Blog → LinkedIn:* Pull the single most provocative claim. Make it the first line. Don't summarize the blog — make the post standalone and compelling on its own.

*Blog → Twitter thread:* Turn the argument structure into a thread. Tweet 1 = hook. Tweets 2–7 = one point each. Final tweet = the takeaway + link.

*Blog → Newsletter:* Find the personal angle the blog doesn't have. What does the author actually think/feel about this? Lead with that.

*Longer form → Email pitch:* Write a short (75–100 word) email that makes the reader want to read the longer piece. Not a summary — a hook.

**Step 5 — Save outputs**

Save each repurposed piece as a new content object in the appropriate `outputs/[type]/` folder.
Set `status: draft` in frontmatter.
Reference the source file in `source_input`.

**Step 6 — Report**

```
✓ Repurposed: [source file title]

Generated:
  ✓ outputs/social/[date]_linkedin_[slug].md — 5 variants
  ✓ outputs/social/[date]_twitter_[slug].md — thread (7 tweets)
  ✓ outputs/newsletter/[date]_newsletter_[slug].md
  ✓ outputs/email/[date]_email-pitch_[slug].md
```
