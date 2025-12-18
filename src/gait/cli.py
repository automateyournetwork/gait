from __future__ import annotations

import argparse
import json
from pathlib import Path

from .repo import GaitRepo
from .schema import Turn
from .objects import short_oid
from .log import walk_commits


# ----------------------------
# Commands
# ----------------------------

def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    repo = GaitRepo(root=root)
    repo.init()
    print(f"Initialized GAIT repo in {repo.gait_dir}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    branch = repo.current_branch()
    head = repo.head_commit_id()
    print(f"root:   {repo.root}")
    print(f"branch: {branch}")
    print(f"HEAD:   {head or '(empty)'}")
    return 0


def cmd_branch(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    repo.create_branch(
        args.name,
        from_commit=args.from_commit,
        inherit_memory=(not args.no_inherit_memory),
    )
    print(f"Created branch {args.name}")
    return 0


def cmd_checkout(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    repo.checkout(args.name)
    print(f"Switched to branch {args.name}")
    return 0


def cmd_revert(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    branch = repo.current_branch()
    head = repo.head_commit_id()
    if not head:
        raise ValueError("Nothing to revert (branch has no commits).")

    # target commit
    if args.commit is None:
        c = repo.get_commit(head)
        parents = c.get("parents") or []
        if not parents:
            repo.write_ref(branch, "")
            print(f"reverted: {branch} is now empty")
            return 0
        target = parents[0]
    else:
        target = args.commit

    resolved = repo.reset_branch(target)
    print(f"reverted: {branch} -> {resolved}")
    print(f"HEAD:   {repo.head_commit_id()}")

    if args.also_memory:
        old_mem = repo.read_memory_ref(branch)
        new_mem = repo.reset_memory_to_commit(branch, repo.head_commit_id())
        print(f"memory: {old_mem} -> {new_mem}")

    return 0


def cmd_record_turn(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()

    context = json.loads(args.context) if args.context else {}
    tools = json.loads(args.tools) if args.tools else {}
    model = json.loads(args.model) if args.model else {}

    turn = Turn.v0(
        user_text=args.user,
        assistant_text=args.assistant,
        context=context,
        tools=tools,
        model=model,
        visibility=args.visibility,
    )
    turn_id, commit_id = repo.record_turn(turn, message=args.message or "")
    print(f"turn:   {turn_id}")
    print(f"commit: {commit_id}")
    print(f"branch: {repo.current_branch()} -> {commit_id}")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    for c in walk_commits(repo, limit=args.limit):
        cid = c["_id"]
        msg = c.get("message") or ""
        kind = c.get("kind") or ""
        created = c.get("created_at") or ""
        turn_ids = c.get("turn_ids") or []

        parents = c.get("parents") or []
        p = ",".join(short_oid(x) for x in parents) if parents else "-"
        merge_flag = " (merge)" if len(parents) > 1 else ""

        print(f"{short_oid(cid)}{merge_flag}  {created}  {kind}  p=[{p}]  turns={len(turn_ids)}  {msg}")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    commit_id = args.commit or repo.head_commit_id()

    commit = repo.get_commit(commit_id)
    print(f"commit: {commit_id}")
    print(f"branch: {commit.get('branch')}")
    print(f"kind:   {commit.get('kind')}")
    print("-" * 60)

    turn_ids = commit.get("turn_ids") or []
    if not turn_ids:
        print("(no turns attached to this commit)")
        return 0

    for i, tid in enumerate(turn_ids, 1):
        turn = repo.get_turn(tid)
        user = (turn.get("user") or {}).get("text", "")
        assistant = (turn.get("assistant") or {}).get("text", "")

        print(f"[Turn {i}]")
        print("User:")
        print(user)
        print("\nAssistant:")
        print(assistant)
        print("-" * 60)

    return 0


def cmd_merge(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    merge_id = repo.merge(
        args.source,
        message=args.message or "",
        with_memory=args.with_memory,
    )
    print(f"merged: {args.source} -> {repo.current_branch()}")
    print(f"HEAD:   {merge_id}")
    if args.with_memory:
        print(f"memory: {repo.read_memory_ref(repo.current_branch())}")
    return 0


def cmd_pin(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()

    def find_last_turn_commit() -> str:
        head = repo.head_commit_id()
        if not head:
            raise ValueError("No HEAD commit to pin.")
        cid = head
        seen = set()
        while cid and cid not in seen:
            seen.add(cid)
            c = repo.get_commit(cid)
            if (c.get("turn_ids") or []):
                return cid
            parents = c.get("parents") or []
            cid = parents[0] if parents else ""
        raise ValueError("No commit with turns found in history to pin.")

    if args.last:
        commit_id = find_last_turn_commit()
    else:
        if not args.commit:
            raise ValueError("Provide a commit id/prefix or use --last.")
        commit_id = args.commit

    mem_id = repo.pin_commit(commit_id, note=args.note or "")
    print(f"pinned commit {commit_id} into memory")
    print(f"memory: {mem_id}")
    return 0


def cmd_memory(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    manifest = repo.get_memory()
    print(f"branch: {repo.current_branch()}")
    print(f"pinned: {len(manifest.items)}")
    print("-" * 60)
    for i, it in enumerate(manifest.items, start=1):
        print(f"{i}. turn={short_oid(it.turn_id)} commit={short_oid(it.commit_id)} note={it.note}")
    return 0


def cmd_unpin(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    manifest = repo.get_memory()
    if not manifest.items:
        print("nothing to unpin (memory is empty)")
        return 0

    mem_id = repo.unpin_index(args.index)
    print(f"unpinned #{args.index}")
    print(f"memory: {mem_id}")
    return 0


def cmd_budget(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    b = repo.budget_for_memory()
    print(f"branch: {b['branch']}")
    print(f"pinned_items: {b['pinned_items']}")
    print(f"tokens_input_total: {b['tokens_input_total']}")
    print(f"tokens_output_total: {b['tokens_output_total']}")
    print(f"unknown_token_fields: {b['unknown_token_fields']}")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    repo = GaitRepo.discover()
    bundle = repo.build_context_bundle(full=args.full)

    if args.json:
        print(json.dumps(bundle, ensure_ascii=False, indent=2))
        return 0

    print(f"branch: {bundle['branch']}")
    print(f"memory: {bundle['memory_id']}")
    print(f"pinned: {bundle['pinned_items']}")
    print("-" * 60)

    if not bundle["items"]:
        print("(no pinned memory)")
        return 0

    for it in bundle["items"]:
        print(f"[PIN {it['index']}] note={it.get('note','')}")
        print("User:")
        print(it.get("user_text", ""))
        print("\nAssistant:")
        print(it.get("assistant_text", ""))
        print("-" * 60)

    return 0


# ----------------------------
# Parser
# ----------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gait")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="Initialize a GAIT repo in PATH (default: .)")
    s.add_argument("path", nargs="?", default=".")
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("status", help="Show current repo status")
    s.set_defaults(func=cmd_status)

    s = sub.add_parser("branch", help="Create a branch")
    s.add_argument("name")
    s.add_argument("--from-commit", default=None)
    s.add_argument("--no-inherit-memory", action="store_true", help="Do not inherit HEAD+ memory from current branch")
    s.set_defaults(func=cmd_branch)

    s = sub.add_parser("checkout", help="Switch branches")
    s.add_argument("name")
    s.set_defaults(func=cmd_checkout)

    s = sub.add_parser("record-turn", help="Record a user+assistant turn and auto-commit")
    s.add_argument("--user", required=True)
    s.add_argument("--assistant", required=True)
    s.add_argument("--message", default="")
    s.add_argument("--visibility", default="private", choices=["private", "shareable"])
    s.add_argument("--context", default="", help="JSON string")
    s.add_argument("--tools", default="", help="JSON string")
    s.add_argument("--model", default="", help="JSON string")
    s.set_defaults(func=cmd_record_turn)

    s = sub.add_parser("log", help="Show commit log")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_log)

    s = sub.add_parser("show", help="Show prompts and responses for a commit (default: HEAD)")
    s.add_argument("commit", nargs="?", default=None)
    s.set_defaults(func=cmd_show)

    s = sub.add_parser("pin", help="Pin a commit's turns into branch HEAD+ memory")
    s.add_argument("commit", nargs="?", default=None, help="Commit id/prefix (required unless --last)")
    s.add_argument("--last", action="store_true", help="Pin last commit with turns (skips merges)")
    s.add_argument("--note", default="", help="Optional note for why this was pinned")
    s.set_defaults(func=cmd_pin)

    s = sub.add_parser("memory", help="List pinned HEAD+ memory items for this branch")
    s.set_defaults(func=cmd_memory)

    s = sub.add_parser("unpin", help="Remove a pinned memory item by index (use `gait memory` to see indices)")
    s.add_argument("index", type=int)
    s.set_defaults(func=cmd_unpin)

    s = sub.add_parser("budget", help="Show token budget summary for pinned HEAD+ memory")
    s.set_defaults(func=cmd_budget)

    s = sub.add_parser("merge", help="Merge SOURCE branch into the current branch (creates merge commit)")
    s.add_argument("source")
    s.add_argument("--message", default="")
    s.add_argument("--with-memory", action="store_true", help="Also merge HEAD+ memory (pinned items)")
    s.set_defaults(func=cmd_merge)

    s = sub.add_parser("context", help="Print the branch HEAD+ context pack (from pinned memory)")
    s.add_argument("--json", action="store_true", help="Output JSON (agent/MCP-friendly)")
    s.add_argument("--full", action="store_true", help="Include raw context/tools/model/tokens per turn")
    s.set_defaults(func=cmd_context)

    s = sub.add_parser("revert", help="Rewind current branch HEAD to a prior commit (default: parent of HEAD)")
    s.add_argument("commit", nargs="?", default=None, help="Commit id/prefix (default: first parent of HEAD)")
    s.add_argument("--also-memory", action="store_true", help="Also rewind HEAD+ memory via memory reflog")
    s.set_defaults(func=cmd_revert)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)
