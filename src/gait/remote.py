from __future__ import annotations

import re
import hashlib
import json
import string
import urllib.request
import urllib.error
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .repo import GaitRepo

_OID_RE = re.compile(r"^[0-9a-f]{64}$")
_HEX = set(string.hexdigits.lower())

# ---------------------------------------------------------------------
# Canonical payload hashing rules (MUST match gait/objects.py)
# ---------------------------------------------------------------------

def _canonical_payload_bytes(raw: bytes) -> bytes:
    # Accept either canonical JSON bytes or canonical JSON bytes + "\n"
    return raw[:-1] if raw.endswith(b"\n") else raw


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_payload(raw: bytes) -> str:
    return _sha256_hex(_canonical_payload_bytes(raw))


# ---------------------------------------------------------------------
# HTTP helpers (urllib, consistent with your CLI style)
# ---------------------------------------------------------------------

def _http_bytes(method: str, url: str, *, token: str = "", body: Optional[bytes] = None, headers: Optional[dict] = None, timeout: float = 60.0) -> bytes:
    h = {}
    if token:
        h["Authorization"] = f"Bearer {token}"

    # If we are sending raw bytes, be explicit
    if body is not None:
        h.setdefault("Content-Type", "application/octet-stream")

    if headers:
        h.update(headers)

    req = urllib.request.Request(url, data=body, headers=h, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason} @ {url}: {txt}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Cannot reach {url}: {e}") from e


def _http_json(method: str, url: str, *, token: str = "", payload: Optional[dict] = None, headers: Optional[dict] = None, timeout: float = 60.0) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    if headers:
        h.update(headers)

    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason} @ {url}: {txt}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Cannot reach {url}: {e}") from e


def _norm_base(url: str) -> str:
    return url.rstrip("/")


def _repo_base(remote_url: str, owner: str, repo: str) -> str:
    return f"{_norm_base(remote_url)}/repos/{owner}/{repo}"


# ---------------------------------------------------------------------
# Remote config in .gait/config.json
# ---------------------------------------------------------------------

