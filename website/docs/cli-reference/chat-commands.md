# Interactive Chat Commands 🎮

Complete reference for all commands available inside `gait chat` interactive sessions.

## Basic Commands

### Regular Text (No Command)

Just type normally to chat with the AI!

```
> Hello, how are you?
```

No slash, no special syntax - just conversation. 💬

---

## Memory Commands

### `/pin` - Pin to Memory 📌

Pin the last turn to permanent memory.

**Usage:**
```
/pin [note]
```

**Examples:**
```
> You are a Python expert. Use type hints in all code examples.
> /pin

> This is an important rule!
> /pin Important coding guideline
```

**What it does:**
- Adds last turn to MemoryManifest
- Turn will be injected into system prompt for all future conversations
- Persists across chat sessions

---

### `/unpin` - Remove from Memory 🗑️

Remove an item from pinned memory.

**Usage:**
```
/unpin INDEX
```

**Example:**
```
> /memory
{
  "items": [
    {"note": "Rule 1", ...},  # Index 0
    {"note": "Rule 2", ...}   # Index 1
  ]
}

> /unpin 1
✅ Unpinned memory item 1
```

---

### `/memory` - View Pinned Memory 🧠

Show all currently pinned items.

**Usage:**
```
/memory
```

**Output:**
```json
{
  "schema": "gait.memory.v0",
  "items": [
    {
      "turn_id": "abc123...",
      "commit_id": "def456...",
      "note": "Python expert instructions",
      "pinned_at": "2026-01-07T10:30:45Z"
    }
  ]
}
```

---

## History Commands

### `/undo` or `/revert` - Undo Last Turn ⏪

Delete the last question and answer, reverting to previous state.

**Usage:**
```
/undo
```

**Example:**
```
> What's 2+2?
AI: 5  (Wrong!)

> /undo
✅ Reverted to previous commit

> What's 2+2?
AI: 4  (Correct!)
```

**What it does:**
- Moves HEAD back to parent commit
- Last turn is "forgotten" (still in objects, but not in history)
- If turn was pinned, it's automatically unpinned

---

### `/log` - View Conversation History 📜

Show recent conversation history.

**Usage:**
```
/log [N]
```

**Examples:**
```
# Show all history
/log

# Show last 5 turns
/log 5
```

---

## Branch Commands

### `/branch` - Create New Branch 🌿

Create a new branch from the current HEAD.

**Usage:**
```
/branch NAME
```

**Example:**
```
> /branch experiment
✅ Created branch 'experiment'
✅ Switched to branch 'experiment'
```

**What it does:**
- Creates new branch pointing to current commit
- Copies current memory to new branch
- Automatically checks out new branch

---

### `/checkout` - Switch Branches 🔄

Switch to a different branch.

**Usage:**
```
/checkout BRANCH
```

**Example:**
```
> /checkout main
✅ Switched to branch 'main'
```

**What it does:**
- Updates HEAD to point to specified branch
- Rebuilds conversation context with that branch's memory
- Loads recent history from that branch

---

### `/merge` - Merge Branches 🔀

Merge another branch into the current one.

**Usage:**
```
/merge SOURCE [--with-memory]
```

**Examples:**
```
# Merge commits only
> /merge experiment
✅ Merged branch 'experiment' into 'main'

# Merge commits and memory
> /merge experiment --with-memory
✅ Merged branch 'experiment' (including memory) into 'main'
```

**What it does:**
- Creates merge commit with two parents
- Optionally merges memory (deduplicates pinned items)
- Combines conversation histories

---

## Model Commands

### `/models` - List Available Models 📋

Show all models available from current provider.

**Usage:**
```
/models
```

**Output:**
```
Available models for provider 'ollama':
  - llama3.1
  - llama3.3
  - gemma2
  - qwen2.5
  - mistral
  - codellama
```

---

### `/model` - Switch Model 🧠

Change to a different model mid-conversation.

**Usage:**
```
/model NAME
```

**Example:**
```
> /model gemma2
✅ Switched to model 'gemma2'

> What's your name?
AI: I'm Gemma, a large language model...
```

