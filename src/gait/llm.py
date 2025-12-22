from __future__ import annotations

import json
import urllib.request
import urllib.error
from typing import Any, Dict, Optional


# ----------------------------
# Small HTTP helpers (urllib)
# ----------------------------

def _http_json(
    url: str,
    *,
    method: str = "GET",
    payload: Optional[dict] = None,
    headers: Optional[dict] = None,
    timeout: float = 60.0,
) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Cannot reach {url}: {e}") from e


# ============================
# Ollama provider
# ============================

def _ollama_url(host: str, path: str) -> str:
    host = host.rstrip("/")
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
    return host + path


def ollama_list_models(host: str) -> list[str]:
    r = _http_json(_ollama_url(host, "/api/tags"), method="GET")
    models: list[str] = []
    for m in (r.get("models") or []):
        name = m.get("name")
        if name:
            models.append(name)
    return models


def ollama_chat(
    host: str,
    model: str,
    messages: list[dict],
    *,
    temperature: float | None = None,
    num_predict: int | None = None,
    debug: bool = False,
) -> str:
    """
    If num_predict is None, we DO NOT send options.num_predict.
    That means: no explicit output cap (use Ollama/model defaults).
    """
    payload: dict = {
        "model": model,
        "messages": messages,
        "stream": False,
    }

    options: dict[str, Any] = {}
    if temperature is not None:
        options["temperature"] = float(temperature)
    if num_predict is not None:
        options["num_predict"] = int(num_predict)

    if options:
        payload["options"] = options

    r = _http_json(_ollama_url(host, "/api/chat"), method="POST", payload=payload, timeout=600.0)

    if debug:
        done_reason = r.get("done_reason") or r.get("doneReason")
        if done_reason:
            print(f"[gait] ollama done_reason={done_reason}")

    return ((r.get("message") or {}).get("content")) or ""


# ============================
# OpenAI-compatible provider (Foundry Local / LM Studio)
# ============================

def _openai_base(base_url: str) -> str:
    # Accept:
    #   http://127.0.0.1:63545
    #   http://127.0.0.1:63545/v1
    b = base_url.rstrip("/")
    if b.endswith("/v1"):
        return b
    return b + "/v1"


def openai_compat_list_models(base_url: str, api_key: str = "") -> list[str]:
    b = _openai_base(base_url)
    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    r = _http_json(f"{b}/models", method="GET", headers=headers, timeout=30.0)

    out: list[str] = []
    for item in (r.get("data") or []):
        mid = item.get("id")
        if mid:
            out.append(mid)
    return out


def openai_compat_chat(
    base_url: str,
    model: str,
    messages: list[dict],
    *,
    api_key: str = "",
    temperature: float | None = None,
    max_tokens: int | None = None,
    debug: bool = False,
) -> str:
    """
    If max_tokens is None, we DO NOT send it.
    That means: no explicit output cap (server/model default).
    """
    b = _openai_base(base_url)
    headers: dict[str, str] = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": False,
    }
    if temperature is not None:
        payload["temperature"] = float(temperature)
    if max_tokens is not None:
        payload["max_tokens"] = int(max_tokens)

    r = _http_json(f"{b}/chat/completions", method="POST", payload=payload, headers=headers, timeout=600.0)

    if debug:
        choices = r.get("choices") or []
        if choices and isinstance(choices, list):
            fr = (choices[0] or {}).get("finish_reason")
            if fr:
                print(f"[gait] openai_compat finish_reason={fr}")

    choices = r.get("choices") or []
    if choices and isinstance(choices, list):
        msg = (choices[0] or {}).get("message") or {}
        content = msg.get("content")
        if isinstance(content, str):
            return content

    return ""
