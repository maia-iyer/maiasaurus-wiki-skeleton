---
name: skill:postmortem
description: Retrospective on skill usage — identify what worked, what didn't, and improvements
user-invocable: true
allowed-tools: Read, Bash, AskUserQuestion
---

# Skill: Postmortem

Retrospective on a recent skill invocation to identify improvement opportunities.

Usage: `/skill:postmortem <skill-name>`

## Phase 1: Gather Context

Ask the user:
1. What did you just use this skill for?
2. What went well?
3. What was frustrating or didn't work as expected?
4. Did it load the right context? Too much? Too little?

## Phase 2: Diagnose

Based on user feedback, categorize issues:

- **Context loading** — wrong results, missing results, too much irrelevant content
- **Workflow friction** — too many steps, wrong order, missing steps
- **Output quality** — wrong format, wrong level of detail, missing provenance
- **Scope** — skill tried to do too much or too little

For context loading issues, run a diagnostic:

```bash
python -m qmd search --collection wiki --query "<what the skill searched for>" --top-k 10
```

Compare against what the user expected.

## Phase 3: Recommend

Present 1-3 concrete improvements, prioritized by impact:

```
1. [Category] <what to change>
   Why: <diagnosis>
   How: <specific edit to SKILL.md>
```

Ask: "Want me to apply these via `/skill:improve <name>`?"

## Boundaries

- This skill diagnoses and recommends. It does not edit skills directly.
- For edits, invoke `/skill:improve` with the recommendations as context.
- Do not write files.
