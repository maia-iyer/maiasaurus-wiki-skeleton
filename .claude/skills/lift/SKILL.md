---
name: lift
description: Promote claims from notes or source pages into a target topic or initiative page, with provenance
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, AskUserQuestion
---

# Lift

Move claims from `notes/<...>.md` (or a source page) into a target topic or initiative page. Each lifted claim gets a provenance entry tying it back to its origin note or source.

This is the only skill allowed to write into `pages/initiatives/`.

Usage:
- `/lift <note-path> [--into <page-path>]` — lift from a note file
- `/lift --from <source-key> [--into <page-path>]` — lift claims already captured in a source page

If `--into` is omitted, infer the target.

## Phase 1: Identify source and target

**Source side.** Read the `<note-path>` or `pages/sources/<source-key>.md`. Parse it into discrete bullet-level claims. For prose paragraphs, split on sentence boundaries.

**Target side.** If `--into` was provided, use it. Otherwise infer:

- If the note path is `notes/<initiative>/...`, propose `pages/initiatives/<initiative>.md` as the default target.
- Otherwise run `python -m qmd search --collection wiki --query "<note title and key terms>" --top-k 3` and propose the top-scoring topic or initiative page.

Confirm: *"Lift from `<source>` into `<target>`?"*

## Phase 2: Propose claims

For each parsed claim, propose:

```
N. <claim text — verbatim or lightly edited>
   Into section: <existing section in target> | new section: <suggested name>
```

Group claims by their suggested section. Prefer existing sections over new ones.

Ask: *"Which to lift? (e.g. 1,2,4 or 'all')"*

## Phase 3: Apply

For each accepted claim:

1. Edit the target page — append the claim as a bullet under the chosen section. Create the section only if explicitly accepted.
2. Append a provenance entry:

   For lifts from a note:
   ```json
   {"page": "<target-path>", "section": "<section>", "origin": "note", "note_file": "<note-path>", "claim": "<claim text>", "ts": "<today>", "action": "lifted"}
   ```

   For lifts from a registered source:
   ```json
   {"page": "<target-path>", "section": "<section>", "origin": "source", "source_key": "<key>", "claim": "<claim text>", "ts": "<today>", "action": "lifted"}
   ```

3. Do not modify the original note or source page. The original remains the canonical capture; the lifted claim now also lives on the target page.

## Phase 4: Index & commit

```bash
source .venv/bin/activate && python -m qmd document add --collection wiki --document-id "<target-path>" --markdown-file "<full-path>"
```

```bash
git add <target-path> provenance.jsonl
git commit -m "lift: <N> claims from <source> → <target>"
```

Confirm the commit hash.
