#!/usr/bin/env python3
"""
validate_frontmatter.py — Pre-publish validation for draft content files.

Checks frontmatter completeness, status gate, quality score, placeholder text,
and content existence. Logs all runs to log/validation-errors.jsonl.

Exit codes:
  0 — all hard gates passed (file is ready to publish)
  1 — validation errors found (do not publish)
  2 — file not found or unreadable
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = [
    "id", "type", "voice_profile", "title", "client",
    "platform", "status", "created", "quality_score",
]

WARNING_FIELDS = ["quality_notes", "pillar", "persona", "word_count"]

PLACEHOLDER_PATTERNS = [
    r"\[PLACEHOLDER\]", r"\[TODO\]", r"\[CLIENT_NAME\]",
    r"FILL IN", r"\[INSERT\]", r"\[YOUR_", r"\[ADD ",
]

VALID_STATUSES_FOR_PUBLISH = {"approved"}

FILE_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2}_(personal|company)_[\w\-]+_[\w\-]+\.md$"
)


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from markdown content.
    Returns (frontmatter_dict, body_text).
    """
    if not content.startswith("---"):
        return {}, content

    # Find closing ---
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content

    fm_text = content[3:end].strip()
    body = content[end + 4:].strip()

    frontmatter = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            # Normalise null/None values
            if value.lower() in ("null", "none", "~", ""):
                value = None
            # Normalise booleans
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            else:
                # Try numeric
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        # Strip quotes
                        value = value.strip('"').strip("'")
            frontmatter[key] = value

    return frontmatter, body


def count_words(text: str) -> int:
    """Count words in body text, excluding frontmatter markers."""
    # Remove markdown headers
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    # Remove YAML-like lines
    text = re.sub(r"^\w+:.*$", "", text, flags=re.MULTILINE)
    words = text.split()
    return len(words)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

class ValidationResult:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    @property
    def is_ready(self) -> bool:
        return len(self.errors) == 0

    def add_pass(self, msg: str) -> None:
        self.passes.append(msg)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def validate_file(filepath: Path, min_score: int = 7, strict: bool = False,
                  status_filter: str | None = None) -> ValidationResult:
    result = ValidationResult(str(filepath))

    if not filepath.exists():
        result.add_error(f"File not found: {filepath}")
        return result

    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        result.add_error(f"Cannot read file: {e}")
        return result

    frontmatter, body = parse_frontmatter(content)

    # ── Status filter (for batch mode) ──
    if status_filter:
        file_status = str(frontmatter.get("status", "")).lower()
        if file_status != status_filter.lower():
            # Return a "skip" result — not a failure, just not matching the filter
            result.add_pass(f"skipped (status={file_status}, filter={status_filter})")
            return result

    # ── Hard gate: status ──
    status = str(frontmatter.get("status", "")).lower()
    if status in VALID_STATUSES_FOR_PUBLISH:
        result.add_pass(f"status: {status}")
    else:
        result.add_error(f"status: {status} (must be 'approved' to publish)")

    # ── Hard gate: quality_score ──
    quality_score = frontmatter.get("quality_score")
    if quality_score is None:
        result.add_error("quality_score: missing (required field)")
    else:
        try:
            score_val = int(quality_score)
            if score_val >= min_score:
                result.add_pass(f"quality_score: {score_val} (≥ {min_score})")
            else:
                result.add_error(f"quality_score: {score_val} (minimum is {min_score})")
        except (ValueError, TypeError):
            result.add_error(f"quality_score: '{quality_score}' is not a valid integer")

    # ── Hard gate: required fields ──
    missing = [f for f in REQUIRED_FIELDS if f not in frontmatter or frontmatter[f] is None]
    # quality_score already checked above
    missing = [f for f in missing if f != "quality_score"]
    if missing:
        for f in missing:
            result.add_error(f"required field missing: '{f}'")
    else:
        result.add_pass("required fields: all present")

    # ── Hard gate: placeholder text ──
    combined = content
    has_placeholder = any(re.search(p, combined, re.IGNORECASE) for p in PLACEHOLDER_PATTERNS)
    if has_placeholder:
        result.add_error("placeholder text found in content (remove before publishing)")
    else:
        result.add_pass("no placeholder text")

    # ── Hard gate: content exists ──
    word_count = count_words(body)
    if word_count == 0:
        result.add_error("content: empty body (no text below frontmatter)")
    elif word_count < 20:
        result.add_error(f"content: only {word_count} words — too short to be a real draft")
    else:
        result.add_pass(f"content: {word_count} words")

    # ── Warning: optional recommended fields ──
    for field in WARNING_FIELDS:
        if field == "quality_notes":
            val = frontmatter.get("quality_notes")
            if not val:
                result.add_warning("quality_notes: missing (add a reviewer note before publishing)")
        elif field == "word_count":
            declared = frontmatter.get("word_count")
            if declared is not None:
                try:
                    declared_int = int(declared)
                    # Allow ±30% tolerance
                    if word_count > 0 and abs(declared_int - word_count) / max(word_count, 1) > 0.30:
                        result.add_warning(
                            f"word_count: declared={declared_int} but actual={word_count} (>30% discrepancy)"
                        )
                except (ValueError, TypeError):
                    pass
        else:
            if not frontmatter.get(field):
                result.add_warning(f"{field}: missing")

    # ── Warning: notion_id already set ──
    notion_id = frontmatter.get("notion_id")
    if notion_id and str(notion_id).lower() not in ("null", "none", ""):
        result.add_warning(f"notion_id is already set ({notion_id}) — may have been published already")

    # ── Warning: file path convention ──
    if not FILE_PATTERN.search(filepath.name):
        result.add_warning(
            f"filename doesn't match convention YYYY-MM-DD_[voice]_[channel]_[slug].md"
        )

    # In strict mode, warnings become errors
    if strict and result.warnings:
        result.errors.extend([f"(strict) {w}" for w in result.warnings])
        result.warnings.clear()

    return result


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def print_result(result: ValidationResult, verbose: bool = True) -> None:
    if verbose:
        print(f"\n=== Publish Validator ===")
        print(f"File: {result.filepath}\n")

    for msg in result.passes:
        print(f"  PASS  {msg}")
    for msg in result.errors:
        print(f"  FAIL  {msg}")
    for msg in result.warnings:
        print(f"  WARN  {msg}")

    if result.is_ready:
        warn_note = f" ({len(result.warnings)} warning(s))" if result.warnings else ""
        print(f"\nResult: READY TO PUBLISH{warn_note}")
    else:
        print(f"\nResult: NOT READY — {len(result.errors)} error(s) must be resolved before publishing")


