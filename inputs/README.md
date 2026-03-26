# inputs/

Drop raw inputs here. The morning scan picks them up.

| Folder | What goes here |
|--------|---------------|
| `recordings/` | Audio files (.mp3, .m4a, .wav) — transcribed by `scripts/transcribe.py` |
| `notes/` | Text notes (.md, .txt) — client calls, observations, raw thinking |
| `briefs/` | Campaign briefs (.yaml) — use `briefs/_template-campaign-brief.yaml` as starting point |
| `inspiration/` | Liked posts, screenshots, quick ideas — processed by `/process-inspiration` |
| `processed/` | Structured outputs from `/process-input` and inspiration queues |

## How inputs flow

```
inputs/ → /morning-scan detects → /process-input extracts insights
→ orchestrator builds manifest → you approve → generation runs
→ processed inputs archived to archive/YYYY-MM/
```
