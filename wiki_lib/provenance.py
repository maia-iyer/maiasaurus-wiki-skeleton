# wiki_lib/provenance.py
import json
import os
from datetime import date


class ProvenanceLog:
    def __init__(self, path: str):
        self._path = path
        self._entries: list[dict] = []
        self._load()

    def _load(self):
        self._entries = []
        if os.path.exists(self._path):
            with open(self._path) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self._entries.append(json.loads(line))

    def log(self, page: str, section: str, origin: str, claim: str, **kwargs):
        entry = {
            "page": page,
            "section": section,
            "origin": origin,
            "claim": claim,
            "ts": str(date.today()),
            **kwargs,
        }
        self._entries.append(entry)
        with open(self._path, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def for_page(self, page: str) -> list[dict]:
        return [e for e in self._entries if e["page"] == page]

    def for_source(self, source_key: str) -> list[dict]:
        return [e for e in self._entries if e.get("source_key") == source_key]

    def for_section(self, page: str, section: str) -> list[dict]:
        return [e for e in self._entries
                if e["page"] == page and e["section"] == section]

    def all_entries(self) -> list[dict]:
        return list(self._entries)