def log_result(result: ValidationResult, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "date": str(date.today()),
        "file": result.filepath,
        "result": "pass" if result.is_ready else "fail",
        "errors": result.errors,
        "warnings": result.warnings,
    }
    with open(log_path, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Batch mode
# ---------------------------------------------------------------------------

def batch_validate(target: Path, min_score: int, strict: bool,
                   status_filter: str | None, log_path: Path) -> int:
    """Validate all .md files under target. Returns 0 if all pass, 1 if any fail."""
    if not target.exists():
        print(f"Error: Path not found: {target}", file=sys.stderr)
        return 2

    files = sorted(target.rglob("*.md")) if target.is_dir() else [target]
    files = [f for f in files if f.name != "README.md"]

    if not files:
        print("No .md files found.")
        return 0

    print(f"\n=== Batch Validation: {target} ===\n")

    ready = []
    not_ready = []
    skipped = []

    for filepath in files:
        result = validate_file(filepath, min_score=min_score, strict=strict,
                                status_filter=status_filter)
        log_result(result, log_path)

        # Detect "skipped" results
        if result.passes and result.passes[0].startswith("skipped"):
            skipped.append(filepath.name)
            continue

        score = None
        status = None
        for msg in result.passes + result.errors:
            if "quality_score:" in msg:
                m = re.search(r"quality_score: (\d+)", msg)
                if m:
                    score = int(m.group(1))
            if "status:" in msg:
                m = re.search(r"status: (\w+)", msg)
                if m:
                    status = m.group(1)

        score_str = f"score={score}" if score is not None else ""
        status_str = f"status={status}" if status else ""
        detail = "  ".join(filter(None, [score_str, status_str]))

        first_error = result.errors[0] if result.errors else ""

        if result.is_ready:
            print(f"  READY     {filepath.name:<60} {detail}")
            ready.append(filepath.name)
        else:
            print(f"  NOT READY {filepath.name:<60} {first_error}")
            not_ready.append(filepath.name)

    print(f"\nSummary: {len(ready)} ready, {len(not_ready)} not ready", end="")
    if skipped:
        print(f", {len(skipped)} skipped (status filter)", end="")
    print()

    return 1 if not_ready else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Validate draft files before publishing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  python validate_frontmatter.py drafts/brian/personal-linkedin/2026-03-22_personal_personal-linkedin_slug.md

  # Validate all approved files in a directory
  python validate_frontmatter.py drafts/brian/ --status approved

  # Validate everything in batch mode
  python validate_frontmatter.py drafts/ --batch

  # Strict mode (warnings become errors)
  python validate_frontmatter.py drafts/brian/personal-linkedin/2026-03-22_*.md --strict

  # Override minimum score threshold
  python validate_frontmatter.py drafts/some-file.md --min-score 8
        """,
    )

    p.add_argument("path", help="File or directory to validate")
    p.add_argument("--min-score", type=int, default=7, help="Minimum quality score (default: 7)")
    p.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    p.add_argument("--status", help="Only validate files with this status (e.g. 'approved')")
    p.add_argument("--batch", action="store_true", help="Batch mode (summary table output)")
    p.add_argument("--log", default=".claude/skills/publish-validator/log/validation-errors.jsonl",
                   help="Path to error log JSONL")
    p.add_argument("--quiet", action="store_true", help="Suppress per-check output (batch mode)")

    args = p.parse_args()
    log_path = Path(args.log).resolve()
    target = Path(args.path).resolve()

    # Batch mode if directory or --batch flag
    if target.is_dir() or args.batch:
        return batch_validate(target, args.min_score, args.strict, args.status, log_path)

    # Single file mode
    if not target.exists():
        print(f"Error: File not found: {target}", file=sys.stderr)
        return 2

    result = validate_file(target, min_score=args.min_score, strict=args.strict,
                            status_filter=args.status)
    log_result(result, log_path)
    print_result(result, verbose=not args.quiet)

    return 0 if result.is_ready else 1


if __name__ == "__main__":
    sys.exit(main())
