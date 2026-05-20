# {{WIKI_NAME}} — LLM-Maintained Wiki Skeleton

A starter template for a local, LLM-maintained knowledge base with semantic search, provenance tracking, and a set of Claude Code skills for ingesting, synthesizing, and refining content.

This is a **skeleton** — fork or clone it, fill in the `{{WIKI_NAME}}` and `{{WIKI_DESCRIPTION}}` placeholders, and start ingesting sources.

## What you get

- **CLI** (`./wiki`) — lint, reindex, provenance, sources, validate
- **Skills** in `.claude/skills/` (load on demand inside Claude Code):
  - `/ingest` — pull a URL into the wiki as a source page + provenance entries
  - `/lift` — promote claims from sources/notes into topic or initiative pages
  - `/note` — capture insights into wiki pages or freeform notes
  - `/draft:edit` — wiki-aware revision pass on a draft
  - `/spar` — Socratic dialogue grounded in wiki context
  - `/lint` — LLM-powered content quality linting (contradictions, staleness, vagueness)
  - `/context:test` — verify what context a query would load
  - `/skill:write`, `/skill:improve`, `/skill:postmortem` — author and refine skills
- **Page topology**: topic pages, source summaries, initiative trackers, drafts, notes, raw archive
- **Provenance log** (`provenance.jsonl`) — every claim traceable to its origin
- **Source registry** (`sources.jsonl`) — metadata + URLs for everything ingested
- **One worked example** — `pages/semantic-search.md` and `pages/sources/example-rag-primer.md` show the shape; delete or replace once you have real content.

## Quick start

See [INSTALL.md](INSTALL.md) for the full setup. Short version:

```bash
git clone <this repo> my-wiki && cd my-wiki

# Replace the {{WIKI_NAME}} / {{WIKI_DESCRIPTION}} placeholders
sed -i '' 's/{{WIKI_NAME}}/my-wiki/g; s/{{WIKI_DESCRIPTION}}/My team knowledge base./g' \
  README.md INSTALL.md CLAUDE.md

# Install dependencies (uv recommended; pip works too)
uv venv .venv && uv pip install --python .venv/bin/python qmd pyyaml
source .venv/bin/activate

# Verify and index
./wiki lint
./wiki reindex

# Open in Claude Code and try a skill
# /ingest https://example.com/some-blog-post
```

## Design principles

- **No raw files stored** unless the URL is unstable (ephemeral links, etc.) — summaries + pointers are sufficient.
- **Every claim is traceable** via `provenance.jsonl`, not inline citations.
- **Semantic search replaces taxonomy** — qmd handles retrieval; you don't need a tag tree.
- **Pages stay short** (200–300 lines max) so retrieved chunks remain coherent.
- **Epistemic stance preserved**: "X proposes..." rather than "X is...".

## Repo layout

```
.claude/
  settings.json              env vars for skills (offline HF, log levels)
  skills/                    10 wiki skills, load on demand
pages/
  *.md                       topic synthesis (200–300 lines)
  sources/*.md               per-source summaries (30–80 lines)
  initiatives/*.md           living project trackers
drafts/                      WIPs you're authoring
notes/                       freeform captures, meeting notes
raw/                         archival original text (unstable URLs only, NOT indexed)
wiki                         CLI entry point
wiki_lib/                    Python modules (indexer, linter, sources, provenance)
qmd.yaml                     qmd search config
sources.jsonl                source registry
provenance.jsonl             claim → origin trace log
CLAUDE.md                    project behavior + topology rules
```

## Acknowledgments

Distilled from a working personal wiki. Skills are intentionally minimal — extend them or write your own with `/skill:write`.
