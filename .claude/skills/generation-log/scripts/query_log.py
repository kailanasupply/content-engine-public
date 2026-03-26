#!/usr/bin/env python3
"""
query_log.py — Generation log query and management tool.

Reads/writes log/generations.jsonl. Supports filtering, appending,
seeding from cadence-log.yaml, and producing summary views.

Exit codes:
  0 — success (results found, or no results but no error)
  1 — error (file not found, parse error, invalid JSON for --append)
  2 — no log file exists and no seed/append operation requested
"""

import argparse
import json
import os
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict

# Resolve log file path relative to this script's location
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
LOG_FILE = SKILL_DIR / "log" / "generations.jsonl"


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def load_log(log_file: Path) -> list[dict]:
    """Load all entries from the JSONL log. Returns [] if file doesn't exist."""
    if not log_file.exists():
        return []
    entries = []
    with open(log_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[warn] Skipping malformed line {i}: {e}", file=sys.stderr)
    return entries


def append_entry(log_file: Path, entry: dict) -> None:
    """Append a single JSON entry to the log file."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def write_log(log_file: Path, entries: list[dict]) -> None:
    """Overwrite the log file with a list of entries (used by seed)."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def parse_date(d: str) -> date | None:
    """Parse ISO date string. Returns None on failure."""
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def filter_entries(entries: list[dict], args: argparse.Namespace) -> list[dict]:
    """Apply CLI filter flags to entry list."""
    result = entries[:]

    if args.client:
        result = [e for e in result if e.get("client", "").lower() == args.client.lower()]

    if args.format:
        result = [e for e in result if e.get("format", "").lower() == args.format.lower()]

    if args.pillar:
        result = [e for e in result if e.get("pillar", "").lower() == args.pillar.lower()]

    if args.status:
        result = [e for e in result if e.get("status", "").lower() == args.status.lower()]

    if args.days:
        cutoff = date.today() - timedelta(days=args.days)
        result = [e for e in result if parse_date(e.get("date", "")) and parse_date(e.get("date", "")) >= cutoff]

    if args.search:
        query = args.search.lower()
        def matches(e):
            return (
                query in e.get("title", "").lower()
                or query in e.get("angle", "").lower()
                or query in e.get("pillar", "").lower()
            )
        result = [e for e in result if matches(e)]

    if args.last:
        result = result[-args.last:]

    return result


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_entry(e: dict) -> str:
    """Single-entry display line."""
    parts = [
        e.get("date", "????-??-??"),
        f"[{e.get('client', '?')}]",
        f"[{e.get('format', '?')}]",
        e.get("title", "(no title)"),
        f"score={e.get('quality_score', '?')}",
        f"status={e.get('status', '?')}",
    ]
    if e.get("pillar"):
        parts.append(f"pillar={e['pillar']}")
    return "  ".join(parts)


def print_entries(entries: list[dict]) -> None:
    if not entries:
        print("No entries found.")
        return
    for e in entries:
        print(format_entry(e))
    print(f"\n{len(entries)} entry/entries.")


def print_summary(entries: list[dict], args: argparse.Namespace) -> None:
    """Compact summary view for morning scan."""
    if not entries:
        print("No entries in this time window.")
        return

    total = len(entries)
    formats = defaultdict(int)
    pillars = defaultdict(int)
    statuses = defaultdict(int)
    scores = []

    for e in entries:
        formats[e.get("format", "unknown")] += 1
        if e.get("pillar"):
            pillars[e["pillar"]] += 1
        statuses[e.get("status", "unknown")] += 1
        if isinstance(e.get("quality_score"), (int, float)):
            scores.append(e["quality_score"])

    scope = f"last {args.days} days" if args.days else "all time"
    client_scope = f" for {args.client}" if args.client else ""
    print(f"=== Generation Log Summary{client_scope} ({scope}) ===\n")
    print(f"Total pieces: {total}")

    if scores:
        avg = sum(scores) / len(scores)
        print(f"Avg quality score: {avg:.1f}")

    print("\nFormats generated:")
    for fmt, count in sorted(formats.items(), key=lambda x: -x[1]):
        print(f"  {fmt}: {count}")

    print("\nPillars covered:")
    for pillar, count in sorted(pillars.items(), key=lambda x: -x[1]):
        print(f"  {pillar}: {count}")

    print("\nStatus breakdown:")
    for status, count in sorted(statuses.items()):
        print(f"  {status}: {count}")

    drafts = [e for e in entries if e.get("status") == "draft"]
    if drafts:
        print(f"\nDrafts still pending ({len(drafts)}):")
        for e in drafts:
            print(f"  {e.get('date', '?')}  {e.get('format', '?')}  {e.get('title', '(no title)')}")


# ---------------------------------------------------------------------------
# Seed from cadence-log.yaml
# ---------------------------------------------------------------------------

def seed_from_cadence(cadence_path: str, log_file: Path) -> int:
    """
    Read cadence-log.yaml and convert entries to JSONL format.
    Returns number of entries written. Does NOT overwrite existing log —
    appends only entries not already present (matched by date+client+format+title).
    """
    try:
        import yaml
    except ImportError:
        print("Error: PyYAML required. Run: pip install pyyaml --break-system-packages", file=sys.stderr)
        return -1

    cadence_file = Path(cadence_path)
    if not cadence_file.exists():
        print(f"Error: cadence-log.yaml not found at {cadence_path}", file=sys.stderr)
        return -1

    with open(cadence_file, "r", encoding="utf-8") as f:
        raw = f.read()

    # PyYAML may silently resolve duplicate keys; load both values
    data = yaml.safe_load(raw)
    if not data:
        print("Warning: cadence-log.yaml is empty or unparseable.", file=sys.stderr)
        return 0

    # Normalise: data might be a dict with a 'runs' key
    runs = data.get("runs", []) if isinstance(data, dict) else []
    if not runs:
        print("Warning: No 'runs' entries found in cadence-log.yaml.", file=sys.stderr)
        return 0

    existing = load_log(log_file)
    existing_keys = {
        (e.get("date", ""), e.get("client", ""), e.get("format", ""), e.get("title", ""))
        for e in existing
    }

    new_entries = []
    for run in runs:
        if not isinstance(run, dict):
            continue

        # Support two shapes:
        #   1. Flat: each run IS a piece (cadence-log.yaml format)
        #   2. Nested: run has a "pieces" list (future multi-piece runs)
        pieces = run.get("pieces")
        if pieces and isinstance(pieces, list):
            # Nested format — run is a container
            run_date = str(run.get("date", ""))
            client_default = run.get("client", "brian")
            for piece in pieces:
                if not isinstance(piece, dict):
                    continue
                title = piece.get("title") or piece.get("question") or "(untitled)"
                fmt = piece.get("format", "unknown")
                score = piece.get("quality_score") or piece.get("score")
                status = piece.get("status", "draft")
                pillar = piece.get("pillar") or piece.get("content_pillar", "")
                angle = piece.get("angle", "")
                filepath = piece.get("file") or piece.get("output_file", "")
                client = piece.get("client", client_default)

                key = (run_date, client, fmt, title)
                if key in existing_keys:
                    continue
                entry = {"date": run_date, "client": client, "format": fmt, "title": title}
                if score is not None:
                    entry["quality_score"] = score
                if status:
                    entry["status"] = status
                if pillar:
                    entry["pillar"] = pillar
                if angle:
                    entry["angle"] = angle
                if filepath:
                    entry["file"] = filepath
                new_entries.append(entry)
                existing_keys.add(key)
        else:
            # Flat format — the run itself is the piece (cadence-log.yaml)
            run_date = str(run.get("date", ""))
            client = run.get("client", "brian")
            title = run.get("title") or run.get("question") or "(untitled)"
            fmt = run.get("format", "unknown")
            score = run.get("quality_score") or run.get("score")
            status = run.get("status", "draft")
            pillar = run.get("pillar") or run.get("content_pillar") or run.get("content-pillar", "")
            angle = run.get("angle", "")
            filepath = run.get("file") or run.get("output_file", "")

            key = (run_date, client, fmt, title)
            if key in existing_keys:
                continue

            entry = {"date": run_date, "client": client, "format": fmt, "title": title}
            if score is not None:
                entry["quality_score"] = score
            if status:
                entry["status"] = status
            if pillar:
                entry["pillar"] = pillar
            if angle:
                entry["angle"] = angle
            if filepath:
                entry["file"] = filepath

            new_entries.append(entry)
            existing_keys.add(key)

    if not new_entries:
        print("No new entries to import (all already present or no data found).")
        return 0

    for entry in new_entries:
        append_entry(log_file, entry)

    print(f"Seeded {len(new_entries)} entries from {cadence_path}.")
    return len(new_entries)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Query and manage the generation log (log/generations.jsonl).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # What's been generated for Brian this week?
  python query_log.py --client brian --days 7

  # All pieces on the building-in-public pillar, ever
  python query_log.py --pillar building-in-public

  # Last newsletter per client
  python query_log.py --format newsletter --last 1

  # Everything in the last 3 days across all clients
  python query_log.py --days 3

  # Check if a topic has been covered recently
  python query_log.py --search "first-party fraud" --days 30

  # Morning scan summary for a client
  python query_log.py --client brian --days 7 --summary

  # Append a new entry
  python query_log.py --append '{"date": "2026-03-22", "client": "brian", ...}'

  # Seed log from cadence-log.yaml (run once to bootstrap)
  python query_log.py --seed-from performance/cadence-log.yaml
        """,
    )

    # Filter flags
    p.add_argument("--client", help="Filter by client slug (e.g. brian, house-of-fraud)")
    p.add_argument("--format", help="Filter by format (e.g. personal-linkedin, newsletter)")
    p.add_argument("--pillar", help="Filter by content pillar tag")
    p.add_argument("--status", help="Filter by status (draft, approved, rejected, published)")
    p.add_argument("--days", type=int, help="Only entries from the last N days")
    p.add_argument("--search", help="Search titles, angles, and pillars for keyword")
    p.add_argument("--last", type=int, help="Return only the last N entries (after other filters)")

    # Output mode
    p.add_argument("--summary", action="store_true", help="Compact summary view (for morning scan)")

    # Mutation flags
    p.add_argument("--append", metavar="JSON", help="Append a single JSON entry to the log")
    p.add_argument("--seed-from", metavar="PATH", help="Seed log from cadence-log.yaml")

    # Optional log file override
    p.add_argument("--log-file", metavar="PATH", help="Override log file path (default: log/generations.jsonl)")

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Override log file if specified
    log_file = Path(args.log_file) if args.log_file else LOG_FILE

    # -- Seed mode --
    if args.seed_from:
        result = seed_from_cadence(args.seed_from, log_file)
        return 0 if result >= 0 else 1

    # -- Append mode --
    if args.append:
        try:
            entry = json.loads(args.append)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in --append: {e}", file=sys.stderr)
            return 1
        if not isinstance(entry, dict):
            print("Error: --append value must be a JSON object.", file=sys.stderr)
            return 1
        append_entry(log_file, entry)
        print(f"Appended: {json.dumps(entry)}")
        return 0

    # -- Query mode --
    if not log_file.exists():
        print(f"No log file found at {log_file}.")
        print("Run --seed-from performance/cadence-log.yaml to bootstrap, or --append to add entries.")
        return 2

    entries = load_log(log_file)
    if not entries:
        print("Log file is empty.")
        return 0

    filtered = filter_entries(entries, args)

    if args.summary:
        print_summary(filtered, args)
    else:
        print_entries(filtered)

    return 0


if __name__ == "__main__":
    sys.exit(main())
