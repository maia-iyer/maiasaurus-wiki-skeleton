---
name: draft:edit
description: Wiki-aware revision pass on a draft, with optional freeform notes
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion
---

# Draft: Edit

Run a wiki-aware revision pass on a draft in `drafts/`. Compares the draft against wiki context and surfaces gaps, contradictions, and new references.

Usage: `/draft:edit <path> [notes]`

Notes can be inline text or a file reference with `@path/to/file.md`.

Examples:
- `/draft:edit drafts/state-management-epic.md`
- `/draft:edit drafts/state-management-epic.md @notes/2026-05-06-meeting.md`
- `/draft:edit drafts/state-management-epic.md These primitives also need multi-backend storage`

## Phase 1: Load Context

Read the draft file. Extract its title and subject matter from the content.

Search for relevant wiki context:

```bash
python -m qmd search --collection wiki --query "<draft title and key themes>" --top-k 8
```

Read top results (up to 4000 tokens of wiki context).

**If notes were provided:** Parse into discrete claims.
- Inline text: split on sentence boundaries.
- `@path`: read the file, then split.

Announce what was loaded:

> **Draft:** `<path>`
> **Loaded:**
> - <list of wiki pages/sections>
> **Notes provided:** yes / no

## Phase 2: Analyze & Suggest

Produce a numbered suggestion list, ordered by position in the draft (top to bottom).

### Wiki-driven suggestions

For each loaded page:
- Does the draft reference or address this content?
- Does the draft contradict any claims in the wiki?
- Are there wiki concepts relevant to the draft's thesis but missing?

Types:
- **new reference** — wiki content relevant but unmentioned
- **update claim** — draft says X, wiki says Y
- **fill gap** — draft's thesis implies this but it's missing
- **flag contradiction** — draft contradicts wiki content

### Note-driven suggestions (when notes provided)

For each discrete point:
- Where does it belong in the draft?
- Does it add new content or refine existing?

Types:
- **incorporate note** — new content from notes
- **revise from note** — notes refine existing draft claim

### Format

```
N. [Type]
   Where: <section heading in draft>
   Why: <cite wiki page and section, or quote note>
   Proposed text: <exact wording>
```

If no suggestions: "No gaps, contradictions, or note-driven changes found."

## Phase 3: Interactive Review

Ask: "Which suggestions to apply? (e.g. 1,3,4 or 'all' or 'none')"

For each accepted suggestion: "Apply as-is, or rephrase?"

Apply edits as confirmed — do not batch.

## Phase 4: Provenance & Commit

For any wiki claims that flow into the draft, log provenance:

```json
{"page": "<draft-path>", "section": "<section>", "origin": "draft", "draft_file": "<draft-path>", "claim": "<claim>", "ts": "<today>"}
```

Update qmd index for the draft:

```bash
python -m qmd document add --collection wiki --document-id "<draft-path>" --markdown-file "<full-path>"
```

Commit:

```bash
git add <draft-path> provenance.jsonl
git commit -m "draft:edit: <brief summary>"
```
