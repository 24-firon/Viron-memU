from __future__ import annotations

from typing import Any

from memu.llm.backends.base import LLMBackend


class GoogleLLMBackend(LLMBackend):
    """Backend for Google Generative AI."""

    name = "google"
    summary_endpoint = ""

    def build_summary_payload(
        self, *, text: str, system_prompt: str | None, chat_model: str, max_tokens: int | None
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "contents": [
                {
                    "parts": [{"text": text}],
                    "role": "user"
                }
            ],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }
        if max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens
        return payload

    def parse_summary_response(self, data: dict[str, Any]) -> str:
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return str(data)

    def build_vision_payload(
        self,
        *,
        prompt: str,
        base64_image: str,
        mime_type: str,
        system_prompt: str | None,
        chat_model: str,
        max_tokens: int | None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inlineData": {
                                "mimeType": mime_type,
                                "data": base64_image
                            }
                        }
                    ],
                    "role": "user"
                }
            ],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [{"text": system_prompt}]
            }
        if max_tokens:
            payload["generationConfig"]["maxOutputTokens"] = max_tokens
        return payload
