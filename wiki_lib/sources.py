# wiki_lib/sources.py
import json
import os
from datetime import date


class SourceRegistry:
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

    def _save(self):
        with open(self._path, "w") as f:
            for entry in self._entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def add(self, key: str, title: str, url: str, source_type: str,
            one_liner: str | None = None, **kwargs) -> dict:
        entry = {
            "key": key,
            "title": title,
            "url": url,
            "source_type": source_type,
            "one_liner": one_liner,
            "ingest_date": str(date.today()),
            **kwargs,
        }
        self._entries.append(entry)
        self._save()
        return entry

    def get(self, key: str) -> dict | None:
        for e in self._entries:
            if e["key"] == key:
                return e
        return None

    def list_all(self) -> list[dict]:
        return list(self._entries)

    def update(self, key: str, **fields) -> dict | None:
        for e in self._entries:
            if e["key"] == key:
                e.update(fields)
                self._save()
                return e
        return None

    def check_url(self, url: str) -> str | None:
        normalized = url.rstrip("/").replace("http://", "https://")
        for e in self._entries:
            entry_url = (e.get("url") or "").rstrip("/").replace("http://", "https://")
            if normalized == entry_url or normalized in entry_url or entry_url in normalized:
                return e["key"]
        return None
