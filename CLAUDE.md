# {{WIKI_NAME}}

{{WIKI_DESCRIPTION}}

Local LLM-maintained knowledge base. Skills in `.claude/skills/` load on demand.

## Behavior

- No scope creep. Flag adjacent issues; don't fix them uninvited.
- Every claim must be traceable to its origin via provenance.jsonl.
- No inline citations in wiki pages — provenance log handles traceability.
- Epistemic stance: frame claims as "X proposes..." / "according to Y..." — never as fact.

## Search

All context loading uses qmd:
```bash
python -m qmd search --collection wiki --query "<query>" --top-k <N>
```

## CLI

```bash
./wiki lint              # Tier 1 structural linting
./wiki reindex           # Rebuild qmd index
./wiki provenance <page> # Show provenance for a page
./wiki sources           # List registered sources
./wiki validate          # Registry integrity check
```

## Page topology

- `pages/*.md` — topic synthesis (200-300 lines max, 3+ subtopics/sources threshold)
- `pages/sources/*.md` — minimal source summaries (30-80 lines, 3+ key claims threshold)
- `pages/initiatives/*.md` — living initiative trackers
- `drafts/` — WIPs the user is authoring
- `notes/` — freeform captures, meeting notes
- `raw/` — archival original text (unstable URLs only, NOT indexed)
