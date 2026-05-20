# wiki_lib/linter.py
import json
import os
import re

import yaml


class Linter:
    def __init__(self, wiki_root: str):
        self._root = wiki_root
        self._sources = self._load_jsonl("sources.jsonl")
        self._provenance = self._load_jsonl("provenance.jsonl")

    def _load_jsonl(self, filename: str) -> list[dict]:
        path = os.path.join(self._root, filename)
        entries = []
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entries.append(json.loads(line))
        return entries

    def _parse_frontmatter(self, filepath: str) -> dict | None:
        with open(filepath) as f:
            content = f.read()
        if not content.startswith("---"):
            return None
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        try:
            return yaml.safe_load(parts[1])
        except Exception:
            return None

    def _all_pages(self) -> list[str]:
        pages_dir = os.path.join(self._root, "pages")
        result = []
        if not os.path.isdir(pages_dir):
            return result
        for root, _, files in os.walk(pages_dir):
            for f in files:
                if f.endswith(".md") and not f.startswith("."):
                    result.append(os.path.join(root, f))
        return result

    def _rel(self, path: str) -> str:
        return os.path.relpath(path, self._root)

    def run(self) -> list[dict]:
        errors = []
        errors.extend(self._check_frontmatter())
        errors.extend(self._check_source_keys())
        errors.extend(self._check_internal_links())
        errors.extend(self._check_uncited_sources())
        errors.extend(self._check_provenance_targets())
        return errors

    def _check_frontmatter(self) -> list[dict]:
        errors = []
        for filepath in self._all_pages():
            rel = self._rel(filepath)
            fm = self._parse_frontmatter(filepath)
            if fm is None:
                errors.append({"file": rel, "message": f"Missing frontmatter in {rel}"})
                continue
            if "/sources/" in filepath:
                if "source_key" not in fm:
                    errors.append({"file": rel, "message": f"Source page {rel} missing 'source_key' in frontmatter"})
            else:
                if "sources" not in fm:
                    errors.append({"file": rel, "message": f"Topic page {rel} missing 'sources' in frontmatter"})
        return errors

    def _check_source_keys(self) -> list[dict]:
        errors = []
        known_keys = {s["key"] for s in self._sources}
        for filepath in self._all_pages():
            if "/sources/" not in filepath:
                continue
            fm = self._parse_frontmatter(filepath)
            if fm and fm.get("source_key") and fm["source_key"] not in known_keys:
                rel = self._rel(filepath)
                errors.append({"file": rel, "message": f"Source page {rel} references unknown key '{fm['source_key']}' not in sources.jsonl"})
        return errors

    def _check_internal_links(self) -> list[dict]:
        errors = []
        link_re = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')
        for filepath in self._all_pages():
            rel = self._rel(filepath)
            with open(filepath) as f:
                content = f.read()
            for match in link_re.finditer(content):
                target = match.group(2)
                if target.startswith("http://") or target.startswith("https://"):
                    continue
                if target.startswith("#"):
                    continue
                resolved = os.path.normpath(os.path.join(os.path.dirname(filepath), target))
                if not os.path.exists(resolved):
                    errors.append({"file": rel, "message": f"Broken link to '{target}' in {rel}"})
        return errors

    def _check_uncited_sources(self) -> list[dict]:
        errors = []
        cited_keys = {e.get("source_key") for e in self._provenance if e.get("source_key")}
        for source in self._sources:
            if source["key"] not in cited_keys:
                errors.append({"file": "sources.jsonl", "message": f"Source '{source['key']}' never cited in provenance"})
        return errors

    def _check_provenance_targets(self) -> list[dict]:
        errors = []
        for entry in self._provenance:
            page_path = os.path.join(self._root, entry["page"])
            if not os.path.exists(page_path):
                errors.append({"file": entry["page"], "message": f"Provenance references missing page '{entry['page']}'"})
        return errors
