---
name: lint
description: LLM-powered content quality linting — contradictions, staleness, vagueness, scope creep
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion
---

# Lint (Tier 2 — Content Quality)

Interactive content quality pass. Proposes structural and content changes for user approval.

Usage:
- `/lint` — full wiki scan
- `/lint <page-path>` — lint a specific page
- `/lint --check <type>` — run only one check type (contradictions, staleness, vagueness, scope)

## Phase 1: Select scope

If a specific page was given, load it. Otherwise, list all pages and select candidates:

```bash
python -m qmd search --collection wiki --query "" --top-k 20
```

For `--check`, only run the specified check type.

## Phase 2: Run checks

### Contradictions

For each page in scope, search for pages with overlapping content:

```bash
python -m qmd search --collection wiki --query "<page title and key terms>" --top-k 5
```

Load the page and each related page. Check for claims that directly conflict.

### Staleness

Read `provenance.jsonl`. Find entries with `ts` older than 90 days. For each stale entry, check if the source has known updates or if the claim still holds.

### Vagueness

Read pages and flag claims that:
- Use hedge words without specifics ("various", "many", "often")
- Make claims without concrete examples or references
- Define terms circularly

### Scope creep

Count distinct subtopics (## headings) per page. If a page has more than 5 distinct subtopics, or exceeds 300 lines, flag for potential splitting.

## Phase 3: Present findings

For each finding:

```
[Type] <page-path> §<section>
  Issue: <description>
  Suggestion: <proposed fix — split, rewrite, verify, remove>
```

Ask: "Which to address? (e.g. 1,3 or 'all' or 'skip')"

## Phase 4: Apply changes

For each accepted suggestion:
- Make the edit (split page, rewrite claim, update content)
- Log provenance with `origin: "lint"` and appropriate `action`
- For splits: duplicate original provenance entries to new page
- Update qmd index for changed pages

## Phase 5: Commit

```bash
git add pages/ provenance.jsonl
git commit -m "lint: <brief summary of changes>"
```

### Structural change provenance

When splitting a page:
```json
{"page": "<new-page>", "section": "<section>", "origin": "lint", "action": "split_from", "from_page": "<original-page>", "from_section": "<original-section>", "ts": "<today>"}
```

When merging:
```json
{"page": "<target-page>", "section": "<section>", "origin": "lint", "action": "merged_from", "from_page": "<source-page>", "from_section": "<source-section>", "ts": "<today>"}
```
