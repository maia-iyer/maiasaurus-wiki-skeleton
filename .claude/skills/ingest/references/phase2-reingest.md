# Phase 2 (re-ingest): Walk prior provenance

Triggered when Phase 1 detects that `source_key` already exists in `sources.jsonl`. This is a revised version of a previously ingested source.

## Load prior provenance

```bash
source .venv/bin/activate && python -c "
import sys; sys.path.insert(0, '.')
from wiki_lib.provenance import ProvenanceLog
p = ProvenanceLog('provenance.jsonl')
for e in p.for_source('<source_key>'):
    print(f\"[{e['ts']}] {e['page']} :: {e['section']}\")
    print(f\"  claim: {e['claim']}\")
"
```

## Walk each prior claim with the user

For each entry, ask:

> "This claim was lifted on `<ts>` from `<page>` / `<section>`: `<claim text>`. Still accurate in the new version? (keep / revise / remove)"

Record the user's decision for each claim. Do not proceed until every prior entry is triaged.

## Apply decisions

For each claim:

- **keep** — no action. The old provenance entry remains; no new entry needed.
- **revise** — append a *new* provenance entry with today's `ts` and the revised claim text. Update the claim on the target page. Old entry stays in the log as history.
- **remove** — append a new provenance entry with today's `ts`, the same `source_key`, and a special marker: set `origin: "source"`, add `superseded: true`, and use the claim text `"REMOVED: <old claim>"`. Remove the claim from the target page. This makes the removal visible to anyone reading provenance later without mutating the old entry.

## Bump source registration

Update the source's `ingest_date` and note the new raw filename:

```bash
source .venv/bin/activate && python -c "
import sys; sys.path.insert(0, '.')
from wiki_lib.sources import SourceRegistry
from datetime import date
r = SourceRegistry('sources.jsonl')
r.update('<source_key>', ingest_date=str(date.today()), raw_path='raw/<new-filename>')
"
```

## Update the source page banner

Open `pages/sources/<source_key>.md`. Update the "Last ingested: YYYY-MM-DD" line in the status banner to today. Rewrite any claims that changed. Preserve the `volatile` status banner.

## Walk the initiative page

If any revised or removed claims were synthesized into an initiative page (grep for the `source_key` in provenance for initiative pages), prompt the user to walk that initiative page and adjust affected synthesis.

## Proceed to Phase 3 for any *new* claims

After the walk, any new claims in the revised source follow the normal Phase 3 flow (interactive drafting + provenance).
