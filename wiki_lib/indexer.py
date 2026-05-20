# wiki_lib/indexer.py
import os
import subprocess
import json


class Indexer:
    def __init__(self, wiki_root: str, collection: str = "wiki"):
        self._root = wiki_root
        self._collection = collection
        self._indexed_dirs = ["pages", "drafts", "notes"]

    def _run_qmd(self, args: list[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python", "-m", "qmd"] + args,
            cwd=self._root,
            capture_output=True,
            text=True,
        )

    def _markdown_files(self) -> list[str]:
        files = []
        for dirname in self._indexed_dirs:
            dirpath = os.path.join(self._root, dirname)
            if not os.path.isdir(dirpath):
                continue
            for root, _, filenames in os.walk(dirpath):
                for fname in filenames:
                    if fname.endswith(".md") and not fname.startswith("."):
                        files.append(os.path.join(root, fname))
        return files

    def _doc_id(self, filepath: str) -> str:
        return os.path.relpath(filepath, self._root)

    def reindex(self):
        for filepath in self._markdown_files():
            self.add_document(filepath)

    def add_document(self, filepath: str):
        doc_id = self._doc_id(filepath)
        self._run_qmd([
            "document", "add",
            "--collection", self._collection,
            "--document-id", doc_id,
            "--markdown-file", filepath,
        ])

    def remove_document(self, filepath: str):
        doc_id = self._doc_id(filepath)
        self._run_qmd([
            "document", "remove",
            "--collection", self._collection,
            "--document-id", doc_id,
        ])

    def clear_collection(self):
        """Remove all documents from the collection."""
        result = self._run_qmd([
            "document", "list",
            "--collection", self._collection,
        ])
        if result.returncode != 0:
            return
        try:
            docs = json.loads(result.stdout)
            if isinstance(docs, list):
                for doc_id in docs:
                    if isinstance(doc_id, str):
                        # Use qmd directly to remove documents by ID
                        self._run_qmd([
                            "document", "delete",
                            "--collection", self._collection,
                            "--document-id", doc_id,
                        ])
                    else:
                        # If it's a dict, extract the document_id
                        extracted_id = doc_id.get("document_id", "")
                        if extracted_id:
                            self._run_qmd([
                                "document", "delete",
                                "--collection", self._collection,
                                "--document-id", extracted_id,
                            ])
        except json.JSONDecodeError:
            pass

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        result = self._run_qmd([
            "search",
            "--collection", self._collection,
            "--query", query,
            "--top-k", str(top_k),
        ])
        if result.returncode != 0 or not result.stdout.strip():
            return []
        return self._parse_search_output(result.stdout)

    def _parse_search_output(self, output: str) -> list[dict]:
        results = []
        try:
            data = json.loads(output)
            if isinstance(data, list):
                # Normalize the results to have document_id at top level
                for item in data:
                    normalized = {
                        "document_id": item.get("chunk_ref", {}).get("document_id", ""),
                        "score": item.get("score", 0.0),
                        "text": item.get("text", ""),
                    }
                    results.append(normalized)
                return results
        except json.JSONDecodeError:
            pass
        # Fallback: parse line-by-line if not JSON
        for line in output.strip().split("\n"):
            line = line.strip()
            if line:
                results.append({"raw": line, "score": 0.0, "document_id": ""})
        return results
