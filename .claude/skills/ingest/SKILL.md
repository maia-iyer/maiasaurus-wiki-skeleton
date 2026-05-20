---
name: ingest
description: Ingest a source into the wiki with interactive review — fetches, summarizes, routes to pages, logs provenance
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion, WebFetch
---

# Ingest

Usage:
- `/ingest <url> [focus notes]` — single-page source
- `/ingest repo <path-or-github-url> [focus notes]` — git repository
- `/ingest site <seed-url> [focus notes]` — documentation website (bounded crawl)
- `/ingest file <path> [focus notes]` — local file (coworker epic, AI report, personal notes)

## Epistemic stance

Load `references/epistemic-stance.md`.

## Phase 1: Fetch & Route

Detect mode from the first argument after `/ingest`:
- `repo` → load `references/phase1-repo.md`
- `site` → load `references/phase1-site.md`
- `file` → load `references/phase1-file.md`
- anything else (a URL) → load `references/phase1-single.md`

Phase 1 ends with confirmed metadata. Do not proceed until the user confirms.

## Scope

`/ingest` writes only to:
- `pages/` (topic pages)
- `pages/sources/` (source pages)
- `sources.jsonl`, `provenance.jsonl`

It must **not** write to `pages/initiatives/` or `notes/`. Initiative pages are read as context (they may show up in qmd search results) but are never modified by this skill. Promoting captured material into an initiative page is the job of `/lift`.

If the source seems to belong on an initiative page, surface that observation to the user and stop — do not auto-route into `pages/initiatives/`.

## Phase 2: Search for Related Content

### Re-ingest detection

If Phase 1 found an existing `source_key` in `sources.jsonl`, this is a **re-ingest** of a revised version. Load `references/phase2-reingest.md` and complete the prior-provenance walk *before* proceeding with the rest of Phase 2.

Search the wiki for existing related pages:

```bash
# qmd search treats `-<word>` as a field operator (e.g. "multi-agent" fails
# with {"error": "no such column: agent"}). Strip hyphens before querying.
query=$(echo "<title> <one-liner>" | tr '-' ' ')
source .venv/bin/activate && python -m qmd search --collection wiki --query "$query" --top-k 5
```

Read top results to understand what already exists.

### Routing decisions

1. **Source page?** 3+ key claims or primary reference → `pages/sources/<key>.md`. Otherwise claims flow into topic pages.

2. **Topic page updates?** Existing page covers the topic → propose additions. New topic page only if 3+ existing sources/subtopics already cover the area; list them explicitly and ask "create new page `<key>` or attach to existing?". Never default to creating.

3. **Initiative-relevant?** If yes, say so but do not write to `pages/initiatives/` — surface that `/lift` can promote claims later.

### Presentation

Numbered list: (1) source registry entry, (2) source page if warranted, (3) topic page updates or new topic pages.

## Phase 3: Interactive Review

### Phase 3a: High-level triage

Ask: "Which suggestions to keep? (e.g. 1,2,4)"

For each accepted item, state its intent. Ask: "Does this look right? (yes / adjust)"

### Phase 3b: Inline drafting

Default to **minimal additions**. Synthesis prose, framing paragraphs, and connective tissue are opt-in only — ask before writing them.

**Topic page additions:**
- One bullet per claim. New bullet over new subsection; new subsection over new section.
- No synthesis paragraph unless the user explicitly asks for one.

**Source pages:**
- No cross-links to other wiki pages. Source pages are minimal summaries of the source itself.
- No "Relation to X" or "See also" sections by default.
- If the user wants synthesis or cross-links, they will say so.

For source pages, use this template:
```markdown
---
source_key: <key>
url: <url>
source_type: <type>
ingested: <YYYY-MM-DD>
volatile: <true if active working doc, else omit>
---

# <Title>

<one-liner>

<!-- Include this banner only when volatile: true -->
> **Status:** Active working document — claims here may be revised or superseded. Last ingested: <YYYY-MM-DD>.

## Key Claims
- Claim 1
- Claim 2
- ...

## Relevance
<brief note on why this matters>
```

When registering with `volatile: true`:

```python
r.add(key='<key>', title='<title>', url='<url>', source_type='<type>',
      one_liner='<one-liner>', volatile=True)
```

Present drafts one at a time. Once confirmed, write immediately.

### Phase 3c: Provenance

For each claim written to a page, append a provenance entry. Pick `origin` based on where the claim came from:

- **`source`** — claim from a registered source (coworker epic, AI report, published doc). Includes `source_key`.
  ```json
  {"page": "<path>", "section": "<section>", "origin": "source", "source_key": "<key>", "claim": "<claim text>", "ts": "<today>"}
  ```

- **`note`** — claim from the user's own notes (files in `notes/`). Not registered in `sources.jsonl`. Includes `note_file` (path to the note).
  ```json
  {"page": "<path>", "section": "<section>", "origin": "note", "note_file": "notes/<path>.md", "claim": "<claim text>", "ts": "<today>"}
  ```

- **`synthesis`** — the user's own framing on a topic page, not traceable to a specific input.
  ```json
  {"page": "<path>", "section": "<section>", "origin": "synthesis", "claim": "<claim text>", "ts": "<today>"}
  ```

Append each entry to `provenance.jsonl`. `./wiki provenance <page>` already displays all three origins.

## Phase 4: Register & Index

Register in sources.jsonl:

```bash
source .venv/bin/activate && python -c "
import sys; sys.path.insert(0, '.')
from wiki_lib.sources import SourceRegistry
r = SourceRegistry('sources.jsonl')
r.add(key='<key>', title='<title>', url='<url>', source_type='<type>', one_liner='<one-liner>')
"
```

Index new/updated pages in qmd:

```bash
source .venv/bin/activate && python -m qmd document add --collection wiki --document-id "<path>" --markdown-file "<full-path>"
```

## Phase 5: Commit

```bash
git add sources.jsonl provenance.jsonl pages/ notes/
git commit -m "ingest: <key>"
```

Confirm the commit hash to the user.
