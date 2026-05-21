# Install

## 1. Clone

```bash
git clone <this repo> my-wiki
cd my-wiki
```

## 2. Install dependencies

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

## 3. Run setup

```bash
chmod +x wiki
./wiki init
```

`./wiki init` is interactive. It asks for your wiki name and a one-line description, writes them into `CLAUDE.md` (the project context Claude Code reads), offers to remove the example content, then runs lint + validate + reindex. The first reindex takes ~30 seconds while the embedding model downloads.

For scripted setups, pass everything as flags:

```bash
./wiki init --name my-wiki --description "My team knowledge base." --remove-example
```

If you re-run `./wiki init` after personalizing, it will refuse and tell you to use `--force`.

## 4. Use the skills

Open the directory in Claude Code. The skills in `.claude/skills/` are auto-discovered and invoked with a leading slash:

```
/ingest https://example.com/some-blog-post
/note "Idea I want to capture"
/spar context-engineering
/lint
```

See `README.md` for the full skill list.

## Troubleshooting

- **`./wiki: command not found`** — run `chmod +x wiki`.
- **`ModuleNotFoundError: qmd`** — activate the venv (`source .venv/bin/activate`) or install into the active Python: `uv pip install --python .venv/bin/python qmd` (or `pip install qmd`).
- **`./wiki init` says "already personalized"** — that's the safety net; use `./wiki init --force` to overwrite, or edit `CLAUDE.md` by hand.
- **Lint fails on a new page** — topic pages need a `sources:` list in frontmatter; source pages need `source_key`. See the example pages for the exact shape.
- **`source 'X' never cited in provenance`** — every entry in `sources.jsonl` must have at least one matching `source_key` row in `provenance.jsonl`.
