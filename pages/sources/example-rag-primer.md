---
source_key: example-rag-primer
url: https://example.com/rag-primer
source_type: blog
ingested: 2026-05-20
---

# Example: A Primer on Retrieval-Augmented Generation

This is an example source page demonstrating the shape of `pages/sources/*.md`. Replace it with real ingested sources via `/ingest <url>`.

A source page is a minimal, faithful summary of one document. The `source_key` in frontmatter must match an entry in `sources.jsonl`.

## Key Claims

- **Claim 1**: Retrieval-augmented generation pairs a retriever (often a vector index) with a generator LLM, letting the model condition on documents outside its training data.
- **Claim 2**: Hybrid retrieval (sparse + dense) typically outperforms either alone on heterogeneous corpora.
- **Claim 3**: Reranking a wide candidate set with a cross-encoder is a common quality lever, at the cost of latency.

## Relevance

Demonstrates how a source page captures discrete, attributable claims that can be promoted (via `/lift`) into topic pages with provenance preserved.
