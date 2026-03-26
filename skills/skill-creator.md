---
name: skill-creator
description: Meta skill for building, improving, and evaluating other skills in this engine. Use when creating a new skill, improving an existing skill, running evals against a skill, benchmarking performance, or optimizing a skill's trigger description. Trigger: "create a new skill", "improve this skill", "run evals on [skill]", "the [skill] keeps failing", "add a skill for [task]", "benchmark this skill".
triggers:
  - create a new skill
  - improve this skill
  - run evals on
  - add a skill for
  - benchmark this skill
  - the skill keeps failing
  - update skill description
loop: Plan → Build → Eval → Compound
---

# Skill Creator

The meta layer. This skill creates and improves other skills. Every time a skill fails, this is how it gets fixed. Every time a new workflow needs to be codified, this is how it becomes a skill.

---

## LOOP: Plan → Build → Eval → Compound

---

## Phase 1: PLAN

Determine what kind of skill work this is:

| Task | What it means |
|------|--------------|
| New skill | A workflow that doesn't exist as a skill yet |
| Improve existing | A skill that exists but keeps producing wrong outputs |
| Fix trigger | A skill that exists but isn't being invoked at the right times |
| Add eval | A skill with no test coverage |
| Benchmark | Measure a skill's performance with and without it active |

Load context:
1. `knowledge/INDEX.md` — what skills already exist
2. `knowledge/ERRORS.md` — any open errors related to this skill
3. `QUALITY_GATE.md` — the scoring standard that all content skills must produce against
4. If improving an existing skill: read the current SKILL.md in full

---

## Phase 2: BUILD

### Creating a new skill

**Skill anatomy:**

Every skill in `skills/` follows this structure:

```markdown
---
name: [skill-name]
description: [One-paragraph description for skill discovery. Include: what it does, when to use it, and 5+ trigger phrases.]
triggers:
  - [trigger phrase 1]
  - [trigger phrase 2]
  - ...
loop: [Plan → Work → Assess → Compound | or the specific phases used]
---

# [Skill Name]

[1-2 sentence summary of what this skill does and why it exists.]

---

## LOOP: [phases]

## Phase 1: PLAN
[What context to load. In what order. What to check in INDEX.md and ERRORS.md first.]

## Phase 2: WORK
[The actual work. Step-by-step. No vagueness — specific tools, file paths, commands.]

## Phase 3: ASSESS
[Quality check. Synthetic personas where applicable. What standard must be met before output is produced.]

## Phase 4: COMPOUND
[What to update after: ERRORS.md, learning files, generation-log, cadence-log.]

## Output format
[What the user sees. Structured output. No open-ended prose.]
```

**Key rules for skill writing:**
- Every skill reads `knowledge/INDEX.md` first in Phase 1
- Every skill checks `knowledge/ERRORS.md` for open issues before proceeding
- Every content-generating skill includes the Assess phase (synthetic personas + quality gate)
- Every skill ends with a Compound step (updates ERRORS.md at minimum)
- Trigger phrases should be conversational ("what should I make today") AND command-style ("/morning-scan")
- The `description` frontmatter is what the engine reads to decide which skill to invoke — write it for discovery, not documentation

### Improving an existing skill

1. Read the current skill SKILL.md
2. Read the open errors in `knowledge/ERRORS.md` related to this skill
3. Identify the failure mode:
   - **Wrong outputs:** Phase 2 (WORK) steps are incomplete or ambiguous
   - **Skipping checks:** Phase 1 (PLAN) doesn't load enough context
   - **No learning:** Phase 4 (COMPOUND) is missing or incomplete
   - **Triggering too often/rarely:** `description` or `triggers` need tuning
   - **Voice drift in output:** Assess phase is not catching it

4. Make the minimal change that fixes the failure. Don't rewrite the whole skill.

### Updating triggers / description

When a skill keeps getting invoked for the wrong task, or isn't being invoked when it should be:

1. Log 3–5 examples of when it was invoked incorrectly (or should have been invoked but wasn't)
2. Identify the pattern: what phrase or intent was the mismatch?
3. Update the `description` paragraph to include or exclude that pattern
4. Update the `triggers` list

**Good trigger description pattern:**
"Trigger with: [command], [natural language phrase], [the thing the user says when they have this need], or [the context in which this skill is automatically needed]."

---

## Phase 3: EVAL

Every skill should have a 3-scenario eval. Structure:

```yaml
# .claude/skills/[skill-name]/evals/evals.json
{
  "skill": "[skill-name]",
  "scenarios": [
    {
      "id": "eval-01",
      "description": "[What this eval tests]",
      "input": "[What file or prompt to use as input]",
      "expected_behavior": "[What the skill should do — not exact output, but behavior]",
      "pass_criteria": "[How to determine if it passed]",
      "known_failure_mode": "[What typically goes wrong here]"
    }
  ]
}
```

**Minimum 3 evals:**
1. **Happy path** — ideal input, expected output
2. **Edge case** — ambiguous input or blocked channel
3. **Failure recovery** — input that should trigger ERRORS.md logging

### Running an eval

1. Feed the eval input to the skill
2. Capture the output
3. Check against `pass_criteria`
4. Score: pass | partial | fail
5. If fail → note in ERRORS.md: "[skill-name] eval-0X failed: [reason]"

### Benchmarking (with/without skill)

For content-generating skills, compare output quality with skill active vs. inactive:

```
BENCHMARK: [skill-name]
Sample size: [n] drafts
WITH skill: avg quality score [n], persona A/B/C avg [n]/9
WITHOUT skill: avg quality score [n], persona A/B/C avg [n]/9
Delta: [+n quality points | -n quality points]
Conclusion: [skill improves|hurts|neutral] output quality
```

---

## Phase 4: COMPOUND

After building or improving a skill:

1. Update `knowledge/INDEX.md`:
   - Add/update the skill entry in the Skills section
   - Update the "last modified" timestamp

2. Update `knowledge/ERRORS.md`:
   - Mark any related errors as resolved
   - Add a note: "Skill [name] updated — [what changed]"

3. If this is a new skill:
   - Add it to the skills/ folder
   - Reference it in relevant slash commands (`.claude/commands/`) if applicable
   - Add an entry to CLAUDE.md Setup Checklist if it requires setup

4. Propagate to `ContentEngine-Template/`:
   - Copy the skill SKILL.md to `ContentEngine-Template/.claude/skills/[name]/SKILL.md` (or `skills/`)
   - If it includes Python scripts, copy those too
   - Update `ContentEngine-Template/CLAUDE.md` if the setup checklist changed

---

## Skill naming conventions

| Location | Purpose |
|----------|---------|
| `skills/` (root) | High-level orchestration skills. Claude reads these as behavior instructions. Named as workflows: `morning-content-scan.md` |
| `.claude/skills/[name]/` | Technical implementations with Python scripts, data files, evals. Named as tools: `anti-ai-scanner`, `generation-log` |

**When to use root `skills/`:** The workflow is conversational, plan-based, or orchestrates multiple tools.
**When to use `.claude/skills/`:** The skill has Python scripts, data stores, or eval suites that need to persist.

Many workflows have both: a root `skills/morning-content-scan.md` (orchestration instructions) + `.claude/skills/generation-log/` (the underlying data tool it calls).

---

## Output format

```
═══ SKILL BUILD/UPDATE ════════════════════════════════
Skill: [name] | Action: [new|improve|fix-trigger|eval]
Status: [complete|in-progress]

Changes made:
  - [specific change 1]
  - [specific change 2]

Evals: [n passing | n failing]
Benchmark: [if applicable]

Updated: knowledge/INDEX.md | knowledge/ERRORS.md
Template sync: [done|needed]

Recommended next: [/morning-scan | test the skill | benchmark]
════════════════════════════════════════════════════════
```
