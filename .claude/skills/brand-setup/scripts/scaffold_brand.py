#!/usr/bin/env python3
"""
scaffold_brand.py — Brand context folder scaffolding tool.

Creates brand/[client]/ directory from brand/_template/, populates
placeholders, and tracks setup progress via a state JSON file.

Exit codes:
  0 — success (scaffold created, resume loaded, or check passed)
  1 — error or check failed (missing required sections)
  2 — client already fully set up (no-op, use --force to overwrite)
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path


# Placeholder token used in template files
CLIENT_PLACEHOLDER = "[CLIENT_NAME]"

# Section order for the setup interview
SECTIONS = ["identity", "voice", "pillars", "personas", "messaging", "channels"]

# Minimum required rules/entries per file for the quality check
QUALITY_CHECKS = {
    "voice-personal.md": 5,
    "voice-company.md": 5,
}

# Files that map to each section (relative to brand/[client]/)
SECTION_FILES = {
    "identity": ["voice-personal.md", "voice-company.md"],
    "voice": ["voice-personal.md", "voice-company.md"],
    "pillars": ["pillars.md"],
    "personas": ["personas.yaml"],
    "messaging": ["messaging.md"],
    "channels": [
        "channel-notes/personal-linkedin.md",
        "channel-notes/company-linkedin.md",
        "channel-notes/newsletter.md",
        "channel-notes/twitter.md",
        "channel-notes/blog.md",
    ],
}

DEFAULT_STATE = {
    "sections": {s: "pending" for s in SECTIONS},
    "active_channels": [],
    "notes": "",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_state(state_path: Path) -> dict:
    if state_path.exists():
        with open(state_path) as f:
            return json.load(f)
    return {}


def save_state(state_path: Path, state: dict) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)
    print(f"State saved → {state_path}")


def replace_placeholders(text: str, client: str) -> str:
    """Replace [CLIENT_NAME] with the actual client slug."""
    return text.replace(CLIENT_PLACEHOLDER, client)


def file_has_real_content(filepath: Path, min_non_template_lines: int = 3) -> bool:
    """
    Return True if the file exists and has at least N lines that are
    neither blank, comment-only, nor pure placeholder text.
    """
    if not filepath.exists():
        return False
    with open(filepath) as f:
        lines = f.readlines()
    real = [
        l for l in lines
        if l.strip()
        and not l.strip().startswith("#")
        and CLIENT_PLACEHOLDER not in l
        and l.strip() not in ("---", "```", "```yaml")
    ]
    return len(real) >= min_non_template_lines


# ---------------------------------------------------------------------------
# Scaffold
# ---------------------------------------------------------------------------

def scaffold(client: str, brand_dir: Path, template_dir: Path, state_path: Path, force: bool = False) -> int:
    """
    Create brand/[client]/ from brand/_template/.
    Returns 0 on success, 1 on error, 2 if already fully set up.
    """
    target_dir = brand_dir / client

    # Load existing state
    existing_state = load_state(state_path)

    if existing_state and not force:
        all_complete = all(
            v == "complete"
            for v in existing_state.get("sections", {}).values()
        )
        if all_complete:
            print(f"Brand '{client}' is already fully set up. Use --force to re-scaffold.")
            return 2

    if not template_dir.exists():
        print(f"Error: Template directory not found at {template_dir}", file=sys.stderr)
        return 1

    # Create target directory
    target_dir.mkdir(parents=True, exist_ok=True)

    # Copy template files, replacing placeholders
    copied = 0
    skipped = 0
    for src_path in template_dir.rglob("*"):
        if src_path.name in (".DS_Store", ".gitkeep"):
            continue
        if src_path.is_dir():
            continue

        rel = src_path.relative_to(template_dir)
        dest_path = target_dir / rel

        # Skip if destination exists and has real content (don't overwrite)
        if dest_path.exists() and file_has_real_content(dest_path) and not force:
            skipped += 1
            continue

        dest_path.parent.mkdir(parents=True, exist_ok=True)

        content = src_path.read_text(encoding="utf-8", errors="replace")
        content = replace_placeholders(content, client)
        dest_path.write_text(content, encoding="utf-8")
        copied += 1

    # Create examples directories (empty — populated manually)
    (target_dir / "examples" / "personal").mkdir(parents=True, exist_ok=True)
    (target_dir / "examples" / "company").mkdir(parents=True, exist_ok=True)

    print(f"Scaffolded brand '{client}' → {target_dir}")
    print(f"  Files created: {copied}  |  Skipped (already have content): {skipped}")

    # Initialise or update state file
    state = existing_state or {}
    state.setdefault("client", client)
    state.setdefault("created", str(date.today()))
    for k, v in DEFAULT_STATE.items():
        state.setdefault(k, v)
    if force:
        state["sections"] = {s: "pending" for s in SECTIONS}

    save_state(state_path, state)
    return 0


# ---------------------------------------------------------------------------
# Resume
# ---------------------------------------------------------------------------

def resume(client: str, state_path: Path) -> int:
    """Print resume instructions: which section to continue from."""
    state = load_state(state_path)
    if not state:
        print(f"No state file found at {state_path}. Run without --resume first.")
        return 1

    sections = state.get("sections", {})
    print(f"\n=== Brand Setup: {client} ===\n")
    for section in SECTIONS:
        status = sections.get(section, "pending")
        icon = {"complete": "✓", "in_progress": "→", "pending": "○"}.get(status, "?")
        print(f"  {icon}  {section:15s}  {status}")

    # Find first incomplete section
    for section in SECTIONS:
        if sections.get(section) != "complete":
            print(f"\nNext: Continue with section '{section}'")
            print(f"Files to fill: {', '.join(SECTION_FILES.get(section, []))}")
            return 0

    print("\nAll sections complete. Brand setup is done.")
    return 0


# ---------------------------------------------------------------------------
# Mark section complete
# ---------------------------------------------------------------------------

def mark_section(client: str, section: str, status: str, state_path: Path) -> int:
    if section not in SECTIONS:
        print(f"Error: Unknown section '{section}'. Valid: {', '.join(SECTIONS)}", file=sys.stderr)
        return 1

    state = load_state(state_path)
    if not state:
        print(f"No state file found at {state_path}.", file=sys.stderr)
        return 1

    state["sections"][section] = status
    save_state(state_path, state)
    print(f"Section '{section}' marked as '{status}'.")
    return 0


# ---------------------------------------------------------------------------
# Quality check
# ---------------------------------------------------------------------------

def check(client: str, brand_dir: Path, state_path: Path) -> int:
    """
    Run quality checks on brand/[client]/ files.
    Returns 0 if all pass, 1 if any fail.
    """
    target_dir = brand_dir / client
    if not target_dir.exists():
        print(f"Error: Brand directory not found: {target_dir}", file=sys.stderr)
        return 1

    print(f"\n=== Quality Check: {client} ===\n")
    failures = []

    # Required files
    required = [
        "voice-personal.md",
        "voice-company.md",
        "pillars.md",
        "personas.yaml",
        "messaging.md",
    ]
    for fname in required:
        fpath = target_dir / fname
        if not file_has_real_content(fpath):
            failures.append(f"FAIL  {fname} — missing or has only placeholder content")
        else:
            print(f"  OK    {fname}")

    # Channel-notes: at least one should be filled
    channel_dir = target_dir / "channel-notes"
    channel_files = list(channel_dir.glob("*.md")) if channel_dir.exists() else []
    filled_channels = [f for f in channel_files if file_has_real_content(f)]
    if not filled_channels:
        failures.append("FAIL  channel-notes/ — no channel files have real content")
    else:
        print(f"  OK    channel-notes/ ({len(filled_channels)} channel(s) configured)")

    # Examples: at least one personal example (warning only — populated manually)
    personal_ex = list((target_dir / "examples" / "personal").glob("*.md")) if (target_dir / "examples" / "personal").exists() else []
    if not personal_ex:
        print(f"  WARN  examples/personal/ — no example files found (add before generating)")
    else:
        print(f"  OK    examples/personal/ ({len(personal_ex)} example(s))")

    company_ex = list((target_dir / "examples" / "company").glob("*.md")) if (target_dir / "examples" / "company").exists() else []
    if not company_ex:
        print(f"  WARN  examples/company/ — no example files found (add before generating company content)")
    else:
        print(f"  OK    examples/company/ ({len(company_ex)} example(s))")

    print()
    if failures:
        for f in failures:
            print(f"  {f}")
        print(f"\n{len(failures)} issue(s) found. Fix before running generation.")
        return 1
    else:
        print("All checks passed. Brand setup is ready for generation.")
        return 0


# ---------------------------------------------------------------------------
# List clients
# ---------------------------------------------------------------------------

def list_clients(brand_dir: Path, state_dir: Path) -> int:
    """List all client brand folders with setup status."""
    if not brand_dir.exists():
        print(f"Brand directory not found: {brand_dir}")
        return 1

    clients = [
        d for d in brand_dir.iterdir()
        if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")
    ]

    if not clients:
        print("No client brand folders found.")
        return 0

    print(f"\n{'Client':<20}  {'State file':<12}  Sections complete")
    print("-" * 60)
    for client_dir in sorted(clients):
        name = client_dir.name
        state_path = state_dir / f"{name}-setup.json"
        if state_path.exists():
            state = load_state(state_path)
            sections = state.get("sections", {})
            done = sum(1 for v in sections.values() if v == "complete")
            total = len(SECTIONS)
            print(f"  {name:<18}  {'yes':<12}  {done}/{total}")
        else:
            print(f"  {name:<18}  {'no':<12}  —")

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Scaffold and manage client brand context folders.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create brand/new-client/ from template
  python scaffold_brand.py --client new-client

  # Resume an interrupted setup (see which section is next)
  python scaffold_brand.py --client new-client --resume

  # Mark a section complete
  python scaffold_brand.py --client new-client --mark-complete identity

  # Run quality check
  python scaffold_brand.py --client new-client --check

  # List all clients and setup status
  python scaffold_brand.py --list
        """,
    )

    p.add_argument("--client", help="Client slug (e.g. new-client, acme-corp)")
    p.add_argument("--brand-dir", default="brand/", help="Path to brand/ directory (default: brand/)")
    p.add_argument("--template-dir", default="brand/_template", help="Path to template directory")
    p.add_argument("--state-dir", default=".claude/skills/brand-setup/state", help="Directory for state files")

    # Actions
    p.add_argument("--resume", action="store_true", help="Show setup progress and next section")
    p.add_argument("--check", action="store_true", help="Run quality checks on brand files")
    p.add_argument("--mark-complete", metavar="SECTION", help="Mark a section as complete")
    p.add_argument("--mark-status", metavar="STATUS", default="complete",
                   help="Status to set with --mark-complete (default: complete)")
    p.add_argument("--list", action="store_true", help="List all clients and setup status")
    p.add_argument("--force", action="store_true", help="Overwrite existing content (use carefully)")

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Resolve paths
    script_dir = Path(__file__).parent
    # Walk up to find the ContentEngine root (where brand/ lives)
    # Default: relative to CWD
    brand_dir = Path(args.brand_dir).resolve()
    template_dir = Path(args.template_dir).resolve()
    state_dir = Path(args.state_dir).resolve()

    if args.list:
        return list_clients(brand_dir, state_dir)

    if not args.client:
        parser.print_help()
        print("\nError: --client is required unless using --list", file=sys.stderr)
        return 1

    client = args.client.lower().strip()
    state_path = state_dir / f"{client}-setup.json"

    if args.resume:
        return resume(client, state_path)

    if args.check:
        return check(client, brand_dir, state_path)

    if args.mark_complete:
        return mark_section(client, args.mark_complete, args.mark_status, state_path)

    # Default: scaffold
    return scaffold(client, brand_dir, template_dir, state_path, force=args.force)


if __name__ == "__main__":
    sys.exit(main())
