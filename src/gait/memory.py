from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional
import time


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


@dataclass(frozen=True)
class MemoryItem:
    pinned_at: str
    commit_id: str
    turn_id: str
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MemoryManifest:
    schema: str
    created_at: str
    items: List[MemoryItem] = field(default_factory=list)

    @staticmethod
    def empty() -> "MemoryManifest":
        return MemoryManifest(schema="gait.memory.v0", created_at=now_iso(), items=[])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "created_at": self.created_at,
            "items": [it.to_dict() for it in self.items],
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "MemoryManifest":
        items = []
        for it in d.get("items") or []:
            items.append(
                MemoryItem(
                    pinned_at=it.get("pinned_at", ""),
                    commit_id=it.get("commit_id", ""),
                    turn_id=it.get("turn_id", ""),
                    note=it.get("note", "") or "",
                )
            )
        return MemoryManifest(
            schema=d.get("schema", "gait.memory.v0"),
            created_at=d.get("created_at", ""),
            items=items,
        )
