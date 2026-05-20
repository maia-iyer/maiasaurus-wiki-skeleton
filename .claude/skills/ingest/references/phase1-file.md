# Phase 1: Read, Extract & Route (file mode)

Use when the user invokes `/ingest file <path> [focus notes]` against a local file already on disk (coworker epic, AI-generated report, personal notes).

## Stage the file

If the file is outside the wiki tree, copy it in first. Choose the destination by material type:

- **Coworker epic / AI-generated report** → `raw/<filename-stem>-YYYY-MM-DD.<ext>` using today's date. Keep prior dated copies; do not overwrite.
- **Personal notes** → `notes/<initiative-key>/<topic>.md` (if topic-grouped) or `notes/<topic>.md`.

Confirm the destination with the user before copying.

## Read

Use **Read** on the staged file. For PDFs, Read supports up to 20 pages per request; pass `pages:` for larger documents. For Word/other binary formats, ask the user to convert to `.md`, `.txt`, or `.pdf` first.

## Extract metadata

- title (from first heading or filename)
- authors (from frontmatter, document metadata, or ask the user)
- date (document's own date, if stated; otherwise ingest date)
- suggested `source_key` — **must be stable across revisions**. Derive from filename stem with any trailing date stripped. Example: `raw/acme-epic-2026-05-12.md` → `source_key: acme-epic`.
- one-liner
- source_type (`epic`, `report`, `note`, `doc`, `proposal`, `other`)

## Duplicate check

Check whether the `source_key` already exists:

```bash
source .venv/bin/activate && python -c "
import sys; sys.path.insert(0, '.')
from wiki_lib.sources import SourceRegistry
r = SourceRegistry('sources.jsonl')
existing = r.get('<source_key>')
print(existing)
"
```

If an entry exists, this is a **re-ingest**. Switch to `references/phase2-reingest.md` before drafting new claims.

## Volatile flag

Coworker epics and AI-generated reports are active working documents. Register them with `volatile: true`. Personal notes are not registered in sources.jsonl at all (see Phase 3 below and the three-origin provenance model in SKILL.md).

## Metadata table

Present metadata as a table and ask: "Confirm metadata? (or correct any field)" — wait for confirmation before proceeding to Phase 2.
