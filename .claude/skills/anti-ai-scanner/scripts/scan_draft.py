#!/usr/bin/env python3
"""
anti-ai-scanner: Scans a draft markdown file for banned AI writing patterns.

Usage:
    python scan_draft.py <file_path> [--json] [--strict]

Arguments:
    file_path   Path to the markdown file to scan
    --json      Output raw JSON (for programmatic use)
    --strict    Treat soft_flag patterns as hard_ban (stricter mode)

Exit codes:
    0 = Clean (no hard_ban violations found)
    1 = Violations found (hard_ban patterns)
    2 = File error (file not found, unreadable, etc.)
"""

import sys
import re
import json
import os
from pathlib import Path

# Load banned patterns from the JSON file in the same directory
SCRIPT_DIR = Path(__file__).parent
PATTERNS_FILE = SCRIPT_DIR / "banned_patterns.json"


def load_patterns():
    """Load banned patterns from the JSON config file."""
    if not PATTERNS_FILE.exists():
        print(f"ERROR: banned_patterns.json not found at {PATTERNS_FILE}", file=sys.stderr)
        sys.exit(2)
    with open(PATTERNS_FILE, "r") as f:
        return json.load(f)


def strip_frontmatter(content):
    """Remove YAML frontmatter from markdown files. Returns (frontmatter, body)."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            frontmatter = content[:end + 4]
            body = content[end + 4:].lstrip("\n")
            return frontmatter, body
    return "", content


def strip_quality_scorecard(content):
    """Remove the HTML comment quality scorecard block at end of drafts."""
    # Remove <!-- QUALITY GATE SCORECARD ... --> blocks
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    return content


def scan_banned_words(lines, patterns_data, strict=False):
    """Scan for banned individual words."""
    violations = []
    banned_words = set(w.lower() for w in patterns_data.get("banned_words", []))

    for line_num, line in enumerate(lines, 1):
        # Skip markdown headers and frontmatter markers
        stripped = line.strip()
        if stripped.startswith("#") or stripped == "---":
            continue

        words_in_line = re.findall(r'\b[a-zA-Z]+\b', line)
        for word in words_in_line:
            if word.lower() in banned_words:
                violations.append({
                    "type": "banned_word",
                    "severity": "hard_ban",
                    "line_number": line_num,
                    "line_text": line.rstrip(),
                    "matched": word,
                    "description": f"Banned word: '{word}'. Remove or replace with specific language.",
                })

    return violations


def scan_banned_phrases(lines, patterns_data):
    """Scan for banned multi-word phrases."""
    violations = []
    banned_phrases = patterns_data.get("banned_phrases", [])

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped == "---":
            continue

        line_lower = line.lower()
        for phrase in banned_phrases:
            if phrase.lower() in line_lower:
                violations.append({
                    "type": "banned_phrase",
                    "severity": "hard_ban",
                    "line_number": line_num,
                    "line_text": line.rstrip(),
                    "matched": phrase,
                    "description": f"Banned phrase: '{phrase}'. Replace with direct, specific language.",
                })

    return violations


def scan_patterns(lines, patterns_data, strict=False):
    """Scan for banned regex sentence patterns."""
    violations = []
    full_text = "\n".join(lines)
    banned_patterns = patterns_data.get("banned_patterns", [])

    for pattern_def in banned_patterns:
        severity = pattern_def.get("severity", "hard_ban")
        if severity == "soft_flag" and not strict:
            # Still scan, but mark as soft
            pass

        try:
            regex = re.compile(pattern_def["regex"], re.IGNORECASE | re.MULTILINE)
        except re.error as e:
            continue  # Skip malformed patterns

        for match in regex.finditer(full_text):
            # Find line number
            line_num = full_text[:match.start()].count("\n") + 1
            line_text = lines[line_num - 1] if line_num <= len(lines) else ""

            # Skip matches inside YAML frontmatter comments or scorecard blocks
            if line_text.strip().startswith("<!--") or line_text.strip().startswith("---"):
                continue

            violations.append({
                "type": "pattern_violation",
                "severity": severity,
                "pattern_name": pattern_def["name"],
                "line_number": line_num,
                "line_text": line_text.rstrip(),
                "matched": match.group(0)[:100],  # Cap match display at 100 chars
                "description": pattern_def["description"],
                "example_fix": pattern_def.get("fix", ""),
            })

    return violations


def scan_context_sensitive(lines, patterns_data):
    """Scan for context-sensitive words that may or may not be violations."""
    candidates = []
    context_words = patterns_data.get("banned_words_context_sensitive", [])

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped == "---":
            continue

        for entry in context_words:
            word = entry["word"]
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            if pattern.search(line):
                candidates.append({
                    "type": "context_sensitive",
                    "severity": "review_needed",
                    "line_number": line_num,
                    "line_text": line.rstrip(),
                    "matched": entry["flag_as"],
                    "description": entry["note"],
                })

    return candidates


def deduplicate_violations(violations):
    """Remove near-duplicate violations (same line, same match)."""
    seen = set()
    unique = []
    for v in violations:
        key = (v.get("line_number"), v.get("matched", "").lower()[:30])
        if key not in seen:
            seen.add(key)
            unique.append(v)
    return unique


def format_report(file_path, violations, context_candidates, strict=False):
    """Format a human-readable scan report."""
    hard_bans = [v for v in violations if v.get("severity") == "hard_ban"]
    soft_flags = [v for v in violations if v.get("severity") == "soft_flag"]

    lines = []
    lines.append("=" * 60)
    lines.append(f"ANTI-AI SCAN REPORT")
    lines.append(f"File: {file_path}")
    lines.append("=" * 60)

    if not hard_bans and not soft_flags and not context_candidates:
        lines.append("")
        lines.append("✅ CLEAN — No violations found.")
        lines.append("")
        lines.append("This draft passed the anti-AI scan. No banned words,")
        lines.append("banned phrases, or sentence pattern violations detected.")
        return "\n".join(lines)

    # Summary
    lines.append("")
    status = "🚫 VIOLATIONS FOUND" if hard_bans else "⚠️  REVIEW NEEDED"
    lines.append(f"Status: {status}")
    lines.append(f"Hard bans (must fix): {len(hard_bans)}")
    lines.append(f"Soft flags (review):  {len(soft_flags)}")
    lines.append(f"Context-sensitive:    {len(context_candidates)}")
    lines.append("")

    if hard_bans:
        lines.append("─" * 60)
        lines.append("HARD BANS — Must fix before saving")
        lines.append("─" * 60)
        for i, v in enumerate(hard_bans, 1):
            lines.append(f"\n[{i}] Line {v['line_number']} — {v.get('pattern_name', v['type'])}")
            lines.append(f"    Match:   \"{v['matched']}\"")
            lines.append(f"    Text:    {v['line_text'][:120]}")
            lines.append(f"    Why:     {v['description']}")
            if v.get("example_fix"):
                lines.append(f"    Fix:     {v['example_fix']}")

    if soft_flags:
        lines.append("")
        lines.append("─" * 60)
        lines.append("SOFT FLAGS — Review before saving")
        lines.append("─" * 60)
        for i, v in enumerate(soft_flags, 1):
            lines.append(f"\n[{i}] Line {v['line_number']} — {v.get('pattern_name', v['type'])}")
            lines.append(f"    Match:   \"{v['matched']}\"")
            lines.append(f"    Text:    {v['line_text'][:120]}")
            lines.append(f"    Why:     {v['description']}")

    if context_candidates:
        lines.append("")
        lines.append("─" * 60)
        lines.append("CONTEXT-SENSITIVE — Manual check required")
        lines.append("─" * 60)
        lines.append("These words are banned in some contexts but OK in others.")
        lines.append("Review each and decide.")
        for i, v in enumerate(context_candidates, 1):
            lines.append(f"\n[{i}] Line {v['line_number']} — {v['matched']}")
            lines.append(f"    Text:    {v['line_text'][:120]}")
            lines.append(f"    Note:    {v['description']}")

    lines.append("")
    lines.append("─" * 60)
    lines.append("The scanner finds violations. Claude or the human fixes them.")
    lines.append("Do not save this draft until all hard bans are resolved.")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan_draft.py <file_path> [--json] [--strict]")
        sys.exit(2)

    file_path = sys.argv[1]
    output_json = "--json" in sys.argv
    strict_mode = "--strict" in sys.argv

    # Read file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_content = f.read()
    except FileNotFoundError:
        error = {"error": f"File not found: {file_path}"}
        if output_json:
            print(json.dumps(error))
        else:
            print(f"ERROR: File not found: {file_path}")
        sys.exit(2)
    except Exception as e:
        error = {"error": str(e)}
        if output_json:
            print(json.dumps(error))
        else:
            print(f"ERROR: {e}")
        sys.exit(2)

    # Load patterns
    patterns_data = load_patterns()

    # Strip frontmatter and quality scorecard before scanning
    _, body = strip_frontmatter(raw_content)
    body = strip_quality_scorecard(body)
    lines = body.split("\n")

    # Run all scans
    word_violations = scan_banned_words(lines, patterns_data, strict_mode)
    phrase_violations = scan_banned_phrases(lines, patterns_data)
    pattern_violations = scan_patterns(lines, patterns_data, strict_mode)
    context_candidates = scan_context_sensitive(lines, patterns_data)

    # Combine and deduplicate
    all_violations = deduplicate_violations(
        word_violations + phrase_violations + pattern_violations
    )

    # Sort by line number
    all_violations.sort(key=lambda v: v.get("line_number", 0))
    context_candidates.sort(key=lambda v: v.get("line_number", 0))

    hard_bans = [v for v in all_violations if v.get("severity") == "hard_ban"]
    has_violations = len(hard_bans) > 0

    if output_json:
        result = {
            "file": file_path,
            "clean": not has_violations,
            "hard_ban_count": len(hard_bans),
            "soft_flag_count": len([v for v in all_violations if v.get("severity") == "soft_flag"]),
            "context_sensitive_count": len(context_candidates),
            "violations": all_violations,
            "context_sensitive": context_candidates,
        }
        print(json.dumps(result, indent=2))
    else:
        report = format_report(file_path, all_violations, context_candidates, strict_mode)
        print(report)

    sys.exit(1 if has_violations else 0)


if __name__ == "__main__":
    main()
