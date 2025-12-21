from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .repo import GaitRepo
from .objects import canonical_payload_bytes

def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def verify_repo(repo: GaitRepo) -> Dict[str, Any]:
    problems: List[str] = []
    checked_objects = 0

    # 1) HEAD sanity
    try:
        head_ref = repo.head_ref_path()
        if not head_ref.exists():
            problems.append(f"HEAD points to missing ref: {head_ref}")
    except Exception as e:
        problems.append(f"Invalid HEAD: {e}")

    # 2) verify refs
    def verify_ref_file(path: Path) -> None:
        nonlocal checked_objects
        oid = path.read_text(encoding="utf-8").strip()
        if not oid:
            return
        obj_path = repo.objects_dir / oid[:2] / oid[2:4] / oid
        if not obj_path.exists():
            problems.append(f"Missing object for ref {path}: {oid}")
            return
        raw = obj_path.read_bytes()
        canon = canonical_payload_bytes(raw)
        if _sha256_hex(canon) != oid:
            problems.append(f"Bad hash for object {oid} referenced by {path}")
        checked_objects += 1

    # heads + memory refs
    if repo.refs_dir.exists():
        for p in repo.refs_dir.rglob("*"):
            if p.is_file():
                verify_ref_file(p)

    if repo.memory_refs_dir.exists():
        for p in repo.memory_refs_dir.rglob("*"):
            if p.is_file():
                verify_ref_file(p)

    # 3) optionally verify ALL objects on disk
    for p in repo.objects_dir.rglob("*"):
        if not p.is_file():
            continue
        oid = p.name
        if len(oid) != 64:
            continue
        raw = p.read_bytes()
        canon = canonical_payload_bytes(raw)
        if _sha256_hex(canon) != oid:
            problems.append(f"Bad object on disk: {p}")

    return {
        "ok": len(problems) == 0,
        "problems": problems,
        "checked_ref_objects": checked_objects,
    }
