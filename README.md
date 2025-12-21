# gait
An open source version and source control system, inspired by Git, for Artificial Intelligence Agents

Git-Like Version Control for AI Conversations

GAIT is an open-source, Git-inspired version control system for AI conversations, prompts, and long-lived memory.

It treats AI context as versioned infrastructure, not disposable chat logs.

Think of GAIT as Git for reasoning, not files.

Why GAIT Exists

AI workflows don’t behave like filesystems:

Conversations evolve over time

Some context should persist, some should not

Bad turns must be reversible

Experiments should not pollute production memory

Prompt changes need safe branching and rollback

Traditional chat tools collapse history, memory, and state into one fragile stream.

GAIT separates them — while keeping everything inspectable, versioned, and reversible.

What GAIT Lets You Do

Record user ↔ assistant turns as immutable objects

Commit conversation state to branches

Pin important turns into explicit, long-lived memory

Resume conversations safely (or start fresh automatically)

Branch, merge, and experiment without losing context

Rewind history and memory independently

Chat interactively with local LLMs while versioning every turn

Core Concepts
Turns

A turn is a single user + assistant interaction.

User:      "What is GAIT?"
Assistant: "GAIT is Git for AI conversations."


Turns are immutable

Content-addressed

Stored once, referenced everywhere

Commits

A commit references one or more turns and has parents, metadata, and a branch.

Normal commits contain turns

Merge commits contain no turns

Commits form a DAG (just like Git)

This allows safe history traversal, branching, and merges.

Memory (HEAD+ Memory)

Memory is explicitly pinned context that survives across turns.

Key properties:

Memory is opt-in

Only pinned turns enter memory

Memory is versioned independently from commits

Memory has its own reflog

This prevents accidental context bloat and hallucination drift.

Repository Layout

GAIT stores everything in a .gait/ directory:

.gait/
├── HEAD
├── objects/          # content-addressed objects (turns, commits, memory)
├── refs/
│   ├── heads/        # branches
│   └── memory/       # branch memory refs
├── turns.jsonl       # turn → commit log
└── memory.jsonl      # memory reflog


No magic. Everything is inspectable.

Installation (Dev / Editable)
python -m venv GAITING
source GAITING/bin/activate
pip install -e .


This installs the gait CLI into your virtual environment.

(PyPI packaging coming next.)

Quick Start
Initialize a repo
gait init

Record a turn
gait record-turn \
  --user "What is GAIT?" \
  --assistant "GAIT is Git for AI conversations."


This:

Stores the turn

Creates a commit

Advances HEAD

Pin important context into memory
gait pin --last --note "baseline definition"


Pinned turns now become part of HEAD+ memory.

gait memory

View history
gait log
gait show HEAD

Interactive Chat (Local LLMs)

GAIT includes an interactive chat mode that records every turn automatically.

gait chat

Supported local providers

GAIT auto-detects local LLMs in this order:

Ollama — 127.0.0.1:11434

Foundry Local — 127.0.0.1:63545

LM Studio — 127.0.0.1:1234

No flags required in the common case.

Defaults & safety

If history exists → GAIT resumes automatically

If HEAD is empty → GAIT starts fresh (no crash)

Memory is injected only if pinned

Resume can be disabled with --no-resume

Environment overrides
export GAIT_PROVIDER=openai_compat
export GAIT_BASE_URL=http://127.0.0.1:1234
export GAIT_DEFAULT_MODEL=gemma-3-4b

Branching & Experiments

Create and switch branches directly from the CLI:

gait branch experiment
gait checkout experiment


Branches:

Inherit commit history

Optionally inherit memory (--no-inherit-memory)

Are perfect for prompt and reasoning experiments

Inside gait chat, you can also:

/branches
/branch new-idea
/checkout new-idea


(No context loss.)

Merging
gait merge experiment


Optional memory merge:

gait merge experiment --with-memory


Memory merges:

Deduplicate pinned turns

Preserve provenance

Are logged in the memory reflog

Revert vs Reset (Important)
gait revert — safe undo
gait revert
gait revert --also-memory


Moves HEAD to the parent commit

Optionally rewinds memory correctly

Best for interactive usage

gait reset — power tool
gait reset <commit>
gait reset --hard


reset → move HEAD only

reset --hard → move HEAD + memory

Best for timeline surgery and cleanup.

Memory Reflog (The Secret Sauce)

Every memory mutation is logged with:

Timestamp

Branch

HEAD commit at the time

Old memory → new memory

Reason (pin, unpin, merge, revert, reset)

This makes memory auditable, reversible, and safe.

Context Export (Agent-Ready)
gait context --json


Produces a structured context bundle:

{
  "schema": "gait.context.v0",
  "branch": "main",
  "memory_id": "...",
  "pinned_items": 2,
  "items": [...]
}


Designed for:

LLM prompts

Agent frameworks

MCP (future)

What GAIT Is Not (Yet)

❌ File version control

❌ Automatic memory

❌ Hosted SaaS

❌ MCP server (coming)

❌ Remote sync (gaithub in progress)

GAIT is intentionally small, explicit, and correct.

Philosophy

History is cheap.
Memory is intentional.
Reversibility is non-negotiable.

GAIT treats AI context like production infrastructure — not chat logs.

Status

Version: 0.0.1

State: Core model stable, active development