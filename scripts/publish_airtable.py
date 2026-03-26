#!/usr/bin/env python3
"""
publish_airtable.py — Log a content object to the Airtable content calendar
Usage: python scripts/publish_airtable.py <content-object-path>

Reads the content object, adds a row to the Airtable content calendar,
updates the content object with the Airtable record ID.
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

def parse_content_object(file_path: Path) -> dict:
    """Parse YAML frontmatter from a content object file"""
    import yaml
    content = file_path.read_text()
    pattern = r"^---\n(.*?)\n---"
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        raise ValueError(f"No valid frontmatter found in {file_path}")
    return yaml.safe_load(match.group(1))

def build_airtable_record(frontmatter: dict, field_mapping: dict) -> dict:
    """Map content object fields to Airtable column names"""
    record = {}

    for content_field, airtable_column in field_mapping.items():
        value = frontmatter.get(content_field)

        if value is None or value == "" or value == "null":
            continue

        # Handle date fields
        if content_field in ("created", "updated", "approved_at") and value:
            if isinstance(value, str):
                # Airtable accepts ISO datetime strings
                record[airtable_column] = value
            else:
                record[airtable_column] = str(value)

        elif content_field == "publish_date" and value:
            record[airtable_column] = str(value)

        elif content_field == "word_count" and value:
            record[airtable_column] = int(value)

        else:
            record[airtable_column] = str(value) if value else ""

    return record

def create_airtable_record(
    base_id: str,
    table_name: str,
    record_fields: dict,
    api_key: str
) -> dict:
    """Create a record in Airtable"""
    import urllib.request

    url = f"https://api.airtable.com/v0/{base_id}/{urllib.parse.quote(table_name)}"
    payload = json.dumps({"fields": record_fields}).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    import urllib.parse
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise Exception(f"Airtable API error {e.code}: {error_body}")

def update_content_object(file_path: Path, record_id: str):
    """Update the content object file with Airtable record ID"""
    content = file_path.read_text()

    content = re.sub(
        r"^airtable_record_id:.*$",
        f"airtable_record_id: \"{record_id}\"",
        content,
        flags=re.MULTILINE
    )

    content = re.sub(
        r"^updated:.*$",
        f"updated: \"{datetime.now().isoformat()}\"",
        content,
        flags=re.MULTILINE
    )

    file_path.write_text(content)

def log_error(file_path: Path, error: str):
    log_path = Path("config/publish_errors.log")
    with open(log_path, "a") as f:
        f.write(f"\n[{datetime.now().isoformat()}] PUBLISH_ERROR\n")
        f.write(f"  File: {file_path}\n")
        f.write(f"  Step: airtable\n")
        f.write(f"  Error: {error}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/publish_airtable.py <content-object-path>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    load_env()
    settings = load_settings()

    airtable_settings = settings.get("airtable", {})

    if not airtable_settings.get("enabled", False):
        print("Airtable publishing is disabled. Skipping.")
        sys.exit(0)

    api_key = os.environ.get("AIRTABLE_API_KEY")
    if not api_key:
        print("ERROR: AIRTABLE_API_KEY not found in config/.env")
        sys.exit(1)

    base_id = airtable_settings.get("base_id", "")
    if not base_id:
        print("ERROR: airtable.base_id not set in config/settings.yaml")
        sys.exit(1)

    table_name = airtable_settings.get("table_name", "Content Calendar")
    field_mapping = airtable_settings.get("field_mapping", {})

    print(f"\n📊 Logging to Airtable: {file_path.name}")

    try:
        # Parse content object
        frontmatter = parse_content_object(file_path)

        # Build Airtable record
        record_fields = build_airtable_record(frontmatter, field_mapping)

        print(f"   Table: {table_name}")
        print(f"   Fields: {list(record_fields.keys())}")

        # Create record
        response = create_airtable_record(base_id, table_name, record_fields, api_key)
        record_id = response.get("id", "")

        # Update content object
        update_content_object(file_path, record_id)

        print(f"\n✓ Logged to Airtable")
        print(f"   Record ID: {record_id}")

        result = {"airtable_record_id": record_id}
        print(f"\nRESULT_JSON: {json.dumps(result)}")

    except Exception as e:
        error_msg = str(e)
        print(f"\nERROR: {error_msg}")
        log_error(file_path, error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
