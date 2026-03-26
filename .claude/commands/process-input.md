# /process-input

Process a raw input file (recording, notes, or brief) and extract structured insights ready for content generation.

## Usage
```
/process-input [file-path]
/process-input inputs/notes/2026-03-11-strategy-session.md
/process-input inputs/recordings/2026-03-11_brian_call_product-feedback.mp3
/process-input inputs/briefs/q2-launch.yaml
```

## Instructions

You are the **Input Processor** for the Content Ecosystem Engine.

**Step 1 — Detect input type**

Read the file at `$ARGUMENTS`. Determine if it is:
- `recording` — audio file (.mp3, .m4a, .wav, .mp4, .webm)
- `notes` — markdown or text notes file
- `brief` — YAML campaign brief

**Step 2 — Handle recordings**

If input is a recording:
1. Check if a `.meta.yaml` companion file exists with the same base name
2. Run transcription: `python scripts/transcribe.py "$ARGUMENTS"`
3. The transcription script saves a `.transcript.md` file to `inputs/processed/`
4. Continue processing the transcript file

**Step 3 — Extract structured insights**

Read the full content. Extract the following into a structured insight file:

```yaml
# Insight Extraction Output
source_file: [original file path]
source_type: [recording|notes|brief]
client: [from file metadata or active_client from config/settings.yaml]
campaign: [from file metadata if present, else null]
processed_at: [ISO timestamp]

summary: >
  2–3 sentence summary of what this input is about.

core_insights:
  - insight: "[The idea in one clear sentence]"
    why_it_matters: "[For the target audience]"
    evidence: "[Supporting quote, data point, or context from the input]"
    suggested_pillar: "[Best matching content pillar]"
    suggested_persona: "[Best matching persona ID]"
    content_potential:
      blog: true/false
      social: true/false
      newsletter: true/false
      email: true/false

quotable_moments:
  - quote: "[Exact or near-exact quote worth using in content]"
    speaker: "[Who said it]"
    context: "[Brief context]"

key_themes: []      # List of 3–8 theme tags
off_limits: []      # Topics from this input NOT to use for content
```

**Step 4 — Validate**

- If fewer than 2 core insights are found, flag this and ask the user if they want to add context before proceeding
- If client doesn't match a brand folder, stop and prompt the user to run `/new-brand [client-name]` first

**Step 5 — Save output**

Save the structured insight file to:
`inputs/processed/[YYYY-MM-DD]_[source-filename]-insights.yaml`

**Step 6 — Report to user**

Print a concise summary:
```
✓ Processed: [filename]
  Client: [name]
  Insights found: [n]
  Quotable moments: [n]
  Suggested content: [blog, social, newsletter, etc.]

  Saved to: inputs/processed/[filename]-insights.yaml

  Ready to generate. Run:
  /generate-campaign inputs/processed/[filename]-insights.yaml
```
