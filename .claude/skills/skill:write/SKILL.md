---
name: skill:write
description: Author or edit a skill with intent gathering, consolidation check, and review gate
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# Skill: Write

Author a new skill or edit an existing one interactively.

Usage: `/skill:write <name>`

## Phase 1: Intent

Ask the user:
1. What should this skill do?
2. When does it trigger — user-invoked, or loaded by other skills?
3. What does it produce — files, reports, side effects?

## Phase 2: Consolidation Check

Scan `.claude/skills/*/SKILL.md` — read each skill's `name` and `description` from frontmatter.

For each existing skill, assess: could the stated intent be achieved by extending or generalizing it?

Present findings and ask whether to create new or extend existing.

## Phase 3: Scaffold or Load

If `.claude/skills/<name>/SKILL.md` exists: edit mode — read and proceed to Phase 4.

If not: create with frontmatter:
```yaml
---
name: <name>
description: <one-liner>
user-invocable: <true|false>
allowed-tools: <tools needed>
---
```

## Phase 4: Shape

Interactive Q&A to build the skill body:
- Walk through phases sequentially
- For each: what happens, what tools are needed, what happens on failure?
- Build incrementally, showing drafts after each phase

## Phase 5: Review Gate

Check against these criteria:
- Does each phase have a clear entry/exit condition?
- Are all tool calls explicit (not "use appropriate tool")?
- Is the skill testable via `/context:test`?
- Does it follow the epistemic stance (if it writes wiki content)?
- Does it log provenance (if it modifies pages)?

Present findings. Resolve before committing.

## Phase 6: Commit

```bash
git add .claude/skills/<name>/
git commit -m "skill: add <name>"
```
