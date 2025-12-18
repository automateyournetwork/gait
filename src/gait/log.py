from __future__ import annotations

from typing import Dict, Iterator, List, Optional, Set, Tuple

from .repo import GaitRepo


def walk_commits(repo: GaitRepo, start_commit: Optional[str] = None, limit: int = 50) -> Iterator[Dict]:
    """
    Simple parent-walk (first parent) for v0.
    """
    cid = start_commit if start_commit is not None else repo.head_commit_id()
    seen: Set[str] = set()
    n = 0
    while cid and cid not in seen and n < limit:
        seen.add(cid)
        c = repo.get_commit(cid)
        c["_id"] = cid
        yield c
        parents = c.get("parents") or []
        cid = parents[0] if parents else ""
        n += 1
