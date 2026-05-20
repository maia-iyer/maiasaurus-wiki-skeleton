# Phase 1: Fetch, Extract & Route (single-page mode)

## Fetch

Use **WebFetch** as the default. Pass a prompt that extracts the title, authors, publication date, and substantive claims verbatim (not a summary) while preserving section structure.

Fall back to `curl -s <url>` only if WebFetch is blocked, returns a cross-host redirect notice, or the site requires raw HTML. If the content is too large with curl, extract the main body text.

## Extract metadata

- title, authors, year, URL, suggested key, one-liner, source type (`paper`, `blog`, `standard`, `spec`, `doc`, `proposal`, `other`)

## Duplicate check

```bash
./wiki validate
```

Then check if the URL already exists:

```python
from wiki_lib.sources import SourceRegistry
registry = SourceRegistry("sources.jsonl")
existing = registry.check_url("<url>")
```

If a match is found, show the existing entry and ask: Update / Add anyway / Abort.

## Metadata table

Present metadata as a table and ask: "Confirm metadata? (or correct any field)" — wait for confirmation before proceeding to Phase 2.
