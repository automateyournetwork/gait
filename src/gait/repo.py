from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, List
import json

from .objects import store_object, load_object
from .schema import Turn, Commit
from .memory import MemoryManifest, MemoryItem, now_iso

GAIT_DIR = ".gait"


@dataclass
class GaitRepo:
    root: Path

    # ----------------------------
    # Paths
    # ----------------------------

    @property
    def gait_dir(self) -> Path:
        return self.root / GAIT_DIR

    @property
    def objects_dir(self) -> Path:
        return self.gait_dir / "objects"

    @property
    def refs_dir(self) -> Path:
        return self.gait_dir / "refs" / "heads"

    @property
    def memory_refs_dir(self) -> Path:
        return self.gait_dir / "refs" / "memory"

    @property
    def head_file(self) -> Path:
        return self.gait_dir / "HEAD"

    @property
    def turns_log(self) -> Path:
        return self.gait_dir / "turns.jsonl"

    @property
    def memory_log(self) -> Path:
        return self.gait_dir / "memory.jsonl"

    # ----------------------------
    # Setup / discover
    # ----------------------------

    def exists(self) -> bool:
        return self.gait_dir.exists() and self.head_file.exists()

    @staticmethod
    def discover(start: Optional[Path] = None) -> "GaitRepo":
        cur = (start or Path.cwd()).resolve()
        for p in [cur] + list(cur.parents):
            if (p / GAIT_DIR).exists():
                return GaitRepo(root=p)
        raise FileNotFoundError("No .gait directory found (run `gait init`).")

    def init(self) -> None:
        self.gait_dir.mkdir(parents=True, exist_ok=True)
        self.objects_dir.mkdir(parents=True, exist_ok=True)
        self.refs_dir.mkdir(parents=True, exist_ok=True)
        self.memory_refs_dir.mkdir(parents=True, exist_ok=True)

        # default branch
        main_ref = self.refs_dir / "main"
        if not main_ref.exists():
            main_ref.write_text("", encoding="utf-8")

        # HEAD points to refs/heads/main
        if not self.head_file.exists():
            self.head_file.write_text("ref: refs/heads/main\n", encoding="utf-8")

        # turns log
        if not self.turns_log.exists():
            self.turns_log.write_text("", encoding="utf-8")

        # memory reflog
        if not self.memory_log.exists():
            self.memory_log.write_text("", encoding="utf-8")

        # default memory ref for main (points to empty manifest object)
        main_mem_ref = self.memory_refs_dir / "main"
        if not main_mem_ref.exists():
            empty = MemoryManifest.empty()
            mem_id = store_object(self.objects_dir, empty.to_dict())
            main_mem_ref.write_text(mem_id + "\n", encoding="utf-8")

    # ----------------------------
    # HEAD / refs
    # ----------------------------

    def head_ref_path(self) -> Path:
        head = self.head_file.read_text(encoding="utf-8").strip()
        if not head.startswith("ref: "):
            raise ValueError("HEAD is detached or invalid in v0 (expected ref: ...).")
        ref = head[len("ref: ") :].strip()
        return self.gait_dir / ref

    def current_branch(self) -> str:
        return self.head_ref_path().name

    def read_ref(self, branch: str) -> str:
        path = self.refs_dir / branch
        if not path.exists():
            raise FileNotFoundError(f"Branch does not exist: {branch}")
        return path.read_text(encoding="utf-8").strip()

    def write_ref(self, branch: str, commit_id: str) -> None:
        path = self.refs_dir / branch
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(commit_id + "\n", encoding="utf-8")

    def head_commit_id(self) -> str:
        return self.read_ref(self.current_branch())

    # ----------------------------
    # Memory refs + reflog
    # ----------------------------

    def memory_ref_path(self, branch: Optional[str] = None) -> Path:
        b = branch or self.current_branch()
        return self.memory_refs_dir / b

    def read_memory_ref(self, branch: Optional[str] = None) -> str:
        path = self.memory_ref_path(branch)
        if not path.exists():
            empty = MemoryManifest.empty()
            mem_id = store_object(self.objects_dir, empty.to_dict())
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(mem_id + "\n", encoding="utf-8")
            return mem_id
        return path.read_text(encoding="utf-8").strip()

    def write_memory_ref(self, mem_id: str, branch: Optional[str] = None) -> None:
        path = self.memory_ref_path(branch)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(mem_id + "\n", encoding="utf-8")

    def append_memory_log(
        self,
        *,
        branch: str,
        old_mem: str,
        new_mem: str,
        reason: str,
        note: str = "",
        meta: Optional[Dict[str, Any]] = None,
        head_commit: Optional[str] = None,
    ) -> None:
        """
        Memory reflog entry. Record HEAD at time of memory change.
        """
        entry = {
            "ts": __import__("datetime").datetime.now(__import__("datetime").UTC).replace(microsecond=0).isoformat(),
            "branch": branch,
            "head_commit": head_commit if head_commit is not None else self.read_ref(branch),
            "old_mem": old_mem,
            "new_mem": new_mem,
            "reason": reason,
            "note": note,
            "meta": meta or {},
        }
        with self.memory_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_memory(self, branch: Optional[str] = None) -> MemoryManifest:
        mem_id = self.read_memory_ref(branch)
        obj = load_object(self.objects_dir, mem_id)
        return MemoryManifest.from_dict(obj)

    def set_memory(self, manifest: MemoryManifest, branch: Optional[str] = None) -> str:
        mem_id = store_object(self.objects_dir, manifest.to_dict())
        self.write_memory_ref(mem_id, branch)
        return mem_id

    def build_context_bundle(self, *, full: bool = False) -> Dict[str, Any]:
        branch = self.current_branch()
        manifest = self.get_memory(branch)

        items = []
        for idx, it in enumerate(manifest.items, start=1):
            turn = self.get_turn(it.turn_id)
            entry: Dict[str, Any] = {
                "index": idx,
                "turn_id": it.turn_id,
                "commit_id": it.commit_id,
                "note": it.note,
                "pinned_at": it.pinned_at,
                "user_text": (turn.get("user") or {}).get("text", ""),
                "assistant_text": (turn.get("assistant") or {}).get("text", ""),
            }
            if full:
                entry["context"] = turn.get("context") or {}
                entry["tools"] = turn.get("tools") or {}
                entry["model"] = turn.get("model") or {}
                entry["tokens"] = turn.get("tokens") or {}
                entry["visibility"] = turn.get("visibility") or ""
            items.append(entry)

        return {
            "schema": "gait.context.v0",
            "branch": branch,
            "memory_id": self.read_memory_ref(branch),
            "pinned_items": len(items),
            "items": items,
        }

    def iter_turns_from_head(
        self,
        *,
        start_commit: Optional[str] = None,
        limit_turns: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Walk commits backward from start_commit (default HEAD) following first-parent only,
        collect up to limit_turns turns, and return them oldest->newest.
        """
        cid = start_commit or self.head_commit_id()
        if not cid:
            return []
    
        turns_newest_first: List[Dict[str, Any]] = []
        seen_commits = set()
    
        while cid and cid not in seen_commits and len(turns_newest_first) < limit_turns:
            seen_commits.add(cid)
            c = self.get_commit(cid)
    
            for tid in (c.get("turn_ids") or []):
                turns_newest_first.append(self.get_turn(tid))
                if len(turns_newest_first) >= limit_turns:
                    break
                
            parents = c.get("parents") or []
            cid = parents[0] if parents else ""
    
        turns_newest_first.reverse()
        return turns_newest_first

    # ----------------------------
    # Branch ops
    # ----------------------------

    def create_branch(
        self,
        name: str,
        from_commit: Optional[str] = None,
        *,
        inherit_memory: bool = True,
    ) -> None:
        path = self.refs_dir / name
        if path.exists():
            raise FileExistsError(f"Branch already exists: {name}")

        commit = from_commit if from_commit is not None else self.head_commit_id()
        path.write_text((commit or "") + "\n", encoding="utf-8")

        if inherit_memory:
            src_branch = self.current_branch()
            src_mem = self.read_memory_ref(src_branch)
            self.write_memory_ref(src_mem, name)
        else:
            # Ensure branch has its own empty manifest ref
            self.read_memory_ref(name)

    def checkout(self, name: str) -> None:
        path = self.refs_dir / name
        if not path.exists():
            raise FileNotFoundError(f"Branch does not exist: {name}")
        self.head_file.write_text(f"ref: refs/heads/{name}\n", encoding="utf-8")


    def fast_forward_branch(self, branch: str, new_head: str) -> str:
        """
        Fast-forward branch to new_head if possible.
        Returns the resolved new head.
        """
        from .objects import resolve_prefix
    
        if not new_head:
            raise ValueError("Cannot fast-forward to empty commit id.")
    
        new_full = resolve_prefix(self.objects_dir, new_head)
        cur = self.read_ref(branch).strip()
    
        # if branch empty, just set it
        if not cur:
            self.write_ref(branch, new_full)
            return new_full
    
        cur_full = resolve_prefix(self.objects_dir, cur)
    
        if cur_full == new_full:
            return new_full
    
        if not self.is_ancestor(cur_full, new_full):
            raise ValueError(f"Non fast-forward: {branch} would move from {cur_full[:8]} to {new_full[:8]}")
    
        self.write_ref(branch, new_full)
        return new_full

    # ----------------------------
    # Reset / revert helpers
    # ----------------------------

    def reset_branch(self, commit_id: str) -> str:
        """
        Move current branch ref to commit_id (history rewind).
        Returns resolved full commit id.
        """
        branch = self.current_branch()
        _ = self.get_commit(commit_id)  # validates existence/prefix
        from .objects import resolve_prefix
        resolved = resolve_prefix(self.objects_dir, commit_id)
        self.write_ref(branch, resolved)
        return resolved

    def is_ancestor(self, maybe_ancestor: str, commit_id: str) -> bool:
        """
        True if maybe_ancestor is reachable from commit_id by walking parents.
        Prefixes allowed.
        """
        from .objects import resolve_prefix
        anc = resolve_prefix(self.objects_dir, maybe_ancestor)
        cur = resolve_prefix(self.objects_dir, commit_id)

        stack = [cur]
        seen = set()
        while stack:
            cid = stack.pop()
            if cid in seen:
                continue
            seen.add(cid)
            if cid == anc:
                return True
            c = self.get_commit(cid)
            for p in (c.get("parents") or []):
                if p and p not in seen:
                    stack.append(p)
        return False

    def reset_memory_to_commit(self, branch: str, commit_id: str) -> str:
        """
        Rewind branch memory to the most recent reflog entry whose head_commit
        is an ancestor of commit_id.

        Fallback (if no reflog match): prune current manifest to only pins whose
        commit_id is an ancestor of commit_id.
        """
        # current memory
        current_mem = self.read_memory_ref(branch)

        # --- try reflog first ---
        if self.memory_log.exists():
            lines = self.memory_log.read_text(encoding="utf-8").splitlines()
            for raw in reversed(lines):
                if not raw.strip():
                    continue
                e = json.loads(raw)
                if e.get("branch") != branch:
                    continue

                head_at_change = e.get("head_commit") or ""
                new_mem = e.get("new_mem") or ""
                if not head_at_change or not new_mem:
                    continue

                if self.is_ancestor(head_at_change, commit_id):
                    self.write_memory_ref(new_mem, branch)
                    return new_mem

        # --- fallback: prune manifest by reachability ---
        manifest = self.get_memory(branch)
        kept: list[MemoryItem] = []
        dropped = 0

        for it in manifest.items:
            # keep pins whose commit is reachable from the target commit
            if it.commit_id and self.is_ancestor(it.commit_id, commit_id):
                kept.append(it)
            else:
                dropped += 1

        new_manifest = MemoryManifest(schema="gait.memory.v0", created_at=now_iso(), items=kept)
        new_mem = self.set_memory(new_manifest, branch)

        # optional: log this prune so future rewinds get better
        self.append_memory_log(
            branch=branch,
            old_mem=current_mem,
            new_mem=new_mem,
            reason="revert-memory-prune",
            note=f"to={commit_id}",
            meta={"to_commit": commit_id, "dropped": dropped, "kept": len(kept)},
            head_commit=commit_id,
        )

        return new_mem

    # ----------------------------
    # Memory mutate ops (pin/unpin)
    # ----------------------------

    def pin_commit(self, commit_id: str, *, note: str = "", branch: Optional[str] = None) -> str:
        b = branch or self.current_branch()
        commit = self.get_commit(commit_id)
        turn_ids = commit.get("turn_ids") or []
        if not turn_ids:
            raise ValueError("Cannot pin: commit has no turns (merge commit?).")

        old_mem = self.read_memory_ref(b)

        manifest = self.get_memory(b)
        new_items = list(manifest.items)

        for tid in turn_ids:
            new_items.append(
                MemoryItem(
                    pinned_at=now_iso(),
                    commit_id=commit_id,
                    turn_id=tid,
                    note=note,
                )
            )

        new_manifest = MemoryManifest(schema="gait.memory.v0", created_at=now_iso(), items=new_items)
        new_mem = self.set_memory(new_manifest, b)

        # reflog
        self.append_memory_log(
            branch=b,
            old_mem=old_mem,
            new_mem=new_mem,
            reason="pin",
            note=note,
            meta={"commit_id": commit_id, "turns_added": len(turn_ids)},
            head_commit=self.read_ref(b),  # record HEAD at time of pin
        )
        return new_mem

    def unpin_index(self, index: int, branch: Optional[str] = None) -> str:
        b = branch or self.current_branch()
        manifest = self.get_memory(b)
        if index < 1 or index > len(manifest.items):
            raise IndexError(f"Pin index out of range: {index}")

        old_mem = self.read_memory_ref(b)

        new_items = [it for i, it in enumerate(manifest.items, start=1) if i != index]
        new_manifest = MemoryManifest(schema="gait.memory.v0", created_at=now_iso(), items=new_items)
        new_mem = self.set_memory(new_manifest, b)

        self.append_memory_log(
            branch=b,
            old_mem=old_mem,
            new_mem=new_mem,
            reason="unpin",
            note=f"index={index}",
            meta={"index": index},
            head_commit=self.read_ref(b),
        )
        return new_mem

    def budget_for_memory(self, branch: Optional[str] = None) -> Dict[str, Any]:
        b = branch or self.current_branch()
        manifest = self.get_memory(b)
        total_in = 0
        total_out = 0
        unknown = 0

        for it in manifest.items:
            t = self.get_turn(it.turn_id)
            tokens = t.get("tokens") or {}
            in_t = tokens.get("input_total")
            out_t = tokens.get("output_total")
            if isinstance(in_t, int):
                total_in += in_t
            else:
                unknown += 1
            if isinstance(out_t, int):
                total_out += out_t
            else:
                unknown += 1

        return {
            "branch": b,
            "pinned_items": len(manifest.items),
            "tokens_input_total": total_in,
            "tokens_output_total": total_out,
            "unknown_token_fields": unknown,
        }

    def rewind_memory_to_head(self, *, branch: Optional[str] = None, head_commit: str) -> tuple[str, str]:
        b = branch or self.current_branch()
        old_mem = self.read_memory_ref(b)
        new_mem = self.reset_memory_to_commit(b, head_commit)
        return old_mem, new_mem

    # ----------------------------
    # Turns + commits
    # ----------------------------

    def append_turn_log(self, turn_id: str, commit_id: str) -> None:
        entry = {"turn_id": turn_id, "commit_id": commit_id}
        with self.turns_log.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def record_turn(
        self,
        turn: Turn,
        *,
        message: str = "",
        kind: str = "auto",
        meta: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, str]:
        turn_id = store_object(self.objects_dir, turn.to_dict())

        branch = self.current_branch()
        parent = self.head_commit_id()
        parents: List[str] = [parent] if parent else []

        commit = Commit.v0(
            parents=parents,
            turn_ids=[turn_id],
            branch=branch,
            snapshot_id=None,
            kind=kind,
            message=message,
            meta=meta or {},
        )
        commit_id = store_object(self.objects_dir, commit.to_dict())

        self.write_ref(branch, commit_id)
        self.append_turn_log(turn_id, commit_id)
        return turn_id, commit_id

    def merge(self, source_branch: str, *, message: str = "", with_memory: bool = False) -> str:
        target_branch = self.current_branch()
        target_head = self.read_ref(target_branch)
        source_head = self.read_ref(source_branch)

        if not source_head:
            raise ValueError(f"Source branch {source_branch} has no commits to merge.")

        merge_meta: Dict[str, Any] = {"source_branch": source_branch, "source_head": source_head}

        # fast-forward if target is empty
        if not target_head:
            self.write_ref(target_branch, source_head)
            if with_memory:
                old_mem = self.read_memory_ref(target_branch)
                src_mem = self.read_memory_ref(source_branch)
                self.write_memory_ref(src_mem, target_branch)

                self.append_memory_log(
                    branch=target_branch,
                    old_mem=old_mem,
                    new_mem=src_mem,
                    reason="merge-memory-ff",
                    note=f"source={source_branch}",
                    meta={"source_branch": source_branch, "source_mem": src_mem},
                    head_commit=source_head,  # after FF, head becomes source_head
                )
            return source_head

        # --- memory merge ---
        if with_memory:
            target_mem_id_before = self.read_memory_ref(target_branch)
            source_mem_id = self.read_memory_ref(source_branch)

            target_manifest = self.get_memory(target_branch)
            source_manifest = self.get_memory(source_branch)

            seen_turns = {it.turn_id for it in target_manifest.items}
            merged_items = list(target_manifest.items)

            added = 0
            deduped = 0
            for it in source_manifest.items:
                if it.turn_id in seen_turns:
                    deduped += 1
                    continue
                merged_items.append(it)
                seen_turns.add(it.turn_id)
                added += 1

            merged_manifest = MemoryManifest(schema="gait.memory.v0", created_at=now_iso(), items=merged_items)
            target_mem_id_after = self.set_memory(merged_manifest, target_branch)

            self.append_memory_log(
                branch=target_branch,
                old_mem=target_mem_id_before,
                new_mem=target_mem_id_after,
                reason="merge-memory",
                note=f"source={source_branch}",
                meta={
                    "source_branch": source_branch,
                    "source_mem": source_mem_id,
                    "added": added,
                    "deduped": deduped,
                    "total": len(merged_items),
                },
                head_commit=target_head,  # memory merge happened while HEAD was target_head
            )

            merge_meta.update(
                {
                    "memory_merged": True,
                    "memory_target_before": target_mem_id_before,
                    "memory_source": source_mem_id,
                    "memory_target_after": target_mem_id_after,
                    "memory_added": added,
                    "memory_deduped": deduped,
                    "memory_total": len(merged_items),
                }
            )
        else:
            merge_meta["memory_merged"] = False

        # create merge commit
        commit = Commit.v0(
            parents=[target_head, source_head],
            turn_ids=[],
            branch=target_branch,
            snapshot_id=None,
            kind="merge",
            message=message or f"merge {source_branch} -> {target_branch}",
            meta=merge_meta,
        )
        merge_commit_id = store_object(self.objects_dir, commit.to_dict())
        self.write_ref(target_branch, merge_commit_id)
        return merge_commit_id

    # ----------------------------
    # Read helpers
    # ----------------------------

    def get_commit(self, commit_id: str) -> Dict[str, Any]:
        return load_object(self.objects_dir, commit_id)

    def get_turn(self, turn_id: str) -> Dict[str, Any]:
        return load_object(self.objects_dir, turn_id)