**What it does:**
- Switches LLM model for future responses
- Rebuilds context (memory + recent history)
- Previous responses keep their original model metadata

---

### `/provider` - Switch Provider 🔌

Change to a different LLM provider.

**Usage:**
```
/provider NAME [MODEL]
```

**Examples:**
```
# Switch to ChatGPT
> /provider chatgpt gpt-4.1-mini
✅ Switched to provider 'chatgpt', model 'gpt-4.1-mini'

# Switch to local Ollama
> /provider ollama llama3.1
✅ Switched to provider 'ollama', model 'llama3.1'
```

**Supported providers:**
- `ollama` - Local Ollama
- `chatgpt` - OpenAI ChatGPT (requires `OPENAI_API_KEY`)
- `gemini` - Google Gemini (requires `GEMINI_API_KEY`)
- `anthropic` - Anthropic Claude (requires `ANTHROPIC_API_KEY`)
- `openai_compat` - OpenAI-compatible (Foundry, LM Studio)

---

## Advanced Commands

### `/squash` - Compress History 🗜️

Squash multiple commits into a summary.

**Usage:**
```
/squash [LAST] [MODE]
```

**Parameters:**
- `LAST`: Number of commits to squash (default: 10)
- `MODE`: `soft` (backup old HEAD) or `hard` (no backup, default: soft)

**Examples:**
```
# Squash last 10 commits
> /squash

# Squash last 5 commits
> /squash 5

# Squash without backup
> /squash 10 hard
```

**What it does:**
- Collects turns from last N commits
- Creates summary Turn (concatenates user/assistant text)
- Creates new commit with summary as only turn
- Moves branch pointer to new commit
- Optionally backs up old HEAD

**Use case:** Compress long conversations to save context window space.

---

## Remote Commands

### `/push` - Push to Remote ☁️

Upload current branch to GaitHub remote.

**Usage:**
```
/push --owner OWNER --repo REPO [--with-memory]
```

**Example:**
```
> /push --owner john --repo my-project --with-memory
✅ Pushed branch 'main' to john/my-project
```

**Requires:** `GAITHUB_TOKEN` environment variable

---

### `/pull` - Pull from Remote 📥

Download and merge changes from GaitHub remote.

**Usage:**
```
/pull --owner OWNER --repo REPO [--with-memory]
```

**Example:**
```
> /pull --owner john --repo my-project --with-memory
✅ Pulled branch 'main' from john/my-project
```

---

### `/fetch` - Fetch from Remote 🔄

Download changes without merging.

**Usage:**
```
/fetch --owner OWNER --repo REPO
```

**Example:**
```
> /fetch --owner john --repo my-project
✅ Fetched john/my-project
```

---

## Utility Commands

### `/exit` or `/quit` - Exit Chat 🚪

Leave the chat session.

**Usage:**
```
/exit
```

or

```
/quit
```

or

Press `Ctrl+C`

**What it does:**
- Saves all changes (automatic!)
- Closes the chat session
- Returns to shell

Everything is saved - you can resume anytime with `gait chat`!

---

## Command Cheat Sheet 📋

| Command | Shortcut | Description |
|---------|----------|-------------|
| `/pin` | - | Pin last turn to memory |
| `/unpin N` | - | Unpin memory item N |
| `/memory` | - | Show pinned memory |
| `/undo` | `/revert` | Undo last turn |
| `/log [N]` | - | Show history |
| `/branch NAME` | - | Create & switch to branch |
| `/checkout NAME` | - | Switch branch |
| `/merge SRC` | - | Merge branch |
| `/models` | - | List models |
| `/model NAME` | - | Switch model |
| `/provider NAME` | - | Switch provider |
| `/squash [N]` | - | Compress history |
| `/push` | - | Upload to remote |
| `/pull` | - | Download from remote |
| `/fetch` | - | Fetch from remote |
| `/exit` | `/quit`, `Ctrl+C` | Exit chat |

---

## Next Steps

- **[CLI Commands Reference](commands)** - Main `gait` commands
- **[Environment Variables](environment-variables)** - Configuration options
- **[Interactive Chat Guide](../user-guide/interactive-chat)** - Detailed usage guide
