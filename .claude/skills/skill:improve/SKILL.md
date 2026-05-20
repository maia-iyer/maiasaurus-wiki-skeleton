---
name: skill:improve
description: Apply quality rubric to an existing skill and propose improvements
user-invocable: true
allowed-tools: Read, Edit, Write, AskUserQuestion, Bash
---

# Skill: Improve

Apply a quality rubric to an existing skill and propose targeted improvements.

Usage: `/skill:improve <name>`

## Phase 1: Load

Read `.claude/skills/<name>/SKILL.md`. If it has `references/`, read those too.

## Phase 2: Evaluate

Score against rubric:

### Structure
- [ ] Clear frontmatter (name, description, allowed-tools)
- [ ] Phased workflow with explicit entry/exit conditions
- [ ] Each phase has concrete tool invocations (not vague instructions)
- [ ] Failure modes documented

### Integration
- [ ] Uses qmd search for context loading (not hardcoded paths)
- [ ] Logs provenance for wiki modifications
- [ ] Follows epistemic stance (if applicable)
- [ ] Indexes new/changed pages in qmd after writes

### Testability
- [ ] Can be tested via `/context:test` (search queries are explicit)
- [ ] Expected outputs are described
- [ ] Edge cases handled (empty results, missing files)

### Conciseness
- [ ] No redundant instructions
- [ ] No placeholder language ("appropriate", "as needed", "etc.")
- [ ] Skill fits in one readable file (not excessively long)

## Phase 3: Propose

Present findings as:
- Must-fix (blocks correct operation)
- Suggestions (improves quality)

For each, show the current text and proposed replacement.

## Phase 4: Apply

Ask which improvements to apply. Edit inline. Commit:

```bash
git add .claude/skills/<name>/
git commit -m "skill:improve: <name> — <brief summary>"
```
