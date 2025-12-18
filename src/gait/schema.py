from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional
import time


def now_iso() -> str:
    # ISO-ish without timezone complexity (v0)
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


@dataclass(frozen=True)
class Tokens:
    input_total: Optional[int] = None
    output_total: Optional[int] = None
    estimated: bool = True
    by_role: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Turn:
    schema: str
    created_at: str
    user: Dict[str, Any]
    assistant: Dict[str, Any]
    context: Dict[str, Any] = field(default_factory=dict)
    tools: Dict[str, Any] = field(default_factory=dict)
    model: Dict[str, Any] = field(default_factory=dict)
    tokens: Tokens = field(default_factory=Tokens)
    visibility: str = "private"  # private|shareable

    @staticmethod
    def v0(
        user_text: str,
        assistant_text: str,
        *,
        context: Optional[Dict[str, Any]] = None,
        tools: Optional[Dict[str, Any]] = None,
        model: Optional[Dict[str, Any]] = None,
        tokens: Optional[Tokens] = None,
        visibility: str = "private",
    ) -> "Turn":
        return Turn(
            schema="gait.turn.v0",
            created_at=now_iso(),
            user={"type": "message", "text": user_text},
            assistant={"type": "message", "text": assistant_text},
            context=context or {},
            tools=tools or {},
            model=model or {},
            tokens=tokens or Tokens(),
            visibility=visibility,
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["tokens"] = self.tokens.to_dict()
        return d


@dataclass(frozen=True)
class Commit:
    schema: str
    created_at: str
    parents: List[str]
    turn_ids: List[str]
    snapshot_id: Optional[str]
    branch: str
    kind: str = "auto"  # auto|blessed|merge
    message: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def v0(
        *,
        parents: List[str],
        turn_ids: List[str],
        branch: str,
        snapshot_id: Optional[str] = None,
        kind: str = "auto",
        message: str = "",
        meta: Optional[Dict[str, Any]] = None,
    ) -> "Commit":
        return Commit(
            schema="gait.commit.v0",
            created_at=now_iso(),
            parents=parents,
            turn_ids=turn_ids,
            snapshot_id=snapshot_id,
            branch=branch,
            kind=kind,
            message=message,
            meta=meta or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
