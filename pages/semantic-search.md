---
sources:
  - example-rag-primer
---

# Semantic Search

This is an example topic page demonstrating the shape of `pages/*.md`. Replace it with your own synthesis once you have 3+ sources or subtopics worth tying together.

A topic page synthesizes claims across multiple sources, framed with epistemic stance ("X proposes...", "according to Y..."). Inline citations are not used — provenance is tracked in `provenance.jsonl`.

## Hybrid retrieval

The example primer proposes that hybrid retrieval combining sparse (BM25) and dense (vector) signals tends to outperform either alone on heterogeneous corpora. The framing is general and not tied to a specific benchmark.

## Reranking

A cross-encoder rerank stage is presented as a common quality lever — applied to a wider candidate set produced by the first-stage retriever — at the cost of additional latency.

## Caveats

This page is illustrative. The example primer is a placeholder, not a real document; treat its claims as scaffolding rather than evidence.
