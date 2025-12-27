# GAIT (Git for AI Turns)

Git-Like Version Control for AI Conversations, Prompts, and Long-Lived Memory.

GAIT is a specialized version control system built to solve the "poisoned context" problem in LLM workflows. In standard AI chat interfaces, conversations are linear and fragile; one bad turn or a significant hallucination permanently alters the model's "window," often requiring you to delete the chat and start over.

GAIT treats AI context as versioned infrastructure. It allows you to commit conversation states, branch different reasoning paths, pin specific memories, and sync your "reasoning repos" across machines.

## 1. Why GAIT? 

The Problem with Linear Chat

Traditional AI workflows suffer from three major issues:

* Context Pollution: If an LLM gives a wrong answer and you continue the chat, the model is now "primed" by its own mistake.

* Memory Drift: As conversations get long, important early instructions or "ground truths" get pushed out of the model's sliding window.

* The "What-If" Wall: If you want to see how a different prompt or model would have handled a question 10 turns ago, you usually have to copy-paste the whole history into a new window.

GAIT fixes this by introducing the Commit/Branch/Merge workflow to AI reasoning.

## 2. Core Concepts

### The Turn (The "Blob")

A Turn is the atomic unit of GAIT. It contains the user's prompt and the assistant's response. Like a Git blob, it is content-addressed (hashed); if the text changes, the ID changes.

### The Commit

A Commit wraps one or more turns with metadata: the model used, the provider, the timestamp, and—most importantly—a pointer to the parent commit. This creates a Directed Acyclic Graph (DAG) of your conversation.

### HEAD+ Memory (The "Secret Sauce")

This is GAIT's most powerful feature. Standard LLMs have "short-term memory" (the sliding window). GAIT adds HEAD+ Memory:

* Intentional: You explicitly /pin turns that contain "Golden Rules" or vital project info.

* Persistent: Pinned turns are injected into the System Prompt for every future turn on that branch, regardless of how long the history gets.

* Versioned: Memory has its own Reflog. If you revert a commit, GAIT can automatically rewind your memory to exactly how it looked at that moment.

## 3. Installation & Quick Start

## Requirements

Python 3.10+

A local LLM framework running: Ollama, LM Studio, or Microsoft Foundry Local.

## Installation

``` Bash

git clone https://github.com/automateyournetwork/gait.git
cd gait
pip install gait-ai

```

## Initialize a Repository

Navigate to your project folder and run:

``` Bash
gait init
```

This creates a .gait/ directory. You are now ready to version your thoughts.

## 4. The Interactive Chat Workflow

The primary way to use GAIT is through the gait chat command. It feels like a standard terminal chat but works like a version-controlled environment.

```Bash
gait chat --model llama3.1
```

## You can use CLOUD providers as well:

# Use OpenAI ChatGPT (cloud)

export GAIT_PROVIDER=chatgpt
export OPENAI_API_KEY="sk-..."

gait chat --model gpt-4.1-mini

```Bash

### Common Commands inside gait chat

Commands and Actions:

/undo

The Safety Net. Erases the last Q&A turn and moves the branch back to the previous state.

/pin

Freeze Context. Marks the current turn as "Memory." It will now stay in the model's context forever.

/branch <name>

Split Reality. Create a new timeline to explore a different idea without affecting your main chat.

/checkout <name>

Time Travel. Instantly switch between different conversation timelines.

/merge <branch> [--with-memory]

Merge another branch into the current one. Use --with-memory to also bring over pinned turns.

/fetch 

Sync with Remote. Pull down the latest commits and memory from your GaitHub remote.

/pull <owner> <repo> [--path <dir>]

Fast-forward Clone. Grab a reasoning repository from GaitHub and set it up locally.

/push --owner <owner> --repo <repo>

Upload your current branch and memory to GaitHub for remote storage and sharing.

/model <name>

Swap Brains. Switch from a 7B model to a 70B model mid-conversation.

/memory

Audit. View a JSON manifest of everything currently pinned to your branch.



## 5. Advanced Usage Scenarios

### Scenario A: Recovering from Hallucinations

You've been chatting for an hour. You ask a complex coding question, and the AI provides a 200-line script that is completely wrong.

The Old Way: You try to tell the AI it's wrong, but it gets confused and keeps referencing the bad code.

The GAIT Way: Type /undo. The bad code is gone from the history. The model's "window" is restored to the moment before the error occurred.

### Scenario B: Model Comparison

You want to see if Gemma-2 or Llama-3 handles a specific logic puzzle better.Start on main with Llama-3 and ask the question.

/branch gemma-test

/checkout gemma-test

/model gemma-2-9b

Ask the same question. Now you have two distinct commits you can compare using gait log.

### Scenario C: Knowledge Merging

You spent a branch researching "AWS Security Patterns" and pinned the best answers. Now you want those security rules in your "Development" branch.

``` Bash

gait checkout development
gait merge research-branch --with-memory

```

GAIT merges the histories and brings over all the pinned memory turns, deduplicating them so your context remains clean.

## 6. Remote Syncing with GaitHub

GAIT is not limited to your local machine. By using a GaitHub remote, you can treat AI reasoning as a shared asset.

Setting up a Remote

```Bash

gait remote add origin https://gaithub-960937205198.us-central1.run.app/

```

Pushing & Pulling

```Bash

# Push your reasoning to the cloud
# (Requires GAITHUB_TOKEN environment variable)

gait push origin --owner john --repo architecture-decisions

# Resume that conversation on your laptop
gait clone https://gaithub.your-server.com --owner john --repo architecture-decisions --path ./decisions
```

## 7. Configuration & Environment Variables

GAIT is designed to be "zero-config," but you can customize it heavily:

Variables and Descriptions

GAIT_PROVIDER

LLM backend to use.

Valid values:

ollama

openai_compat (Foundry Local, LM Studio)

chatgpt (OpenAI cloud)

GAIT_DEFAULT_MODEL

Default model used if --model is not specified.

GAIT_BASE_URL

Base URL for OpenAI-compatible APIs

(e.g. http://127.0.0.1:1234 or https://api.openai.com/v1)

OPENAI_API_KEY

Required when using GAIT_PROVIDER=chatgpt.

GAITHUB_TOKEN

Authentication token for pushing to a GaitHub remote.

## 8. Repository Layout

GAIT is transparent. You can open any file in .gait/ to see exactly what is happening:

.gait/objects/: 

The content-addressed database. Every turn, commit, and memory manifest is stored here as a JSON file named by its SHA-256 hash.

.gait/refs/: 

Simple text files containing hashes. refs/heads/main tells GAIT which commit is the "top" of the main branch.

.gait/memory.jsonl: 

The Memory Reflog. A line-by-line audit trail of every time you pinned or unpinned an item.

.gait/turns.jsonl: 

A mapping of Turn IDs to Commit IDs for easy lookup.

## 9. Philosophy

History is cheap. Storing text turns costs almost nothing.Memory is expensive. Large contexts slow down models and cause "Lost in the Middle" syndrome.

GAIT empowers the user to record everything but curate specifically. 

By treating your conversations like code, you move from "chatting with a bot" to "architecting a knowledge base."
