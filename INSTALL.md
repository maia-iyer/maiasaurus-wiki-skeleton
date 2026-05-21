# Install

## 1. Clone

```bash
git clone <this repo> my-wiki
cd my-wiki
```

## 2. Personalize CLAUDE.md

`CLAUDE.md` is the only file that gets personalized — it's loaded as project context inside Claude Code. `README.md` and this `INSTALL.md` describe the skeleton itself and stay as-is.

Two placeholders appear in `CLAUDE.md`:

- `{{WIKI_NAME}}` — short name, e.g. `my-wiki`, `team-kb`, `research-notes`
- `{{WIKI_DESCRIPTION}}` — one-line description of the wiki's purpose

Replace them. macOS / BSD `sed`:

```bash
sed -i '' \
  -e 's/{{WIKI_NAME}}/my-wiki/g' \
  -e 's/{{WIKI_DESCRIPTION}}/My team knowledge base./g' \
  CLAUDE.md
```

GNU `sed` (Linux):

```bash
sed -i \
  -e 's/{{WIKI_NAME}}/my-wiki/g' \
  -e 's/{{WIKI_DESCRIPTION}}/My team knowledge base./g' \
  CLAUDE.md
```

## 3. Install dependencies

Requires Python 3.11+.

Recommended ([uv](https://docs.astral.sh/uv/)):

```bash
uv venv .venv
uv pip install --python .venv/bin/python qmd pyyaml
source .venv/bin/activate
```

Note: `uv venv` does not include `pip` inside the venv, so install with `uv pip install --python .venv/bin/python ...` rather than `.venv/bin/python -m pip`.

Fallback (plain `venv` + `pip`):

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install qmd pyyaml
```

Activate the venv (`source .venv/bin/activate`) in any new shell before running `./wiki`.

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
- **`ModuleNotFoundError: qmd`** — activate the venv (`source .venv/bin/activate`) or install into the active Python: `uv pip install --python .venv/bin/python qmd` (or `pip install qmd`).
- **Lint fails on a new page** — topic pages need a `sources:` list in frontmatter; source pages need `source_key`. See the example pages for the exact shape.
- **`source 'X' never cited in provenance`** — every entry in `sources.jsonl` must have at least one matching `source_key` row in `provenance.jsonl`.
