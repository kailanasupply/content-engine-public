# /publish

Push an approved content object to Notion and log it in the Airtable content calendar.

## Usage
```
/publish [content-file-path]
/publish outputs/blog/2026-03-11_blog_content-calendar-problem.md
```

## Instructions

You are the **Publishing Agent** for the Content Ecosystem Engine.

---

**Step 1 — Read and validate the content object**

Read the file at `$ARGUMENTS`.

Check:
- `status` must be `approved` — if it's `draft` or `review`, stop and tell the user:
  ```
  ⚠ This content is still in '[status]' status.
  Update the status to 'approved' in the frontmatter before publishing.
  ```
- `notion_id` must be null — if it already has a Notion ID, confirm:
  ```
  This piece was already published to Notion (ID: [notion_id]).
  Publish again? This will create a duplicate. (yes/no)
  ```

**Step 2 — Check config**

Read `config/settings.yaml`.

If `notion.enabled: false`:
```
⚠ Notion publishing is disabled.
To enable: set notion.enabled to true and add your database IDs in config/settings.yaml.
Save locally only? (yes to skip Notion, no to abort)
```

If `airtable.enabled: false`: skip Airtable step silently (or warn if user expects it).

**Step 3 — Publish to Notion**

Run: `python scripts/publish_notion.py "$ARGUMENTS"`

The script:
1. Reads the content object frontmatter and body
2. Determines the correct Notion database from `settings.yaml` based on content `type`
3. Creates a new page with:
   - Title = content title
   - Body = markdown content converted to Notion blocks
   - Properties = all frontmatter fields mapped to Notion properties
4. Returns the new Notion page ID and URL

On success, update the content object file:
- Set `notion_id` to the returned page ID
- Set `notion_url` to the returned URL
- Set `status` to `published`
- Set `updated` to current timestamp

**Step 4 — Log to Airtable**

Run: `python scripts/publish_airtable.py "$ARGUMENTS"`

The script:
1. Reads the updated content object
2. Creates a new row in the Airtable content calendar table
3. Maps content object fields to Airtable columns per `settings.yaml` field_mapping
4. Returns the Airtable record ID

On success, update the content object file:
- Set `airtable_record_id` to the returned record ID

**Step 5 — Report**

```
✅ Published: [content title]

  Notion: [notion_url]
  Airtable: Row added to Content Calendar
  Local file updated: [file path]

  Status: published
```

**Error handling:**

If either publish step fails, log to `config/publish_errors.log` in this format:
```
[timestamp] PUBLISH_ERROR
  File: [file path]
  Step: [notion|airtable]
  Error: [error message]
```

Then tell the user:
```
⚠ Publish partially failed. Content saved locally at [path].
  Error logged to config/publish_errors.log
  [Specific error message]
```
