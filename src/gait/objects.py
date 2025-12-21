from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Tuple


def canonical_json_bytes(obj: Any) -> bytes:
    """
    Canonical JSON for stable hashing:
    - UTF-8
    - sorted keys
    - no whitespace variance
    """
    s = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return s.encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def object_id(obj: Any) -> str:
    return sha256_hex(canonical_json_bytes(obj))


def fanout_path(objects_dir: Path, oid: str) -> Path:
    return objects_dir / oid[:2] / oid[2:4] / oid

def canonical_payload_bytes(raw: bytes) -> bytes:
    return raw[:-1] if raw.endswith(b"\n") else raw

def store_object(objects_dir: Path, obj: Dict[str, Any]) -> str:
    """
    Stores a JSON object content-addressed by sha256(canonical_json(obj)).
    Returns oid.
    """
    oid = object_id(obj)
    path = fanout_path(objects_dir, oid)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(canonical_json_bytes(obj) + b"\n")
    return oid

def resolve_prefix(objects_dir: Path, prefix: str) -> str:
    prefix = prefix.strip()
    if len(prefix) >= 64:
        return prefix

    if len(prefix) < 2:
        base = objects_dir
    elif len(prefix) < 4:
        base = objects_dir / prefix[:2]
    else:
        base = objects_dir / prefix[:2] / prefix[2:4]

    if not base.exists():
        raise FileNotFoundError(f"No object found with prefix: {prefix}")

    matches = []
    # Only scan files in the narrowed directory tree
    for p in base.rglob("*"):
        if p.is_file() and p.name.startswith(prefix):
            matches.append(p.name)

    if not matches:
        raise FileNotFoundError(f"No object found with prefix: {prefix}")
    if len(matches) > 1:
        cand = ", ".join(m[:12] for m in matches[:10])
        raise ValueError(f"Ambiguous prefix {prefix} matches {len(matches)} objects: {cand} ...")

    return matches[0]

def load_object(objects_dir: Path, oid: str) -> Dict[str, Any]:
    oid = resolve_prefix(objects_dir, oid)
    path = fanout_path(objects_dir, oid)
    if not path.exists():
        raise FileNotFoundError(f"Object not found: {oid}")
    raw = path.read_text(encoding="utf-8").strip()
    return json.loads(raw)

def short_oid(oid: str, n: int = 8) -> str:
    return oid[:n]
