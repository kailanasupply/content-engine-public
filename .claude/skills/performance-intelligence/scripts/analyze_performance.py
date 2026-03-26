#!/usr/bin/env python3
"""
analyze_performance.py

Parses performance/tracker.yaml and performance/cadence-log.yaml.
Writes structured insight files to insights/ and updates performance/insights.md.

Usage:
    python analyze_performance.py \
        --tracker performance/tracker.yaml \
        --cadence performance/cadence-log.yaml \
        --output .claude/skills/performance-intelligence/insights/ \
        --cache .claude/skills/performance-intelligence/cache/last-analysis.json

Exit codes:
    0 — success (or skipped — data unchanged)
    1 — error reading input files
    2 — no data to analyze
"""

import argparse
import hashlib
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_yaml(path):
    """Load a YAML file, return None if missing or unparseable."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR reading {path}: {e}")
        return None


def file_hash(path):
    """MD5 hash of a file's contents, for change detection."""
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def load_cache(cache_path):
    """Load the last-analysis cache."""
    if not os.path.exists(cache_path):
        return {}
    try:
        with open(cache_path, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_cache(cache_path, data):
    """Write the analysis cache."""
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    with open(cache_path, "w") as f:
        json.dump(data, f, indent=2)


def write_file(path, content):
    """Write a file, creating parent dirs as needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_str():
    return datetime.now().strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

def extract_cadence_entries(cadence_data):
    """Pull run entries from cadence-log.yaml. Returns list of dicts."""
    if not cadence_data:
        return []
    entries = []
    # Handle both 'runs' keys (the file has duplicate 'runs' keys — YAML
    # loads the second one; we also check for 'entries' as a fallback)
    runs = cadence_data.get("runs") or []
    if isinstance(runs, list):
        for r in runs:
            if isinstance(r, dict):
                entries.append(r)
    return entries


def extract_tracker_entries(tracker_data):
    """Pull entries from tracker.yaml. Returns list of dicts."""
    if not tracker_data:
        return []
    entries = tracker_data.get("entries") or []
    return [e for e in entries if isinstance(e, dict)]


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze(cadence_entries, tracker_entries):
    """Produce structured analysis dicts from raw entries."""

    results = {
        "by_format": defaultdict(lambda: {"count": 0, "approved": 0, "rejected": 0,
                                           "scores": [], "titles": [], "reaction_strong": 0}),
        "by_client": defaultdict(lambda: {"count": 0, "formats": defaultdict(int),
                                           "scores": [], "approved": 0, "rejected": 0,
                                           "high_performers": [], "rejected_titles": []}),
        "topic_counts": defaultdict(int),
        "title_words": defaultdict(int),
        "quality_distribution": defaultdict(int),
        "rejected_patterns": [],
        "approved_high": [],   # score >= 9 + approved/strong reaction
        "total_entries": 0,
    }

    all_entries = cadence_entries + tracker_entries
    results["total_entries"] = len(all_entries)

    if not all_entries:
        return results

    for entry in all_entries:
        client = entry.get("client", "unknown")
        fmt = entry.get("format", "unknown")
        score = entry.get("quality_score")
        status = entry.get("status", "draft")
        title = entry.get("title") or entry.get("question", "")
        reaction = entry.get("reviewer_reaction", "")
        rejected_note = entry.get("reviewer_note", "")

        # By format
        f = results["by_format"][fmt]
        f["count"] += 1
        if score:
            f["scores"].append(score)
        if title:
            f["titles"].append(title)
        if status == "approved":
            f["approved"] += 1
        elif status == "rejected":
            f["rejected"] += 1
        if reaction and "strong" in reaction.lower():
            f["reaction_strong"] += 1

        # By client
        c = results["by_client"][client]
        c["count"] += 1
        c["formats"][fmt] += 1
        if score:
            c["scores"].append(score)
        if status == "approved":
            c["approved"] += 1
        elif status == "rejected":
            c["rejected"] += 1

        # High performers
        if score and score >= 9 and status in ("approved", "draft"):
            entry_summary = {"title": title, "client": client, "format": fmt,
                             "score": score, "date": entry.get("date", ""),
                             "reaction": reaction}
            if reaction and "strong" in reaction.lower():
                results["approved_high"].insert(0, entry_summary)
            else:
                results["approved_high"].append(entry_summary)

        # Rejected patterns
        if status == "rejected" and title:
            results["rejected_patterns"].append({
                "title": title, "client": client, "format": fmt,
                "note": rejected_note
            })

        # Quality distribution
        if score:
            results["quality_distribution"][score] += 1

        # Topic/title word frequency (crude topic detection)
        if title:
            for word in title.lower().split():
                word = word.strip(".,?!\"'()").rstrip("'s")
                if len(word) > 4 and word not in {
                    "fraud", "about", "their", "which", "where", "there",
                    "these", "those", "would", "could", "should", "that",
                    "your", "what", "when", "will", "from", "with", "have",
                    "this", "into", "than", "then", "them", "they", "just",
                    "only", "every", "does", "going", "still", "first",
                    "house", "brian", "safeguard"
                }:
                    results["title_words"][word] += 1

    return results


def compute_avg(scores):
    if not scores:
        return None
    return round(sum(scores) / len(scores), 1)


# ---------------------------------------------------------------------------
# Report generators
# ---------------------------------------------------------------------------

def gen_by_format(results, date):
    by_fmt = results["by_format"]
    if not by_fmt:
        return "# By Format\n\n*No data yet. Log performance entries to populate this.*\n"

    lines = [
        f"# Performance by Format",
        f"*Generated: {date}*",
        f"*Based on {results['total_entries']} generation log entries*",
        "",
        "---",
        "",
    ]

    # Sort formats by count descending
    for fmt, data in sorted(by_fmt.items(), key=lambda x: -x[1]["count"]):
        avg = compute_avg(data["scores"])
        approve_rate = (data["approved"] / data["count"] * 100) if data["count"] > 0 else 0
        reject_rate = (data["rejected"] / data["count"] * 100) if data["count"] > 0 else 0

        lines.append(f"## {fmt}")
        lines.append(f"**Volume:** {data['count']} pieces generated")
        if avg:
            lines.append(f"**Avg quality score:** {avg}/10")
        lines.append(f"**Approval rate:** {approve_rate:.0f}% | **Rejection rate:** {reject_rate:.0f}%")
        if data["reaction_strong"] > 0:
            lines.append(f"**Strong reviewer reactions:** {data['reaction_strong']}")
        lines.append("")

        # Notable titles
        if data["titles"]:
            sample = data["titles"][:3]
            lines.append("Recent titles:")
            for t in sample:
                lines.append(f"- {t}")
        lines.append("")

    return "\n".join(lines)


def gen_by_client(results, date):
    by_client = results["by_client"]
    if not by_client:
        return "# By Client\n\n*No data yet.*\n"

    lines = [
        f"# Performance by Client",
        f"*Generated: {date}*",
        "",
        "---",
        "",
    ]

    for client, data in sorted(by_client.items(), key=lambda x: -x[1]["count"]):
        avg = compute_avg(data["scores"])
        approve_rate = (data["approved"] / data["count"] * 100) if data["count"] > 0 else 0

        lines.append(f"## {client}")
        lines.append(f"**Total pieces:** {data['count']}")
        if avg:
            lines.append(f"**Avg quality score:** {avg}/10")
        lines.append(f"**Approval rate:** {approve_rate:.0f}%")
        lines.append("")

        # Format breakdown
        if data["formats"]:
            lines.append("Format breakdown:")
            for fmt, count in sorted(data["formats"].items(), key=lambda x: -x[1]):
                lines.append(f"- {fmt}: {count}")
        lines.append("")

    return "\n".join(lines)


def gen_topic_saturation(results, date):
    words = results["title_words"]
    if not words:
        return "# Topic Saturation\n\n*No data yet. Generate more content to track topic frequency.*\n"

    # Topics that appear 3+ times are considered saturated
    saturated = {w: c for w, c in words.items() if c >= 3}
    moderate = {w: c for w, c in words.items() if c == 2}

    lines = [
        f"# Topic Saturation",
        f"*Generated: {date}*",
        f"*Tracks word frequency in titles/questions across all logged pieces.*",
        "",
        "---",
        "",
    ]

    if saturated:
        lines.append("## Saturated topics (covered 3+ times — deprioritize)")
        lines.append("")
        for word, count in sorted(saturated.items(), key=lambda x: -x[1]):
            lines.append(f"- **{word}** — {count} pieces")
        lines.append("")
    else:
        lines.append("## Saturated topics")
        lines.append("")
        lines.append("*No topics saturated yet (threshold: 3+ pieces).*")
        lines.append("")

    if moderate:
        lines.append("## Moderate coverage (covered twice — use with a fresh angle)")
        lines.append("")
        for word, count in sorted(moderate.items(), key=lambda x: -x[1]):
            lines.append(f"- **{word}** — {count} pieces")
        lines.append("")

    # Rejected patterns note
    if results["rejected_patterns"]:
        lines.append("## Angles that were rejected")
        lines.append("")
        lines.append("Do not repeat these angles — they were rejected by the reviewer.")
        lines.append("")
        for r in results["rejected_patterns"]:
            note = f" ({r['note']})" if r["note"] else ""
            lines.append(f"- [{r['client']}/{r['format']}] {r['title']}{note}")
        lines.append("")

    return "\n".join(lines)


def gen_structural_patterns(results, date):
    approved_high = results["approved_high"]
    quality_dist = results["quality_distribution"]

    lines = [
        f"# Structural Patterns",
        f"*Generated: {date}*",
        "",
        "---",
        "",
    ]

    # Quality score distribution
    if quality_dist:
        lines.append("## Quality score distribution")
        lines.append("")
        total = sum(quality_dist.values())
        for score in sorted(quality_dist.keys(), reverse=True):
            count = quality_dist[score]
            bar = "█" * count
            lines.append(f"- {score}/10: {bar} ({count} pieces, {count/total*100:.0f}%)")
        lines.append("")
        avg_all = compute_avg([s for s, c in quality_dist.items() for _ in range(c)])
        if avg_all:
            lines.append(f"**Average quality score across all pieces: {avg_all}/10**")
        lines.append("")

    # Top performers
    if approved_high:
        lines.append("## Top-performing pieces (score ≥ 9, approved or strong reaction)")
        lines.append("")
        lines.append("Patterns in what's landing well:")
        lines.append("")
        for item in approved_high[:8]:
            reaction_note = f" ⭐ {item['reaction']}" if item.get("reaction") else ""
            lines.append(f"- [{item['client']}/{item['format']}] **{item['title']}** "
                         f"(score: {item['score']}{reaction_note})")
        lines.append("")

        # Extract rough structural observations
        lines.append("## Observations from top performers")
        lines.append("")
        lines.append("These patterns appear in pieces scoring 9–10:")
        lines.append("")

        # Count format distribution among top performers
        fmt_counts = defaultdict(int)
        for item in approved_high:
            fmt_counts[item["format"]] += 1
        top_formats = sorted(fmt_counts.items(), key=lambda x: -x[1])
        if top_formats:
            lines.append(f"**Formats producing top scores:** "
                         f"{', '.join(f'{f} ({c})' for f, c in top_formats)}")
            lines.append("")

        lines.append("*Note: Add structural detail (hook type, length, CTA approach) to "
                     "`performance/tracker.yaml` entries to generate richer pattern analysis.*")
        lines.append("")

    if not approved_high and not quality_dist:
        lines.append("*No data yet. Log performance data to populate this.*")

    return "\n".join(lines)


def gen_main_insights_update(results, date):
    """A summary block suitable for writing back to performance/insights.md."""
    total = results["total_entries"]
    by_fmt = results["by_format"]

    approved_total = sum(d["approved"] for d in by_fmt.values())
    rejected_total = sum(d["rejected"] for d in results["by_client"].values())
    all_scores = [s for d in by_fmt.values() for s in d["scores"]]
    avg = compute_avg(all_scores)

    lines = [
        f"# Performance Insights",
        f"",
        f"## How to read this file",
        f"",
        f"This file is the engine's memory. It summarizes what has and hasn't worked",
        f"across all tracked content so the orchestrator can make informed decisions",
        f"about what to generate next.",
        f"",
        f"Run `/synthesize-learnings` after logging 5+ new performance entries",
        f"to update this file with fresh patterns.",
        f"",
        f"---",
        f"",
        f"## Last updated",
        f"{date}",
        f"",
        f"## Entries analyzed",
        f"{total}",
        f"",
        f"---",
        f"",
        f"## What's working",
        f"",
    ]

    if results["approved_high"]:
        lines.append("Top-scoring pieces and formats — see "
                     "`.claude/skills/performance-intelligence/insights/` for full analysis.")
        lines.append("")
        for item in results["approved_high"][:5]:
            lines.append(f"- **{item['title']}** [{item['client']}/{item['format']}] "
                         f"score {item['score']}")
        lines.append("")
    else:
        lines.append("[Not yet populated — run /synthesize-learnings after logging performance data]")
        lines.append("")

    lines += [
        f"---",
        f"",
        f"## What's not working",
        f"",
    ]

    if results["rejected_patterns"]:
        for r in results["rejected_patterns"]:
            note = f" — {r['note']}" if r["note"] else ""
            lines.append(f"- **{r['title']}** [{r['client']}/{r['format']}]{note}")
        lines.append("")
    else:
        lines.append("[Not yet populated]")
        lines.append("")

    # Topic saturation
    saturated = {w: c for w, c in results["title_words"].items() if c >= 3}
    lines += [
        f"---",
        f"",
        f"## Topics that are saturated",
        f"",
    ]
    if saturated:
        for word, count in sorted(saturated.items(), key=lambda x: -x[1]):
            lines.append(f"- **{word}** ({count} pieces in log)")
        lines.append("")
    else:
        lines.append("[None yet — threshold is 3+ pieces on the same topic]")
        lines.append("")

    lines += [
        f"---",
        f"",
        f"## Topics with untapped potential",
        f"",
        f"[Not yet populated — requires tracker.yaml engagement data]",
        f"",
        f"---",
        f"",
        f"## Format observations",
        f"",
    ]

    if by_fmt:
        for fmt, data in sorted(by_fmt.items(), key=lambda x: -x[1]["count"]):
            avg_fmt = compute_avg(data["scores"])
            if avg_fmt:
                lines.append(f"- **{fmt}**: {data['count']} pieces, avg score {avg_fmt}/10")
        lines.append("")
    else:
        lines.append("[Not yet populated]")
        lines.append("")

    lines += [
        f"---",
        f"",
        f"## Cadence observations",
        f"",
        f"[Not yet populated — requires tracker.yaml engagement data]",
        f"",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Analyze ContentEngine performance data.")
    parser.add_argument("--tracker", default="performance/tracker.yaml")
    parser.add_argument("--cadence", default="performance/cadence-log.yaml")
    parser.add_argument("--output", default=".claude/skills/performance-intelligence/insights/")
    parser.add_argument("--cache", default=".claude/skills/performance-intelligence/cache/last-analysis.json")
    parser.add_argument("--force", action="store_true", help="Force re-analysis even if data unchanged")
    parser.add_argument("--insights-file", default="performance/insights.md",
                        help="Path to main insights.md to update")
    args = parser.parse_args()

    # Change to repo root if called from a subdirectory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Try to find repo root (parent of .claude/)
    candidate = script_dir
    for _ in range(5):
        if os.path.exists(os.path.join(candidate, "CLAUDE.md")):
            os.chdir(candidate)
            break
        candidate = os.path.dirname(candidate)

    # Check for data changes
    tracker_hash = file_hash(args.tracker)
    cadence_hash = file_hash(args.cadence)
    cache = load_cache(args.cache)

    if (not args.force
            and cache.get("tracker_hash") == tracker_hash
            and cache.get("cadence_hash") == cadence_hash
            and tracker_hash is not None):
        print(f"Data unchanged since {cache.get('last_run', 'unknown')}. Skipping re-analysis.")
        print("Use --force to re-run anyway.")
        sys.exit(0)

    # Load data
    tracker_data = load_yaml(args.tracker)
    cadence_data = load_yaml(args.cadence)

    cadence_entries = extract_cadence_entries(cadence_data)
    tracker_entries = extract_tracker_entries(tracker_data)
    total = len(cadence_entries) + len(tracker_entries)

    if total == 0:
        print("No data to analyze. Add entries to tracker.yaml or cadence-log.yaml first.")
        sys.exit(2)

    print(f"Analyzing {total} entries ({len(cadence_entries)} from cadence-log, "
          f"{len(tracker_entries)} from tracker)...")

    results = analyze(cadence_entries, tracker_entries)
    date = today_str()

    # Write insight files
    os.makedirs(args.output, exist_ok=True)

    write_file(os.path.join(args.output, "by-format.md"), gen_by_format(results, date))
    print(f"  → {args.output}by-format.md")

    write_file(os.path.join(args.output, "by-client.md"), gen_by_client(results, date))
    print(f"  → {args.output}by-client.md")

    write_file(os.path.join(args.output, "topic-saturation.md"),
               gen_topic_saturation(results, date))
    print(f"  → {args.output}topic-saturation.md")

    write_file(os.path.join(args.output, "structural-patterns.md"),
               gen_structural_patterns(results, date))
    print(f"  → {args.output}structural-patterns.md")

    # Update main insights.md
    if args.insights_file:
        write_file(args.insights_file, gen_main_insights_update(results, date))
        print(f"  → {args.insights_file}")

    # Update cache
    save_cache(args.cache, {
        "last_run": now_iso(),
        "tracker_hash": tracker_hash,
        "cadence_hash": cadence_hash,
        "entries_analyzed": total,
    })
    print(f"\nAnalysis complete. {total} entries processed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
