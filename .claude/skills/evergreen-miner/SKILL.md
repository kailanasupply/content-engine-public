---
name: evergreen-miner
description: Scan the archive for evergreen idea candidates and surface the best ones to repurpose. Use this skill when running /monthly-evergreen-scan, when the morning scan produces no new input, when /repurpose-idea is called without a specific file, or when the generation log shows a gap in a client's content cadence. Trigger on: "monthly evergreen scan", "repurpose ideas", "what can I recycle", "find old ideas worth reusing", "nothing new in inputs", or "evergreen candidates".
---

# Evergreen Miner

Scans `archive/evergreen-candidates/` and the broader archive for ideas worth repurposing. Applies a freshness rubric to identify which candidates are strong, which need a new angle, and which have already been used.

---

## What this skill does

1. Reads `archive/evergreen-candidates/` — the pre-tagged candidates flagged during input processing
2. Cross-references against `generation-log` — skips ideas that have already been turned into published or approved content
3. Scores each candidate against the freshness rubric
4. Produces a ranked shortlist with recommended repurpose angles

---

## Running the miner

```bash
python .claude/skills/evergreen-miner/scripts/mine_evergreen.py \
  --archive archive/ \
  --log .claude/skills/generation-log/log/generations.jsonl \
  --rubric .claude/skills/evergreen-miner/freshness-rubric.md \
  --output .claude/skills/evergreen-miner/log/mined-ideas.jsonl \
  --client [client-slug]
```

**Options:**
- `--client` — filter to ideas for a specific client (optional; scans all clients if omitted)
- `--top N` — return only the top N candidates by score (default: 5)
- `--force` — re-score all candidates even if already in mined-ideas.jsonl
- `--since YYYY-MM-DD` — only consider ideas archived after this date

**Exit codes:**
- `0` — candidates found and output written
- `1` — error reading files
- `2` — no candidates found (archive empty or all already used)

---

## Freshness rubric

The rubric has 5 criteria, each scored 0–2. Max score = 10.

Load `freshness-rubric.md` before scoring. The rubric covers:

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| **Timelessness** | Tied to a news cycle or event | Mostly timeless, minor refresh needed | Core insight is permanently relevant |
| **Pillar fit** | Off-pillar or unclear | Adjacent to a core pillar | Squarely in a core pillar |
| **Narrative hook** | No clear hook | Has a hook but generic | Strong, specific hook that anchors a story |
| **Angle freshness** | Already covered this angle | Covered the topic, not this angle | Topic and angle both unused in 90 days |
| **Audience match** | Wrong audience for current ICP | Partially matches | Directly relevant to primary persona |

Score ≥ 7 → surface as a strong candidate
Score 5–6 → surface with a note that it needs work
Score < 5 → skip for this cycle

---

## Output format

The miner writes results to `log/mined-ideas.jsonl` and prints a ranked shortlist to stdout:

```
=== Evergreen Candidates (brian, 2026-03-22) ===

1. [SCORE: 9]  "18-month transformation timeline"
   File: archive/2026-03/2026-03-16-18-month-transformation-timeline.md
   Pillar: building-in-public
   Recommended angle: "The moment Brian realized the 18-month rule applied to him"
   Last used: never
   Status: strong candidate

2. [SCORE: 7]  "Fraud title vs. leading the program"
   File: archive/evergreen-candidates/2026-03-16-fraud-title-vs-leading-the-program-[EVERGREEN].md
   Pillar: fraud-leadership
   Recommended angle: Company-side perspective (original was personal)
   Last used: 2026-03-17 (personal-linkedin, different angle)
   Status: eligible (different angle available)
```

---

## Cluster themes

The `cluster-themes.md` file defines recurring theme clusters for the active client(s). When two or more evergreen candidates belong to the same cluster, the miner surfaces them together with a note that they could anchor a mini-series or campaign.

Load `cluster-themes.md` before running the miner on a full archive scan.

---

## Integration with morning scan

During `/morning-scan`, if the `inputs/` folder has no new files:

1. Run the evergreen miner with `--top 3 --client [active_client]`
2. If strong candidates are found (score ≥ 7), include them in the scan report as an "Evergreen queue" section
3. Present to user for approval before generating

The morning scan should never auto-generate from evergreen candidates — always pause for review.

---

## Mined ideas log

`log/mined-ideas.jsonl` — tracks every candidate that has been surfaced, so the miner doesn't repeat the same suggestions.

Entry format:
```json
{"date": "2026-03-22", "client": "brian", "file": "archive/evergreen-candidates/...", "score": 9, "angle": "...", "status": "surfaced", "used_in": null}
```

`status` values: `surfaced` | `approved` | `rejected` | `generated`

Update `status` to `generated` after a piece based on this idea is saved to drafts.

---

## Monthly scan integration

`/monthly-evergreen-scan` runs this skill on the full archive — not just `evergreen-candidates/` — looking for ideas that were archived before evergreen tagging was active. It uses a looser threshold (score ≥ 6) and produces a longer shortlist (top 10).

Run once a month. The scan takes longer but finds candidates that would otherwise be missed.
