from __future__ import annotations

import os
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

# ============================
# Gemini provider (Google Generative Language API, REST)
# ============================

def _gemini_api_key() -> str:
    key = (os.environ.get("GEMINI_API_KEY", "") or os.environ.get("GOOGLE_API_KEY", "")).strip()
    if not key:
        raise RuntimeError("Missing Gemini API key. Set GEMINI_API_KEY (or GOOGLE_API_KEY).")
    return key


def gemini_list_models(api_key: str = "") -> list[str]:
    api_key = (api_key or "").strip() or _gemini_api_key()

    # v1beta models list
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    r = _http_json(url, method="GET", timeout=30.0)

    out: list[str] = []
    for m in (r.get("models") or []):
        name = (m.get("name") or "").strip()
        if name:
            out.append(name)
    return out


def gemini_chat(
    model: str,
    messages: list[dict],
    *,
    api_key: str = "",
    temperature: float | None = None,
    max_tokens: int | None = None,
    debug: bool = False,
) -> str:
    api_key = (api_key or "").strip() or _gemini_api_key()

    model_id = (model or "").strip()
    if not model_id:
        raise RuntimeError("gemini_chat: model is required.")
    if not model_id.startswith("models/"):
        model_id = f"models/{model_id}"

    url = f"https://generativelanguage.googleapis.com/v1beta/{model_id}:generateContent?key={api_key}"

    # GAIT -> Gemini mapping:
    # - system messages become system_instruction.parts[]
    # - user/assistant become contents[] with roles user/model
    system_parts: list[dict] = []
    contents: list[dict] = []

    for m in messages:
        role = (m.get("role") or "").strip()
        text = (m.get("content") or "")
        if not isinstance(text, str):
            continue
        text = text.strip()
        if not text:
            continue

        if role == "system":
            system_parts.append({"text": text})
            continue

        gem_role = "user" if role == "user" else "model"
        contents.append({"role": gem_role, "parts": [{"text": text}]})

    payload: Dict[str, Any] = {"contents": contents}

    if system_parts:
        payload["system_instruction"] = {"parts": system_parts}

    gen_cfg: Dict[str, Any] = {}
    if temperature is not None:
        gen_cfg["temperature"] = float(temperature)
    if max_tokens is not None:
        gen_cfg["maxOutputTokens"] = int(max_tokens)
    if gen_cfg:
        payload["generationConfig"] = gen_cfg

    r = _http_json(url, method="POST", payload=payload, timeout=600.0)

    if debug:
        # Gemini responses vary, but candidates[0] is typical
        fc = (r.get("candidates") or [{}])[0]
        if isinstance(fc, dict) and fc.get("finishReason"):
            print(f"[gait] gemini finishReason={fc.get('finishReason')}")

    candidates = r.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"Gemini returned no candidates: {r}")

    content = (candidates[0] or {}).get("content") or {}
    parts = content.get("parts") or []
    texts: list[str] = []
    for p in parts:
        t = (p or {}).get("text")
        if isinstance(t, str) and t:
            texts.append(t)

    out = "".join(texts).strip()
    if not out:
        # some errors come back with "promptFeedback" etc
        raise RuntimeError(f"Gemini returned empty text parts: {r}")
    return out

# ============================
# Claude / Anthropic provider (Messages API)
# ============================

def _anthropic_api_key() -> str:
    key = (os.environ.get("ANTHROPIC_API_KEY", "")).strip()
    if not key:
        raise RuntimeError("Missing Anthropic API key. Set ANTHROPIC_API_KEY.")
    return key


def anthropic_list_models(api_key: str = "", *, base_url: str = "https://api.anthropic.com") -> list[str]:
    api_key = (api_key or "").strip() or _anthropic_api_key()
    b = base_url.rstrip("/")
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    r = _http_json(f"{b}/v1/models", method="GET", headers=headers, timeout=30.0)

    out: list[str] = []
    for item in (r.get("data") or []):
        mid = item.get("id")
        if mid:
            out.append(mid)
    return out


def anthropic_chat(
    model: str,
    messages: list[dict],
    *,
    api_key: str = "",
    max_tokens: int | None = None,
    temperature: float | None = None,
    base_url: str = "https://api.anthropic.com",
    debug: bool = False,
) -> str:
    """
    Maps GAIT messages -> Anthropic Messages API.
    - GAIT system messages => joined into a single `system` string.
    - user/assistant => `messages` with roles user/assistant
    """
    api_key = (api_key or "").strip() or _anthropic_api_key()

    model_id = (model or "").strip()
    if not model_id:
        raise RuntimeError("anthropic_chat: model is required.")

    # Collect system text
    sys_chunks: list[str] = []
    amsgs: list[dict] = []

    for m in messages:
        role = (m.get("role") or "").strip()
        text = m.get("content")
        if not isinstance(text, str):
            continue
        text = text.strip()
        if not text:
            continue

        if role == "system":
            sys_chunks.append(text)
            continue

        if role not in ("user", "assistant"):
            # ignore unknown roles
            continue

        amsgs.append({"role": role, "content": text})

    payload: Dict[str, Any] = {
        "model": model_id,
        "messages": amsgs,
        # Anthropic requires max_tokens; choose a safe default if user didn't set one.
        "max_tokens": int(max_tokens) if max_tokens is not None else 1024,
    }

    if sys_chunks:
        payload["system"] = "\n\n".join(sys_chunks)

    if temperature is not None:
        payload["temperature"] = float(temperature)

    b = base_url.rstrip("/")
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

    r = _http_json(f"{b}/v1/messages", method="POST", payload=payload, headers=headers, timeout=600.0)

    if debug:
        sr = r.get("stop_reason")
        if sr:
            print(f"[gait] anthropic stop_reason={sr}")

    # Response content is an array of blocks; collect text blocks.
    blocks = r.get("content") or []
    texts: list[str] = []
    for b in blocks:
        if isinstance(b, dict) and b.get("type") == "text":
            t = b.get("text")
            if isinstance(t, str) and t:
                texts.append(t)

    out = "".join(texts).strip()
    if not out:
        raise RuntimeError(f"Anthropic returned empty text blocks: {r}")
    return out
