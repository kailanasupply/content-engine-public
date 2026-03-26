# Performance Tracking

This folder contains data about how your content performs.

## Files

### `tracker.yaml`
Log of all published content and performance signals.

Format:
```yaml
- date: 2026-03-16
  channel: personal-linkedin
  title: "Why automation projects fail"
  likes: 47
  comments: 12
  shares: 3
  dms: 2
  leads: 0
  notes: "Strong engagement but no direct leads"
```

### `cadence-log.yaml`
When each content format was last generated. Used by `/morning-scan` to decide what to generate today.

### `insights.md`
Synthesized patterns from tracker.yaml. Updated by `/synthesize-learnings` every 2 weeks.

Describes: what's performing, what isn't, trends over time, and cadence recommendations.

## Workflow

1. Publish content
2. Check performance (1–2 weeks later)
3. Run `/log-performance` to add data
4. After 5+ entries, run `/synthesize-learnings`
5. Generator reads insights.md and adjusts approach

## Thresholds

See `SUCCESS_METRICS.md` for baseline thresholds per channel.
Customize after your first 30–60 days of data.
