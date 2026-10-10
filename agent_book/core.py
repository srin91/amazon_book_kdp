"""One provider boundary. Demo mode is deterministic and costs nothing."""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ModelError(RuntimeError):
    pass


def live_text(instructions: str, user_input: str) -> str:
    """Call the Responses API. No tools, network browsing, or conversation storage."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ModelError("Set OPENAI_API_KEY for --live, or omit --live for demo mode.")
    payload = {
        "model": os.environ.get("OPENAI_MODEL", "gpt-5-mini"),
        "instructions": instructions,
        "input": user_input,
        "store": False,
    }
    request = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=45) as response:
            body = json.load(response)
    except HTTPError as exc:
        raise ModelError(f"API returned HTTP {exc.code}. Check model access, quota and key.") from exc
    except (URLError, TimeoutError) as exc:
        raise ModelError("Could not reach the API. Check your network and retry.") from exc
    texts = [part.get("text", "") for item in body.get("output", [])
             for part in item.get("content", []) if part.get("type") == "output_text"]
    if not texts:
        raise ModelError("API returned no output text; inspect your model configuration.")
    return "\n".join(texts).strip()


def constrained_json(instructions: str, user_input: str) -> dict:
    """Parse untrusted model text and require an object; callers validate fields."""
    raw = live_text(instructions + " Reply with one JSON object only, no Markdown.", user_input)
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ModelError("Model did not return valid JSON; retry or use demo mode.") from exc
    if not isinstance(value, dict):
        raise ModelError("Model returned JSON with the wrong shape.")
    return value


def bounded(value: str, limit: int = 12000) -> str:
    if len(value) > limit:
        raise ValueError(f"Input exceeds {limit} characters; split it first.")
    return value

