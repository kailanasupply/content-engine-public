#!/usr/bin/env python3
"""
parse_analytics_csv.py

Parse Shield App or LinkedIn Creator Analytics CSV exports and normalize
to structured performance data for syncing into the ContentEngine.

Detects CSV source by inspecting column headers. Normalizes to a standard
performance schema that can be merged with performance/tracker.yaml.

Usage:
    python parse_analytics_csv.py <csv_file> [--source shield|linkedin]

Examples:
    python parse_analytics_csv.py shield-export-march.csv
    python parse_analytics_csv.py linkedin-analytics.csv --source linkedin
    python parse_analytics_csv.py analytics.csv --source shield

Output:
    - Human-readable summary report to stdout
    - Structured JSON array to stdout (after report)
    - Exit code 0 on success, 1 on error

Signal thresholds:
    high   = engagement_rate > 3.0%
    medium = 1.0% ≤ engagement_rate ≤ 3.0%
    low    = engagement_rate < 1.0%
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from difflib import SequenceMatcher

# ============================================================================
# Constants
# ============================================================================

# Engagement rate thresholds (as decimals: 0.03 = 3%)
SIGNAL_HIGH_THRESHOLD = 0.03
SIGNAL_MEDIUM_THRESHOLD = 0.01

# Known column name mappings for each source
SHIELD_APP_COLUMNS = {
    "post": ["post", "content", "message", "text"],
    "date": ["date", "published date", "date published"],
    "impressions": ["impressions", "views", "reach"],
    "engagement_rate": ["engagement rate", "engagement_rate"],
    "reactions": ["reactions", "likes", "reacts"],
    "comments": ["comments"],
    "shares": ["shares", "reposts", "shares/reposts"],
    "clicks": ["clicks", "link clicks", "click"],
}

LINKEDIN_COLUMNS = {
    "post": ["post", "post text", "content", "message", "text"],
    "date": ["published date", "date published", "publication date"],
    "impressions": ["impressions"],
    "unique_impressions": ["unique impressions"],
    "clicks": ["clicks", "engagement clicks"],
    "reactions": ["likes", "reactions", "engagements"],
    "comments": ["comments"],
    "shares": ["reposts", "shares", "reposts/shares"],
    "engagement_rate": ["engagement rate", "engagement_rate"],
    "followers_gained": ["followers gained"],
}

# ============================================================================
# Helper Functions
# ============================================================================


def detect_source(headers):
    """
    Detect CSV source by analyzing column names.
    Returns 'shield', 'linkedin', or None if ambiguous.
    """
    headers_lower = [h.lower().strip() for h in headers]

    linkedin_score = 0
    shield_score = 0

    # Check for LinkedIn-specific columns
    linkedin_markers = ["unique impressions", "followers gained"]
    for marker in linkedin_markers:
        if any(marker in h for h in headers_lower):
            linkedin_score += 2

    # Check for Shield-specific patterns
    shield_markers = ["engagement rate", "clicks", "profile views"]
    for marker in shield_markers:
        if any(marker in h for h in headers_lower):
            shield_score += 1

    if linkedin_score > shield_score:
        return "linkedin"
    elif shield_score > linkedin_score:
        return "shield"
    return None


def find_column_index(headers, column_key, source):
    """
    Find column index by key, using source-specific mappings.
    Returns index or None if not found.
    """
    headers_lower = [h.lower().strip() for h in headers]
    mappings = SHIELD_APP_COLUMNS if source == "shield" else LINKEDIN_COLUMNS

    if column_key not in mappings:
        return None

    for variant in mappings[column_key]:
        for i, header in enumerate(headers_lower):
            if variant in header:
                return i

    return None


def safe_int(value, default=0):
    """Safely convert value to int, return default on error."""
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """Safely convert value to float, return default on error."""
    if value is None or value == "":
        return default
    try:
        # Handle percentages: "5.2%" -> 0.052
        s = str(value).strip().rstrip("%")
        return float(s) / 100 if "%" in str(value) else float(s)
    except (ValueError, TypeError):
        return default


def parse_date(value):
    """Parse date string to ISO format (YYYY-MM-DD)."""
    if not value or value == "":
        return None

    value = str(value).strip()

    # Try common formats
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m/%d/%y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def truncate_title(text, max_chars=80):
    """Truncate text to max_chars, clean up whitespace."""
    if not text:
        return "[untitled]"
    text = str(text).strip()[:max_chars]
    return text if text else "[untitled]"


def calculate_signal(engagement_rate):
    """
    Classify engagement signal based on engagement rate.
    Returns 'high', 'medium', 'low'.
    """
    if engagement_rate > SIGNAL_HIGH_THRESHOLD:
        return "high"
    elif engagement_rate >= SIGNAL_MEDIUM_THRESHOLD:
        return "medium"
    else:
        return "low"


def calculate_engagement_rate(total_engagement, impressions):
    """
    Calculate engagement rate safely.
    Returns decimal (0.05 = 5%), or 0 if impressions is 0.
    """
    if impressions <= 0:
        return 0.0
    return total_engagement / impressions


# ============================================================================
# CSV Parsing
# ============================================================================


def parse_shield_csv(csv_path):
    """
    Parse a Shield App CSV export.
    Returns list of normalized records.
    """
    records = []
    skipped = 0

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                print(f"ERROR: CSV has no headers", file=sys.stderr)
                return None

            headers = reader.fieldnames
            # Find column names by matching against known patterns
            post_col = None
            date_col = None
            impr_col = None
            eng_rate_col = None
            react_col = None
            comm_col = None
            share_col = None
            click_col = None

            headers_lower = {h.lower(): h for h in headers}

            # Match columns by pattern (order matters - be specific first)
            for h_lower, h_orig in headers_lower.items():
                if "post" in h_lower or "text" in h_lower or "content" in h_lower or "message" in h_lower:
                    if post_col is None:  # Take first match
                        post_col = h_orig
                if "date" in h_lower or "published" in h_lower:
                    if date_col is None:
                        date_col = h_orig
                if "impression" in h_lower or "view" in h_lower or "reach" in h_lower:
                    if impr_col is None:
                        impr_col = h_orig
                if "engagement" in h_lower and "rate" in h_lower:
                    if eng_rate_col is None:
                        eng_rate_col = h_orig
                if ("reaction" in h_lower or "like" in h_lower) and "engagement" not in h_lower:
                    if react_col is None:
                        react_col = h_orig
                if "comment" in h_lower:
                    if comm_col is None:
                        comm_col = h_orig
                if "repost" in h_lower or "share" in h_lower:
                    if share_col is None:
                        share_col = h_orig
                if "click" in h_lower:
                    if click_col is None:
                        click_col = h_orig

            for row_num, row in enumerate(reader, start=2):
                try:
                    post_text = row.get(post_col, "") if post_col else ""
                    date_str = row.get(date_col, "") if date_col else ""
                    impressions = safe_int(row.get(impr_col, "")) if impr_col else 0
                    engagement_rate = (
                        safe_float(row.get(eng_rate_col, "")) if eng_rate_col else 0
                    )
                    reactions = safe_int(row.get(react_col, "")) if react_col else 0
                    comments = safe_int(row.get(comm_col, "")) if comm_col else 0
                    shares = safe_int(row.get(share_col, "")) if share_col else 0
                    clicks = safe_int(row.get(click_col, "")) if click_col else 0

                    if not post_text or not date_str:
                        skipped += 1
                        continue

                    date_iso = parse_date(date_str)
                    if not date_iso:
                        skipped += 1
                        continue

                    record = {
                        "title": truncate_title(post_text),
                        "date": date_iso,
                        "impressions": impressions,
                        "engagement_rate": engagement_rate,
                        "reactions": reactions,
                        "comments": comments,
                        "shares": shares,
                        "clicks": clicks,
                        "raw_signal": calculate_signal(engagement_rate),
                        "source": "shield",
                    }

                    records.append(record)

                except (IndexError, KeyError) as e:
                    print(
                        f"WARN: Skipped row {row_num} (malformed): {e}",
                        file=sys.stderr,
                    )
                    skipped += 1
                    continue

    except Exception as e:
        print(f"ERROR: Failed to parse Shield CSV: {e}", file=sys.stderr)
        return None

    if skipped > 0:
        print(f"WARN: Skipped {skipped} malformed rows", file=sys.stderr)

    return records


def parse_linkedin_csv(csv_path):
    """
    Parse a LinkedIn Creator Analytics CSV export.
    Returns list of normalized records.
    """
    records = []
    skipped = 0

    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                print(f"ERROR: CSV has no headers", file=sys.stderr)
                return None

            headers = reader.fieldnames
            # Find column names by matching against known patterns
            post_col = None
            date_col = None
            impr_col = None
            clicks_col = None
            react_col = None
            comm_col = None
            share_col = None
            eng_rate_col = None

            headers_lower = {h.lower(): h for h in headers}

            # Match columns by pattern (order matters - be specific first)
            for h_lower, h_orig in headers_lower.items():
                if "post" in h_lower or "text" in h_lower or "content" in h_lower or "message" in h_lower:
                    if post_col is None:  # Take first match
                        post_col = h_orig
                if "date" in h_lower or "published" in h_lower:
                    if date_col is None:
                        date_col = h_orig
                if "impression" in h_lower and "unique" not in h_lower:
                    if impr_col is None:
                        impr_col = h_orig
                if "click" in h_lower:
                    if clicks_col is None:
                        clicks_col = h_orig
                if ("reaction" in h_lower or "like" in h_lower) and "engagement" not in h_lower:
                    if react_col is None:
                        react_col = h_orig
                if "comment" in h_lower:
                    if comm_col is None:
                        comm_col = h_orig
                if "repost" in h_lower:
                    if share_col is None:
                        share_col = h_orig
                elif "share" in h_lower and "impression" not in h_lower:
                    if share_col is None:
                        share_col = h_orig
                if "engagement" in h_lower and "rate" in h_lower:
                    if eng_rate_col is None:
                        eng_rate_col = h_orig

            for row_num, row in enumerate(reader, start=2):
                try:
                    post_text = row.get(post_col, "") if post_col else ""
                    date_str = row.get(date_col, "") if date_col else ""
                    impressions = safe_int(row.get(impr_col, "")) if impr_col else 0
                    clicks = safe_int(row.get(clicks_col, "")) if clicks_col else 0
                    reactions = safe_int(row.get(react_col, "")) if react_col else 0
                    comments = safe_int(row.get(comm_col, "")) if comm_col else 0
                    shares = safe_int(row.get(share_col, "")) if share_col else 0
                    engagement_rate = (
                        safe_float(row.get(eng_rate_col, "")) if eng_rate_col else 0
                    )

                    if not post_text or not date_str:
                        skipped += 1
                        continue

                    date_iso = parse_date(date_str)
                    if not date_iso:
                        skipped += 1
                        continue

                    # LinkedIn provides engagement_rate directly
                    # If not present, calculate it
                    if engagement_rate == 0 and impressions > 0:
                        total_engagement = reactions + comments + shares
                        engagement_rate = calculate_engagement_rate(
                            total_engagement, impressions
                        )

                    record = {
                        "title": truncate_title(post_text),
                        "date": date_iso,
                        "impressions": impressions,
                        "engagement_rate": engagement_rate,
                        "reactions": reactions,
                        "comments": comments,
                        "shares": shares,
                        "clicks": clicks,
                        "raw_signal": calculate_signal(engagement_rate),
                        "source": "linkedin",
                    }

                    records.append(record)

                except (IndexError, KeyError) as e:
                    print(
                        f"WARN: Skipped row {row_num} (malformed): {e}",
                        file=sys.stderr,
                    )
                    skipped += 1
                    continue

    except Exception as e:
        print(f"ERROR: Failed to parse LinkedIn CSV: {e}", file=sys.stderr)
        return None

    if skipped > 0:
        print(f"WARN: Skipped {skipped} malformed rows", file=sys.stderr)

    return records


# ============================================================================
# Report Generation
# ============================================================================


def generate_report(records, source):
    """Generate a human-readable summary report."""
    if not records:
        return "No records parsed."

    total = len(records)
    high_count = sum(1 for r in records if r["raw_signal"] == "high")
    medium_count = sum(1 for r in records if r["raw_signal"] == "medium")
    low_count = sum(1 for r in records if r["raw_signal"] == "low")

    avg_engagement = sum(r["engagement_rate"] for r in records) / total
    avg_impressions = sum(r["impressions"] for r in records) / total

    report = []
    report.append(f"\n{'='*70}")
    report.append(f"Analytics Import Report — {source.upper()}")
    report.append(f"{'='*70}\n")
    report.append(f"Total posts parsed: {total}")
    report.append(f"Date range: {min(r['date'] for r in records)} to {max(r['date'] for r in records)}")
    report.append(f"\nSignal distribution:")
    report.append(f"  High   (>3%):    {high_count} posts")
    report.append(f"  Medium (1-3%):   {medium_count} posts")
    report.append(f"  Low    (<1%):    {low_count} posts")
    report.append(f"\nAverages:")
    report.append(f"  Engagement rate: {avg_engagement:.2%}")
    report.append(f"  Impressions:     {avg_impressions:.0f}")
    report.append(f"\nTop 3 performers (by engagement rate):")

    sorted_records = sorted(records, key=lambda r: r["engagement_rate"], reverse=True)
    for i, record in enumerate(sorted_records[:3], 1):
        report.append(
            f"  {i}. {record['title'][:60]}... ({record['engagement_rate']:.2%})"
        )

    report.append(f"\n{'='*70}\n")

    return "\n".join(report)


# ============================================================================
# Main
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Parse Shield App or LinkedIn analytics CSV and normalize to JSON.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parse_analytics_csv.py shield-export.csv
  python parse_analytics_csv.py linkedin-analytics.csv --source linkedin
  python parse_analytics_csv.py analytics.csv --source shield

Output:
  - Human-readable report printed to stdout
  - Structured JSON array printed to stdout (after report)
  - Warnings/errors printed to stderr
  - Exit code 0 on success, 1 on error
        """,
    )

    parser.add_argument("csv_file", help="Path to CSV export file")
    parser.add_argument(
        "--source",
        choices=["shield", "linkedin"],
        default=None,
        help="CSV source (auto-detected if not specified)",
    )

    args = parser.parse_args()

    # Validate file
    if not os.path.exists(args.csv_file):
        print(f"ERROR: File not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    # Detect source if not specified
    source = args.source
    if not source:
        with open(args.csv_file, "r", encoding="utf-8") as f:
            headers = next(csv.reader(f))
            detected = detect_source(headers)
            if not detected:
                print(
                    f"ERROR: Could not auto-detect CSV source. Specify --source shield or --source linkedin",
                    file=sys.stderr,
                )
                sys.exit(1)
            source = detected

    # Parse CSV
    if source == "shield":
        records = parse_shield_csv(args.csv_file)
    else:
        records = parse_linkedin_csv(args.csv_file)

    if records is None:
        sys.exit(1)

    if not records:
        print("No records parsed from CSV.", file=sys.stderr)
        sys.exit(1)

    # Generate and print report
    report = generate_report(records, source)
    print(report)

    # Print JSON
    print(json.dumps(records, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
