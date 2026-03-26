#!/usr/bin/env python3
"""
publish_notion.py — Push a content object to Notion
Usage: python scripts/publish_notion.py <content-object-path>

Reads the content object, creates a Notion page in the correct database,
updates the content object file with the Notion page ID and URL.
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime

def load_env():
    env_path = Path("config/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ.setdefault(key.strip(), value.strip())

def load_settings():
    import yaml
    with open("config/settings.yaml") as f:
        return yaml.safe_load(f)

def parse_content_object(file_path: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from a content object file"""
    import yaml
    content = file_path.read_text()

    # Extract YAML frontmatter between --- markers
    pattern = r"^---\n(.*?)\n---\n(.*)"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"No valid frontmatter found in {file_path}")

    frontmatter = yaml.safe_load(match.group(1))
    body = match.group(2).strip()

    return frontmatter, body

def markdown_to_notion_blocks(markdown: str) -> list:
    """Convert markdown to Notion block format"""
    blocks = []
    lines = markdown.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Heading 1
        if line.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })

        # Heading 2
        elif line.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                }
            })

        # Heading 3
        elif line.startswith("### "):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                }
            })

        # Bullet list
        elif line.startswith("- ") or line.startswith("* "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })

        # Numbered list
        elif re.match(r"^\d+\. ", line):
            text = re.sub(r"^\d+\. ", "", line)
            blocks.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": text}}]
                }
            })

        # Blockquote
        elif line.startswith("> "):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                }
            })

        # Horizontal rule
        elif line in ("---", "***", "___"):
            blocks.append({"object": "block", "type": "divider", "divider": {}})

        # Empty line = paragraph break
        elif line.strip() == "":
            pass  # Skip — Notion handles spacing between blocks

        # Regular paragraph
        else:
            # Check if the next few lines continue this paragraph
            para_lines = [line]
            while i + 1 < len(lines) and lines[i + 1].strip() != "" and not lines[i + 1].startswith("#"):
                i += 1
                para_lines.append(lines[i])

            paragraph_text = " ".join(para_lines)
            if paragraph_text.strip():
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": paragraph_text}}]
                    }
                })

        i += 1

    # Notion API max 100 blocks per request
    return blocks[:100]

def get_database_id(content_type: str, settings: dict) -> str:
    """Get the Notion database ID for a content type"""
    db_id = settings.get("notion", {}).get("databases", {}).get(content_type, "")
    if not db_id:
        raise ValueError(
            f"No Notion database ID configured for type '{content_type}'.\n"
            f"Add it to config/settings.yaml under notion.databases.{content_type}"
        )
    return db_id

def create_notion_page(
    database_id: str,
    frontmatter: dict,
    body: str,
    api_key: str
) -> dict:
    """Create a Notion page and return the response"""
    from notion_client import Client
    notion = Client(auth=api_key)

    # Build properties
    properties = {
        "Name": {
            "title": [{"text": {"content": frontmatter.get("title", "Untitled")}}]
        },
        "Status": {
            "select": {"name": frontmatter.get("status", "draft").capitalize()}
        },
        "Type": {
            "select": {"name": frontmatter.get("type", "")}
        },
        "Client": {
            "rich_text": [{"text": {"content": frontmatter.get("client", "")}}]
        },
        "Pillar": {
            "rich_text": [{"text": {"content": frontmatter.get("pillar", "")}}]
        },
        "Persona": {
            "rich_text": [{"text": {"content": frontmatter.get("persona", "")}}]
        },
        "Content ID": {
            "rich_text": [{"text": {"content": frontmatter.get("id", "")}}]
        },
    }

    # Optional properties
    if frontmatter.get("campaign"):
        properties["Campaign"] = {
            "rich_text": [{"text": {"content": frontmatter["campaign"]}}]
        }

    if frontmatter.get("publish_date"):
        properties["Publish Date"] = {
            "date": {"start": str(frontmatter["publish_date"])}
        }

    if frontmatter.get("word_count"):
        properties["Word Count"] = {
            "number": frontmatter["word_count"]
        }

    # Build blocks from body
    blocks = markdown_to_notion_blocks(body)

    # Create the page
    response = notion.pages.create(
        parent={"database_id": database_id},
        properties=properties,
        children=blocks
    )

    return response

def update_content_object(file_path: Path, notion_id: str, notion_url: str):
    """Update the content object file with Notion ID and URL"""
    content = file_path.read_text()

    # Update notion_id
    content = re.sub(
        r"^notion_id:.*$",
        f"notion_id: \"{notion_id}\"",
        content,
        flags=re.MULTILINE
    )

    # Update notion_url
    content = re.sub(
        r"^notion_url:.*$",
        f"notion_url: \"{notion_url}\"",
        content,
        flags=re.MULTILINE
    )

    # Update status to published
    content = re.sub(
        r"^status: .*$",
        "status: published",
        content,
        flags=re.MULTILINE
    )

    # Update updated timestamp
    content = re.sub(
        r"^updated:.*$",
        f"updated: \"{datetime.now().isoformat()}\"",
        content,
        flags=re.MULTILINE
    )

    file_path.write_text(content)

def log_error(file_path: Path, error: str):
    """Log publish errors"""
    log_path = Path("config/publish_errors.log")
    with open(log_path, "a") as f:
        f.write(f"\n[{datetime.now().isoformat()}] PUBLISH_ERROR\n")
        f.write(f"  File: {file_path}\n")
        f.write(f"  Step: notion\n")
        f.write(f"  Error: {error}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/publish_notion.py <content-object-path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    load_env()
    settings = load_settings()

    # Check Notion is enabled
    if not settings.get("notion", {}).get("enabled", False):
        print("ERROR: Notion publishing is disabled in config/settings.yaml")
        print("Set notion.enabled to true and add your database IDs to proceed.")
        sys.exit(1)

    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        print("ERROR: NOTION_API_KEY not found in config/.env")
        sys.exit(1)

    print(f"\n📤 Publishing to Notion: {file_path.name}")

    try:
        # Parse content object
        frontmatter, body = parse_content_object(file_path)

        # Get database ID
        content_type = frontmatter.get("type", "")
        database_id = get_database_id(content_type, settings)

        print(f"   Type: {content_type}")
        print(f"   Database: {database_id[:8]}...")

        # Create Notion page
        response = create_notion_page(database_id, frontmatter, body, api_key)

        notion_id = response["id"]
        notion_url = response["url"]

        # Update content object file
        update_content_object(file_path, notion_id, notion_url)

        print(f"\n✓ Published to Notion")
        print(f"   Page ID: {notion_id}")
        print(f"   URL: {notion_url}")

        # Output for the calling agent to parse
        result = {"notion_id": notion_id, "notion_url": notion_url}
        print(f"\nRESULT_JSON: {json.dumps(result)}")

    except Exception as e:
        error_msg = str(e)
        print(f"\nERROR: {error_msg}")
        log_error(file_path, error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
