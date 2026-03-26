---
name: publish-validator
description: Validate a draft file before publishing. Checks frontmatter completeness, required fields, status gate, quality score threshold, and anti-AI scanner status. Use before any /publish run, when reviewing drafts for approval, or when a batch of drafts needs to be checked. Trigger on: "validate before publishing", "check draft", "ready to publish?", "pre-publish check", "/publish", "review drafts for approval", or any time the orchestrator is about to publish a file.
---

# Publish Validator

Pre-publish gate that validates a draft file before it goes live. Catches missing fields, incorrect status, low quality scores, and structural problems before they reach Notion or Airtable.

---

## Running the validator

```bash
# Validate a single file
python .claude/skills/publish-validator/scripts/validate_frontmatter.py drafts/brian/personal-linkedin/2026-03-22_personal_personal-linkedin_fraud-cost-center.md

# Validate all approved files in a client's drafts folder
python .claude/skills/publish-validator/scripts/validate_frontmatter.py drafts/house-of-fraud/ --status approved

# Validate everything in drafts/ (batch mode)
python .claude/skills/publish-validator/scripts/validate_frontmatter.py drafts/ --batch

# Strict mode (fail on warnings, not just errors)
python .claude/skills/publish-validator/scripts/validate_frontmatter.py [file] --strict
```

**Exit codes:**
- `0` — all checks passed (file is ready to publish)
- `1` — validation errors found (do not publish)
- `2` — file not found or unreadable

---

## Validation checklist

### Hard gates (exit 1 if failed — do not publish)

- [ ] **Status = approved** — Only `status: approved` files may be published. `draft`, `review`, `rejected` all block.
- [ ] **quality_score present** — Field must exist in frontmatter.
- [ ] **quality_score ≥ 7** — Pieces scoring below 7 must be rewritten before publishing. Override with `--min-score N`.
- [ ] **Required frontmatter fields** — All of: `id`, `type`, `voice_profile`, `title`, `client`, `platform`, `status`, `created`, `quality_score`
- [ ] **No placeholder text** — Title, quality_notes, and body cannot contain `[PLACEHOLDER]`, `[TODO]`, `[CLIENT_NAME]`, or `FILL IN`.
- [ ] **Word count > 0** — Content must exist below the frontmatter.
- [ ] **No duplicate ID** — The `id` field must not already exist in `output/[client]/` (published content).

### Warnings (reported but do not block unless --strict)

- [ ] **quality_notes present** — Reviewer note field helps track why this scored what it did.
- [ ] **pillar present** — Missing pillar makes performance tracking harder.
- [ ] **persona present** — Missing persona degrades future recommendations.
- [ ] **word_count field matches actual word count** — If the field exists, it should be approximately correct (±20%).
- [ ] **notion_id is null** — If not null, this file may have already been published.
- [ ] **File path matches convention** — Should be `drafts/[client]/[channel]/[YYYY-MM-DD]_[voice]_[channel]_[slug].md`

---

## Validation output format

```
=== Publish Validator ===
File: drafts/brian/personal-linkedin/2026-03-22_personal_personal-linkedin_fraud-cost-center.md

  PASS  status: approved
  PASS  quality_score: 10 (≥ 7)
  PASS  required fields: all present
  PASS  no placeholder text
  PASS  content: 287 words
  WARN  quality_notes: missing (add a reviewer note before publishing)
  WARN  pillar: missing

Result: READY TO PUBLISH (1 warning)
```

Or on failure:
```
  PASS  required fields: all present
  FAIL  status: draft (must be 'approved' to publish)
  FAIL  quality_score: 5 (minimum is 7)

Result: NOT READY — 2 error(s) must be resolved before publishing
```

---

## Batch mode output

In batch mode (`--batch` or directory input), the validator reports a summary table:

```
=== Batch Validation: drafts/brian/ ===

  READY     2026-03-22_personal_personal-linkedin_fraud-cost-center.md   score=10
  NOT READY 2026-03-21_personal_personal-linkedin_ai-jobs.md             status=draft
  NOT READY 2026-03-20_company_company-linkedin_hof-update.md            score=6 (below 7)

Summary: 1 ready, 2 not ready
```

---

## Error log

All validation runs are logged to `log/validation-errors.jsonl`:

```json
{"date": "2026-03-22", "file": "...", "result": "fail", "errors": ["status: draft", "quality_score: 5"], "warnings": ["quality_notes: missing"]}
```

Passed validations are logged with `"result": "pass"` for audit purposes.

---

## Integration with /publish

The `/publish` command calls this validator automatically before pushing to Notion. If the validator returns exit code 1, `/publish` stops and reports the errors. The user must fix the file and re-run.

There is no `--force` flag for publish. If the quality gate blocks a file, the user must either fix it or explicitly lower the minimum score with `--min-score`.

---

## Notes on status management

The engine never sets `status: approved` automatically. Only a human reviewer can approve a draft. This is intentional — the validator enforces that gate.

The valid status flow is:
```
draft → review → approved → published
```

`rejected` is a terminal state — rejected files should be archived, not retried.
