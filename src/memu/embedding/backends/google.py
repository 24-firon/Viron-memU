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
        return [item.get("embedding", {}).get("values", []) for item in data.get("embeddings", [])]
