---
name: note
description: Capture insights — write directly to wiki pages or to notes/ for freeform captures
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion
---

# Note

Capture insights, meeting notes, or thinking. Can attach directly to a wiki page or store as freeform in `notes/`.

Usage:
- `/note <content>` — auto-route based on content
- `/note --page <path> <content>` — write directly to a specific page
- `/note --freeform <content>` — always write to `notes/`

## Phase 1: Route

If `--page` is specified, skip to Phase 2 with that target.

If `--freeform` is specified, skip to Phase 3.

### Resolve ephemeral references

Before routing, scan the note content for referents that won't survive outside this session:

- Single-letter or short alphanumeric labels referring to enumerated items (e.g. "B2", "A3", "the second one", "option 2")
- Pronouns whose antecedent is in the chat history, not the note content ("this approach", "that idea" with no nearby noun)

For each one found, resolve it inline by replacing the placeholder with its meaning from the surrounding conversation. Show the user the rewritten text and ask: *"Resolved as written, or adjust?"*

If nothing ambiguous is found, proceed silently.

Otherwise, search for a relevant page:

```bash
python -m qmd search --collection wiki --query "<content summary>" --top-k 3
```

If the top result scores above 0.7 and is a topic page or initiative page, propose attaching:

> "This seems relevant to **<page title>** (`<path>`). Attach to this page, or save as freeform note?"

Options: Attach to <page> | Save to notes/ | Pick a different page

If no strong match, default to freeform.

## Phase 2: Attach to page

Read the target page. Identify the most relevant existing section based on the note content.

Ask: "Add under **<section>**, or create a new section?"

Write the note content to the chosen section using Edit. Keep the note concise — one to three bullets or a short paragraph.

Log provenance:

```json
{"page": "<path>", "section": "<section>", "origin": "note", "inline": true, "claim": "<summary of note content>", "ts": "<today>"}
```

Append the provenance entry to `provenance.jsonl`.

Update the qmd index:

```bash
python -m qmd document add --collection wiki --document-id "<path>" --markdown-file "<full-path>"
```

Commit:

```bash
git add <page-path> provenance.jsonl
git commit -m "note: <brief summary>"
```

## Phase 3: Freeform

Write to `notes/<YYYY-MM-DD>-<slug>.md`:

```markdown
# <Title derived from content>

<content>
```

Log provenance:

```json
{"page": "notes/<filename>", "section": "# <title>", "origin": "note", "note_file": "notes/<filename>", "claim": "<summary>", "ts": "<today>"}
```

Index in qmd:

```bash
python -m qmd document add --collection wiki --document-id "notes/<filename>" --markdown-file "<full-path>"
```

Commit:

```bash
git add notes/<filename> provenance.jsonl
git commit -m "note: <brief summary>"
```
