#!/usr/bin/env python3
"""
mine_evergreen.py — Evergreen idea candidate scanner.

Scans archive/evergreen-candidates/ (and optionally the full archive)
for ideas worth repurposing. Cross-references generation-log to skip
already-used ideas. Scores each candidate against a 5-criterion rubric.

Exit codes:
  0 — candidates found and output written
  1 — error reading files
  2 — no candidates found (archive empty or all already used)
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from collections import defaultdict


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def append_jsonl(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def extract_title_from_file(filepath: Path) -> str:
    """Extract title from markdown file (first H1 or filename)."""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        # Try frontmatter title
        if "title:" in content:
            for line in content.split("\n"):
                if line.strip().startswith("title:"):
                    return line.split(":", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    # Fallback: clean up filename
    stem = filepath.stem
    stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)  # remove date prefix
    stem = re.sub(r"-\[EVERGREEN\]$", "", stem)        # remove EVERGREEN tag
    return stem.replace("-", " ").title()


def extract_date_from_filename(filename: str) -> str | None:
    """Extract YYYY-MM-DD from filename prefix."""
    m = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    return m.group(1) if m else None


def is_evergreen_candidate(filepath: Path) -> bool:
    """Return True if the file is in evergreen-candidates/ or tagged [EVERGREEN]."""
    return (
        "evergreen-candidates" in str(filepath)
        or "[EVERGREEN]" in filepath.name
    )


def extract_client_from_content(filepath: Path, default: str = "brian") -> str:
    """Try to infer client from file content or path."""
    content = ""
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace").lower()
    except Exception:
        pass
    path_str = str(filepath).lower()

    # Check path segments
    for known in ["house-of-fraud", "safeguard", "sayso", "brian"]:
        if known in path_str or known in content[:500]:
            return known
    return default


def extract_pillar_from_content(content: str) -> str:
    """Try to extract content pillar from file content."""
    for line in content.split("\n"):
        line_lower = line.lower()
        if "pillar" in line_lower or "theme" in line_lower:
            # Try to grab the value after a colon or dash
            m = re.search(r"(?:pillar|theme)[:\s]+([a-z0-9\-]+)", line_lower)
            if m:
                return m.group(1)
    # Heuristic from title/content keywords
    keywords = {
        "building-in-public": ["building in public", "lovable", "rebuild", "shipped"],
        "fraud-leadership": ["fraud leader", "fraud program", "head of fraud", "fraud team"],
        "fraud-operations": ["ops review", "alert", "routing", "model", "triage"],
        "ai-disruption": ["ai", "machine learning", "automation", "artificial intelligence"],
        "trust": ["trust", "customer", "first-party", "lied"],
        "career": ["job", "career", "title", "role", "90 days"],
    }
    content_lower = content.lower()
    for pillar, signals in keywords.items():
        if any(s in content_lower for s in signals):
            return pillar
    return "unknown"


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def score_candidate(filepath: Path, content: str, generation_log: list[dict],
                    mined_log: list[dict], client: str | None) -> dict:
    """
    Score a candidate file against the 5-criterion freshness rubric.
    Returns a dict with score breakdown and metadata.
    """
    title = extract_title_from_file(filepath)
    pillar = extract_pillar_from_content(content)
    archived_date = extract_date_from_filename(filepath.name)
    inferred_client = extract_client_from_content(filepath, default=client or "brian")

    # Check generation log for recent use
    title_lower = title.lower()
    recent_uses = [
        e for e in generation_log
        if (title_lower in e.get("title", "").lower()
            or title_lower in e.get("angle", "").lower())
        and e.get("status") in ("approved", "published")
    ]
    any_recent = bool(recent_uses)
    same_angle_recent = any(
        e for e in recent_uses
        if _days_ago(e.get("date", "")) < 90
    )

    # Check if already surfaced in mined log
    already_surfaced = any(
        m for m in mined_log
        if m.get("file", "") == str(filepath)
        and m.get("status") in ("surfaced", "generated")
    )

    # ── Criterion 1: Timelessness ──
    time_signals = ["announced", "launched", "today", "this week", "news", "breaking"]
    timeless_signals = ["always", "rule", "principle", "pattern", "truth", "habit"]
    c1 = 2
    if any(s in content.lower() for s in time_signals):
        c1 = 1
    if sum(1 for s in time_signals if s in content.lower()) >= 3:
        c1 = 0

    # ── Criterion 2: Pillar fit ──
    c2 = 1  # default: adjacent
    if pillar not in ("unknown",):
        c2 = 2
    if pillar == "unknown":
        c2 = 0

    # ── Criterion 3: Hook strength ──
    # Look for specific numbers, dates, names, direct quotes, moments
    hook_signals = [
        r"\d+[%x×]",           # percentages or multipliers
        r"\$[\d,]+",           # dollar amounts
        r'"[^"]{10,50}"',      # quoted phrases
        r"\b(doubled|tripled|overnight|suddenly|the day|the moment|one thing)\b",
        r"\b\d+ (days|months|years|weeks)\b",
    ]
    hook_count = sum(1 for pattern in hook_signals if re.search(pattern, content, re.IGNORECASE))
    c3 = min(2, hook_count)
    # Also give credit for a strong H1 (specific, not generic)
    if re.search(r"^# .{20,}", content, re.MULTILINE):
        c3 = max(c3, 1)

    # ── Criterion 4: Angle freshness ──
    if same_angle_recent:
        c4 = 0
    elif any_recent:
        c4 = 1  # topic covered, but angle may still be fresh
    else:
        c4 = 2

    # ── Criterion 5: Audience match ──
    # Heuristic: fraud/ai/ops content scores 2 for fraud clients
    fraud_signals = ["fraud", "risk", "ops", "analyst", "fintech", "chargeback", "model"]
    audience_match = sum(1 for s in fraud_signals if s in content.lower())
    c5 = min(2, max(0, audience_match - 1))  # needs at least 2 signals for score 1

    total = c1 + c2 + c3 + c4 + c5
    status = "strong" if total >= 7 else ("needs-work" if total >= 5 else "skip")

    # Suggest an angle
    suggested_angle = _suggest_angle(title, pillar, recent_uses)

    return {
        "file": str(filepath),
        "title": title,
        "client": inferred_client,
        "pillar": pillar,
        "archived_date": archived_date,
        "score": total,
        "score_breakdown": {"timelessness": c1, "pillar_fit": c2, "hook_strength": c3,
                             "angle_freshness": c4, "audience_match": c5},
        "status": status,
        "already_surfaced": already_surfaced,
        "recent_uses": len(recent_uses),
        "suggested_angle": suggested_angle,
    }


def _days_ago(date_str: str) -> int:
    """Return how many days ago a YYYY-MM-DD date was. Returns 999 if unparseable."""
    try:
        d = datetime.strptime(str(date_str), "%Y-%m-%d").date()
        return (date.today() - d).days
    except (ValueError, TypeError):
        return 999


def _suggest_angle(title: str, pillar: str, recent_uses: list[dict]) -> str:
    """Generate a suggested repurpose angle based on context."""
    used_angles = [u.get("angle", "") for u in recent_uses if u.get("angle")]

    # Angle ideas keyed to pillar
    angle_suggestions = {
        "building-in-public": [
            "What I got wrong the first time",
            "The numbers nobody shares",
            "Six months later — what actually happened",
        ],
        "fraud-leadership": [
            "The company-side perspective (what the org gets wrong)",
            "The conversation version — what to say in the room",
            "The new-hire's lens (if you're just starting)",
        ],
        "fraud-operations": [
            "The checklist version — what to actually do",
            "The 'before and after' framing",
            "What this looks like at scale vs. early stage",
        ],
        "ai-disruption": [
            "The vendor perspective decoded (what they're not saying)",
            "The skeptic's version — when AI doesn't help",
            "The practitioner's test — one question to ask",
        ],
        "trust": [
            "The cost of getting it wrong",
            "The policy vs. the reality",
            "What this looks like from the customer's side",
        ],
    }

    suggestions = angle_suggestions.get(pillar, [
        "The personal story version",
        "The data-driven angle",
        "The 'what most people miss' frame",
    ])

    # Filter out angles that match recent use
    fresh = [s for s in suggestions if not any(s.lower() in a.lower() for a in used_angles)]
    return fresh[0] if fresh else suggestions[0]


# ---------------------------------------------------------------------------
# Main scan
# ---------------------------------------------------------------------------

def scan(archive_dir: Path, log_path: Path, output_path: Path,
         client_filter: str | None, top_n: int, force: bool,
         since: str | None, full_archive: bool, threshold: int) -> int:
    """
    Main scan function. Returns 0 on success, 1 on error, 2 if no candidates.
    """
    if not archive_dir.exists():
        print(f"Error: Archive directory not found: {archive_dir}", file=sys.stderr)
        return 1

    generation_log = load_jsonl(log_path)
    mined_log = load_jsonl(output_path)

    # Determine which directories to scan
    scan_dirs = [archive_dir / "evergreen-candidates"]
    if full_archive:
        # Also scan monthly archive folders
        for d in archive_dir.iterdir():
            if d.is_dir() and re.match(r"\d{4}-\d{2}", d.name):
                scan_dirs.append(d)

    # Collect candidate files
    candidates = []
    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue
        for filepath in sorted(scan_dir.glob("*.md")):
            if filepath.name == "README.md":
                continue
            # Date filter
            if since:
                file_date = extract_date_from_filename(filepath.name)
                if file_date and file_date < since:
                    continue
            candidates.append(filepath)

    if not candidates:
        print("No candidate files found in archive.")
        return 2

    # Score all candidates
    results = []
    for filepath in candidates:
        content = ""
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[warn] Could not read {filepath}: {e}", file=sys.stderr)
            continue

        scored = score_candidate(filepath, content, generation_log, mined_log, client_filter)

        # Client filter
        if client_filter and scored["client"] != client_filter:
            # Still include if inferred client matches
            pass  # keep it — client inference is imperfect

        # Skip already-surfaced (unless force)
        if scored["already_surfaced"] and not force:
            continue

        results.append(scored)

    # Filter by threshold and sort by score desc
    eligible = [r for r in results if r["score"] >= threshold]
    eligible.sort(key=lambda x: -x["score"])
    top = eligible[:top_n]

    if not top:
        print(f"No candidates scored ≥ {threshold}. Try lowering --threshold or running --full-archive.")
        return 2

    # Print ranked shortlist
    today_str = str(date.today())
    client_label = client_filter or "all clients"
    print(f"\n=== Evergreen Candidates ({client_label}, {today_str}) ===\n")
    for i, r in enumerate(top, 1):
        status_label = {"strong": "strong candidate", "needs-work": "needs refresh", "skip": "borderline"}.get(r["status"], r["status"])
        last_used = f"{r['recent_uses']} recent use(s)" if r["recent_uses"] else "never used"
        print(f"{i}. [SCORE: {r['score']}/10]  \"{r['title']}\"")
        print(f"   File: {r['file']}")
        print(f"   Pillar: {r['pillar']}  |  Client: {r['client']}")
        print(f"   Recommended angle: {r['suggested_angle']}")
        print(f"   Last used: {last_used}")
        print(f"   Status: {status_label}")
        if r["score"] >= 7:
            breakdown = r["score_breakdown"]
            print(f"   Score breakdown: timeless={breakdown['timelessness']} pillar={breakdown['pillar_fit']} "
                  f"hook={breakdown['hook_strength']} freshness={breakdown['angle_freshness']} audience={breakdown['audience_match']}")
        print()

    # Cluster detection
    _report_clusters(top)

    # Append to mined log
    for r in top:
        entry = {
            "date": today_str,
            "client": r["client"],
            "file": r["file"],
            "title": r["title"],
            "score": r["score"],
            "angle": r["suggested_angle"],
            "pillar": r["pillar"],
            "status": "surfaced",
            "used_in": None,
        }
        append_jsonl(output_path, entry)

    print(f"Surfaced {len(top)} candidate(s). Logged to {output_path}")
    return 0


def _report_clusters(top: list[dict]) -> None:
    """If 2+ candidates share a pillar, flag the campaign opportunity."""
    pillar_groups = defaultdict(list)
    for r in top:
        pillar_groups[r["pillar"]].append(r["title"])
    for pillar, titles in pillar_groups.items():
        if len(titles) >= 2 and pillar != "unknown":
            print(f"  → Campaign cluster detected: '{pillar}' — {len(titles)} ideas available")
            for t in titles:
                print(f"    • {t}")
            print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Scan the archive for evergreen idea candidates.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Standard scan for brian
  python mine_evergreen.py --client brian --top 5

  # Monthly deep scan (all archive folders)
  python mine_evergreen.py --full-archive --top 10 --threshold 6

  # Force rescan (re-surface already-surfaced ideas)
  python mine_evergreen.py --client brian --force

  # Only ideas archived since March 2026
  python mine_evergreen.py --since 2026-03-01
        """,
    )

    p.add_argument("--archive", default="archive/", help="Path to archive/ directory")
    p.add_argument("--log", default=".claude/skills/generation-log/log/generations.jsonl",
                   help="Path to generation log JSONL")
    p.add_argument("--output", default=".claude/skills/evergreen-miner/log/mined-ideas.jsonl",
                   help="Path to output mined-ideas.jsonl")
    p.add_argument("--client", help="Filter by client slug")
    p.add_argument("--top", type=int, default=5, help="Return top N candidates (default: 5)")
    p.add_argument("--threshold", type=int, default=5, help="Minimum score to surface (default: 5)")
    p.add_argument("--force", action="store_true", help="Re-surface already-surfaced ideas")
    p.add_argument("--since", metavar="YYYY-MM-DD", help="Only consider ideas archived after this date")
    p.add_argument("--full-archive", action="store_true",
                   help="Scan all archive folders, not just evergreen-candidates/")

    args = p.parse_args()

    archive_dir = Path(args.archive).resolve()
    log_path = Path(args.log).resolve()
    output_path = Path(args.output).resolve()

    return scan(
        archive_dir=archive_dir,
        log_path=log_path,
        output_path=output_path,
        client_filter=args.client,
        top_n=args.top,
        force=args.force,
        since=args.since,
        full_archive=args.full_archive,
        threshold=args.threshold,
    )


if __name__ == "__main__":
    sys.exit(main())
