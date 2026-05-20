# Install

## 1. Clone

```bash
git clone <this repo> my-wiki
cd my-wiki
```

## 2. Replace placeholders

Two placeholders appear in `README.md`, `INSTALL.md`, and `CLAUDE.md`:

- `{{WIKI_NAME}}` — short name, e.g. `my-wiki`, `team-kb`, `research-notes`
- `{{WIKI_DESCRIPTION}}` — one-line description of the wiki's purpose

Replace them in one pass. macOS / BSD `sed`:

```bash
sed -i '' \
  -e 's/{{WIKI_NAME}}/my-wiki/g' \
  -e 's/{{WIKI_DESCRIPTION}}/My team knowledge base./g' \
  README.md INSTALL.md CLAUDE.md
```

GNU `sed` (Linux):

```bash
sed -i \
  -e 's/{{WIKI_NAME}}/my-wiki/g' \
  -e 's/{{WIKI_DESCRIPTION}}/My team knowledge base./g' \
  README.md INSTALL.md CLAUDE.md
```

## 3. Install dependencies

Requires Python 3.11+.

```bash
pip install qmd pyyaml
```

(Optional) Use a virtualenv:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install qmd pyyaml
```

## 4. Make the CLI executable

```bash
chmod +x wiki
```

## 5. Verify and index

```bash
./wiki lint        # should report: OK — no structural issues found.
./wiki validate    # should report: OK — sources.jsonl is valid.
./wiki reindex     # builds the qmd search index
```

## 6. (Optional) Replace the example content

The skeleton ships with one worked example:

- `pages/semantic-search.md`
- `pages/sources/example-rag-primer.md`
- One entry in `sources.jsonl`
- Three entries in `provenance.jsonl`

Once you've ingested real content, delete the example and remove its rows from `sources.jsonl` and `provenance.jsonl`. Then re-run `./wiki lint && ./wiki reindex`.

## 7. Use the skills

Open the directory in Claude Code. The skills in `.claude/skills/` are auto-discovered and invoked with a leading slash:

```
/ingest https://example.com/some-blog-post
/note "Idea I want to capture"
/spar context-engineering
/lint
```

See `README.md` for the full skill list.

## Troubleshooting

- **`./wiki: command not found`** — run `chmod +x wiki` (step 4).
- **`ModuleNotFoundError: qmd`** — `pip install qmd` in the active Python environment.
- **Lint fails on a new page** — topic pages need a `sources:` list in frontmatter; source pages need `source_key`. See the example pages for the exact shape.
- **`source 'X' never cited in provenance`** — every entry in `sources.jsonl` must have at least one matching `source_key` row in `provenance.jsonl`.