def _load_config(repo: GaitRepo) -> Dict[str, Any]:
    p = repo.gait_dir / "config.json"
    if not p.exists():
        return {"schema": "gait.config.v0", "remotes": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def _save_config(repo: GaitRepo, cfg: Dict[str, Any]) -> None:
    p = repo.gait_dir / "config.json"
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def remote_add(repo: GaitRepo, name: str, url: str) -> None:
    cfg = _load_config(repo)
    cfg.setdefault("remotes", {})
    cfg["remotes"][name] = {"url": url}
    _save_config(repo, cfg)


def remote_get(repo: GaitRepo, name: str) -> str:
    cfg = _load_config(repo)
    rem = (cfg.get("remotes") or {}).get(name) or {}
    url = (rem.get("url") or "").strip()
    if not url:
        raise ValueError(f"Remote not set: {name}. Use `gait remote add {name} <url>`.")
    return url


# ---------------------------------------------------------------------
# Spec + client
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class RemoteSpec:
    base_url: str   # e.g. http://127.0.0.1:8787
    owner: str
    repo: str
    name: str = "origin"


class RemoteClient:
    def __init__(self, spec: RemoteSpec, *, token: str) -> None:
        self.spec = spec
        self.token = token

    def base(self) -> str:
        return _repo_base(self.spec.base_url, self.spec.owner, self.spec.repo)

    # ---- objects ----

    def missing(self, oids: List[str]) -> List[str]:
        r = _http_json(
            "POST",
            f"{self.base()}/objects/missing",
            token=self.token,
            payload={"oids": oids},
        )
        return list(r.get("missing") or [])

    def get_object_bytes(self, oid: str) -> bytes:
        return _http_bytes("GET", f"{self.base()}/objects/{oid}")

    def put_object_bytes(self, oid: str, canon_bytes: bytes) -> None:
        # canon_bytes should NOT include newline
        _http_bytes("PUT", f"{self.base()}/objects/{oid}", token=self.token, body=canon_bytes)

    # ---- refs ----

    def get_refs(self) -> Dict[str, Any]:
        return _http_json("GET", f"{self.base()}/refs", token=self.token)

    def put_head_ref(self, branch: str, oid: str, *, expected_old: Optional[str]) -> None:
        headers = {}
        if expected_old is not None:
            headers["If-Match"] = expected_old
        _http_json("PUT", f"{self.base()}/refs/heads/{branch}", token=self.token, payload={"oid": oid}, headers=headers)

    def put_memory_ref(self, branch: str, oid: str, *, expected_old: Optional[str]) -> None:
        headers = {}
        if expected_old is not None:
            headers["If-Match"] = expected_old
        _http_json("PUT", f"{self.base()}/refs/memory/{branch}", token=self.token, payload={"oid": oid}, headers=headers)


# ---------------------------------------------------------------------
# Local object enumeration + storage
# ---------------------------------------------------------------------

def _is_oid(name: str) -> bool:
    if len(name) != 64:
        return False
    n = name.lower()
    return all(c in _HEX for c in n)

def _iter_local_oids(repo: GaitRepo) -> List[str]:
    if not repo.objects_dir.exists():
        return []
    out: List[str] = []
    for p in repo.objects_dir.rglob("*"):
        if not p.is_file():
            continue
        if _is_oid(p.name):
            out.append(p.name.lower())
    return out

def _store_local_object_bytes(repo: GaitRepo, oid: str, canon_bytes: bytes) -> None:
    # store as canonical bytes + newline (matches objects.py)
    sub = repo.objects_dir / oid[:2] / oid[2:4]
    sub.mkdir(parents=True, exist_ok=True)
    path = sub / oid
    if not path.exists():
        path.write_bytes(canon_bytes + b"\n")


def _load_local_object_bytes(repo: GaitRepo, oid: str) -> bytes:
    if not _OID_RE.match(oid):
        raise RuntimeError(f"Invalid oid encountered during push: {oid!r}")
    path = repo.objects_dir / oid[:2] / oid[2:4] / oid
    return path.read_bytes()


# ---------------------------------------------------------------------
# Dependency walking (commit/turn/memory)
# ---------------------------------------------------------------------

def _enqueue_deps(obj: Dict[str, Any], q: List[str]) -> None:
    schema = obj.get("schema") or ""
    if schema == "gait.commit.v0":
        for p in (obj.get("parents") or []):
            if p:
                q.append(p)
        for tid in (obj.get("turn_ids") or []):
            if tid:
                q.append(tid)
        sid = obj.get("snapshot_id")
        if sid:
            q.append(str(sid))
    elif schema == "gait.memory.v0":
        for it in (obj.get("items") or []):
            cid = it.get("commit_id")
            tid = it.get("turn_id")
            if cid:
                q.append(str(cid))
            if tid:
                q.append(str(tid))
    # gait.turn.v0 has no oid deps in v0


# ---------------------------------------------------------------------
# High-level operations
# ---------------------------------------------------------------------

def push(repo: GaitRepo, spec: RemoteSpec, *, token: str, branch: Optional[str] = None) -> None:
    branch = branch or repo.current_branch()
    client = RemoteClient(spec, token=token)

    local_head = repo.read_ref(branch)
    local_mem = repo.read_memory_ref(branch)

    all_oids = _iter_local_oids(repo)
    missing = client.missing(all_oids)

    for oid in missing:
        raw = _load_local_object_bytes(repo, oid)
        if _sha256_payload(raw) != oid:
            raise RuntimeError(f"Local object corrupt: {oid}")
        canon = _canonical_payload_bytes(raw)
        client.put_object_bytes(oid, canon)

    remote_refs = client.get_refs()
    remote_head_old = (remote_refs.get("heads") or {}).get(branch, "")
    remote_mem_old = (remote_refs.get("memory") or {}).get(branch, "")

    client.put_head_ref(branch, local_head, expected_old=remote_head_old)
    client.put_memory_ref(branch, local_mem, expected_old=remote_mem_old)


def fetch(repo: GaitRepo, spec: RemoteSpec, *, token: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    client = RemoteClient(spec, token=token)
    refs = client.get_refs()

    heads: Dict[str, str] = dict(refs.get("heads") or {})
    mems: Dict[str, str] = dict(refs.get("memory") or {})

    # write remote-tracking refs into local refs using nested paths
    for br, oid in heads.items():
        repo.write_ref(f"remotes/{spec.name}/{br}", oid or "")
    for br, oid in mems.items():
        repo.write_memory_ref(oid or "", f"remotes/{spec.name}/{br}")

    have: Set[str] = set(_iter_local_oids(repo))
    q: List[str] = []

    for oid in heads.values():
        if oid:
            q.append(oid)
    for oid in mems.values():
        if oid:
            q.append(oid)

    while q:
        oid = q.pop()
        if not oid or oid in have:
            continue

        raw = client.get_object_bytes(oid)
        if _sha256_payload(raw) != oid:
            raise RuntimeError(f"Remote sent bad object: {oid}")

        canon = _canonical_payload_bytes(raw)
        _store_local_object_bytes(repo, oid, canon)
        have.add(oid)

        try:
            obj = json.loads(canon.decode("utf-8"))
        except Exception:
            continue
        _enqueue_deps(obj, q)

    return heads, mems

def pull(repo: GaitRepo, spec: RemoteSpec, *, token: str, branch: Optional[str] = None, with_memory: bool = False) -> str:
    branch = branch or repo.current_branch()

    heads, mems = fetch(repo, spec, token=token)

    remote_tracking = f"remotes/{spec.name}/{branch}"
    remote_head = repo.read_ref(remote_tracking).strip()
    if not remote_head:
        raise RuntimeError(f"Remote branch not found: {spec.name}/{branch}")

    # fast-forward only
    new_head = repo.fast_forward_branch(branch, remote_head)

    # optionally fast-forward memory too (simple policy for Phase 1)
    if with_memory:
        remote_mem_ref = f"remotes/{spec.name}/{branch}"
        remote_mem = repo.read_memory_ref(remote_mem_ref).strip()
        if remote_mem:
            repo.write_memory_ref(remote_mem, branch)

    return new_head

def clone_into(dest: Path, spec: RemoteSpec, *, token: str, branch: str = "main") -> None:
    dest.mkdir(parents=True, exist_ok=True)
    repo = GaitRepo(root=dest)
    repo.init()

    remote_add(repo, spec.name, spec.base_url)

    heads, mems = fetch(repo, spec, token=token)

    head = heads.get(branch, "") or ""
    mem = mems.get(branch, "") or ""

    if head:
        repo.write_ref(branch, head)
    if mem:
        repo.write_memory_ref(mem, branch)

    repo.checkout(branch)

def remote_list(repo: GaitRepo) -> Dict[str, str]:
    cfg = _load_config(repo)
    remotes = cfg.get("remotes") or {}
    out: Dict[str, str] = {}
    for name, meta in remotes.items():
        url = (meta.get("url") or "").strip()
        if url:
            out[name] = url
    return out
