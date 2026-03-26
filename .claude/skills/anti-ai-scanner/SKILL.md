---
name: anti-ai-scanner
description: >
  Runs a programmatic scan on any draft file to catch banned AI writing words,
  phrases, and sentence patterns before saving. Zero-miss enforcement — the script
  finds every violation with exact line numbers. Use this skill before saving any
  generated draft, when running a quality check, when asked to "scan this for AI
  patterns", "check for banned words", "run the anti-AI scan", or "scrub this draft".
  Also trigger automatically as part of the generation pipeline before the adversarial
  review. This is the fastest gate in the pipeline — run it first, fix violations,
  then pass the clean draft to adversarial-reviewer for the deeper voice check.
---

# Anti-AI Scanner

This skill runs a Python script that deterministically scans a draft for every banned word, phrase, and sentence pattern from `anti-ai-rules.md`. It gives you exact line numbers and specific fix directions. Claude cannot miss a banned word this way — the script catches everything.

The scanner **finds violations**. It does not fix them. You fix them after reviewing the report.

---

## How to run a scan

```bash
python .claude/skills/anti-ai-scanner/scripts/scan_draft.py <path-to-draft>
```

**For a human-readable report** (default):
```bash
python .claude/skills/anti-ai-scanner/scripts/scan_draft.py drafts/brian/personal-linkedin/2026-03-18_personal_personal-linkedin_example.md
```

**For machine-readable JSON output** (useful for programmatic integration):
```bash
python .claude/skills/anti-ai-scanner/scripts/scan_draft.py <path> --json
```

**Strict mode** — treats soft flags as hard bans:
```bash
python .claude/skills/anti-ai-scanner/scripts/scan_draft.py <path> --strict
```

---

## Reading the output

The script produces a report in three sections:

**Hard bans** (exit code 1) — Must fix before saving. Every item here is on the NEVER list from `anti-ai-rules.md`. No exceptions.

**Soft flags** (exit code 0) — Review before saving. These are patterns worth checking but that require judgment (e.g., title case in headers might be intentional in some contexts).

**Context-sensitive** — Words that are banned in some uses but fine in others (e.g., "key" as a noun is fine; "key insight" is not). The script flags them for manual review.

**Exit codes:**
- `0` = Clean — no hard bans. Safe to proceed.
- `1` = Violations found — hard ban patterns present. Fix before saving.
- `2` = File error — file not found or unreadable.

---

## After running the scan

**If exit code 0 (clean):** Report this to the user and proceed to the adversarial review. A clean scan is a necessary condition for saving, not a sufficient one.

**If exit code 1 (violations):** Present the violation report to the user. For each hard ban:
1. Quote the flagged line
2. Explain what the ban is (the script includes this)
3. Ask Claude to rewrite that line — replacing the banned element with the specific thing it was trying to say
4. Re-run the scan on the revised draft until exit code 0

Do not make up a rewrite without knowing the context. If the flagged line needs a specific detail you don't have, ask the user for it.

---

## What the scanner covers

The `scripts/banned_patterns.json` file is the source of truth. It contains:

- **~30 banned words** — "delve", "pivotal", "testament", "meticulous", "vibrant", "robust", "ecosystem" (non-literal), "journey" (metaphorical), and more
- **Banned phrases** — "serves as", "stands as", "not only... but also", "experts argue", "studies show", "align with", etc.
- **Regex sentence patterns** — tacked-on -ing clauses, false significance statements ("is a testament to"), generic openers ("In today's world"), em dashes (—), vague attribution patterns
- **Context-sensitive words** — words that are sometimes fine and sometimes banned, flagged for manual review

The scanner skips YAML frontmatter and quality scorecard comment blocks — it only scans the content body.

---

## Scanning multiple files

To scan all drafts for a client in one pass:
```bash
for f in drafts/brian/personal-linkedin/*.md; do
  echo "--- $f"
  python .claude/skills/anti-ai-scanner/scripts/scan_draft.py "$f"
done
```

Or for a JSON summary of all files:
```bash
for f in drafts/brian/personal-linkedin/*.md; do
  python .claude/skills/anti-ai-scanner/scripts/scan_draft.py "$f" --json
done
```

---

## Updating the banned list

If `anti-ai-rules.md` is updated with new banned words or patterns, update `scripts/banned_patterns.json` to match. The script is only as current as the JSON file.

The JSON file is human-readable — add new entries to `banned_words`, `banned_phrases`, or `banned_patterns` arrays following the existing format. Context-sensitive words go in `banned_words_context_sensitive`.

---

## Important: this is not a substitute for the adversarial review

The scanner catches rule violations. It cannot catch voice drift, weak specificity, or generic framing that violates no explicit rule. Run the scanner first (fast, programmatic), then run adversarial-reviewer (slower, judgment-based) on the clean draft. Both are needed. Neither replaces the other.
