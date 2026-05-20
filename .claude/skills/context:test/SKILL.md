---
name: context:test
description: Test what context would be loaded for a given query — manifest with token counts
user-invocable: true
allowed-tools: Bash, Read
---

# Context Test

Verify what context gets loaded when skills search the wiki. Shows ranked results with token estimates.

Usage: `/context:test "<query>" [--budget <tokens>] [--top-k <N>]`

Defaults: budget = 4000 tokens, top-k = 10

## Procedure

1. Run the search:

```bash
python -m qmd search --collection wiki --query "<query>" --top-k <N>
```

2. For each result, estimate tokens (chars / 4 as rough approximation).

3. Accumulate results highest-score-first until the token budget is reached.

4. Present the manifest:

```
Query: "<query>"

Results (top N, budget: <budget> tokens):
  1. <document_id> §<section>
     Score: <score> | Tokens: ~<estimate>
  2. ...

Total: ~<sum> tokens (of <budget> budget)
Coverage: <N> topic pages, <N> source pages, <N> initiatives, <N> notes
Excluded (over budget): <list of document_ids that didn't fit>
```

5. If no results are returned, report: "No results for this query. The collection may need reindexing (`./wiki reindex`) or the query may not match any indexed content."

## Interpretation guidance

After presenting results, briefly note:
- Whether the top results seem relevant to the query (based on document_id and section names)
- Whether important-seeming content is missing (based on what you'd expect for the query)
- Whether the budget is being consumed by low-relevance results

Do not make changes — this skill is read-only diagnostic.
