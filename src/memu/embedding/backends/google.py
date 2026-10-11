from __future__ import annotations

from typing import Any

from memu.embedding.backends.base import EmbeddingBackend


class GoogleEmbeddingBackend(EmbeddingBackend):
    """Backend for Google Generative AI embedding API."""

    name = "google"
    embedding_endpoint = ""

    def build_embedding_payload(self, *, inputs: list[str], embed_model: str) -> dict[str, Any]:
        return {
            "requests": [
                {"model": f"models/{embed_model}", "content": {"parts": [{"text": text}]}}
                for text in inputs
            ]
        }

    def parse_embedding_response(self, data: dict[str, Any]) -> list[list[float]]:
        results: list[list[float]] = []
        for item in data.get("embeddings", []):
            if "values" in item:
                results.append(item["values"])
            elif "embedding" in item and isinstance(item["embedding"], dict):
                results.append(item["embedding"].get("values", []))
            else:
                results.append([])
        return results
