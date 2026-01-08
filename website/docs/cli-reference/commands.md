# CLI Command Reference 📟

Complete reference for all GAIT command-line commands.

## Global Options

All GAIT commands support these options:

```bash
--help, -h          Show help message
--version, -v       Show GAIT version
```

## Core Commands

### `gait init`

Initialize a new GAIT repository in the current directory.

**Usage:**
```bash
gait init
```

**What it does:**
- Creates `.gait/` directory
- Sets up `objects/`, `refs/`, and other subdirectories
- Creates initial `HEAD` file pointing to `refs/heads/main`

**Example:**
```bash
mkdir my-project
cd my-project
gait init
```

Output:
```
✅ Initialized empty GAIT repository in /Users/you/my-project/.gait
```

---

### `gait chat`

Start an interactive chat session with an LLM.

**Usage:**
```bash
gait chat [OPTIONS]
```

**Options:**
```bash
--model MODEL          Model to use (e.g., llama3.1, gpt-4.1-mini)
--provider PROVIDER    Force specific provider (ollama, chatgpt, gemini, anthropic)
--resume N             Resume with last N turns of history (default: 10)
--no-resume            Start fresh (no history)
--branch BRANCH        Start on specific branch (default: main)
```

**Examples:**

```bash
# Auto-detect provider, use llama3.1
gait chat --model llama3.1

# Force ChatGPT provider
gait chat --model gpt-4.1-mini --provider chatgpt

# Resume with 20 turns of history
gait chat --model llama3.1 --resume 20

# Start on experiment branch
gait chat --model llama3.1 --branch experiment

# Start completely fresh
gait chat --model llama3.1 --no-resume
```

---

### `gait log`

Show commit history for current branch.

**Usage:**
```bash
gait log [OPTIONS]
```

**Options:**
```bash
-n, --max-count N      Show only N commits (default: all)
--oneline              Show compact one-line format
--branch BRANCH        Show log for specific branch
```

**Examples:**

```bash
# Show all commits
gait log

# Show last 5 commits
gait log -n 5

# Show compact format
gait log --oneline

# Show log for specific branch
gait log --branch experiment
```

**Output Format:**

```
commit abc123def456... (main)
Date: 2026-01-07 10:30:45
Model: llama3.1
Turns: 1

    User: What is recursion?
    AI: Recursion is when a function calls itself...

commit 789abc456def...
Date: 2026-01-07 10:28:30
Model: llama3.1
Turns: 1

    User: Tell me about Python
    AI: Python is a high-level programming language...
```

---

### `gait branch`

List, create, or delete branches.

**Usage:**
```bash
gait branch [NAME] [OPTIONS]
```

**Options:**
```bash
-d, --delete NAME      Delete branch
-m, --move OLD NEW     Rename branch
--list                 List all branches (default)
```

**Examples:**

```bash
# List all branches
gait branch

# Create new branch
gait branch feature-experiment

# Delete branch
gait branch -d old-experiment

# Rename branch
gait branch -m old-name new-name
```

**Output:**

```
* main
  experiment
  feature-test
```

The `*` indicates your current branch.

---

### `gait checkout`

Switch to a different branch.

**Usage:**
```bash
gait checkout BRANCH
```

**Examples:**

```bash
# Switch to experiment branch
gait checkout experiment

# Switch back to main
gait checkout main
```

**Output:**
```
✅ Switched to branch 'experiment'
```

---

### `gait merge`

Merge another branch into the current branch.

**Usage:**
```bash
gait merge SOURCE [OPTIONS]
```

**Options:**
```bash
--with-memory          Also merge memory from source branch
--no-ff                Always create a merge commit (even if fast-forward possible)
```

**Examples:**

```bash
# Merge experiment into current branch
gait merge experiment

# Merge experiment including memory
gait merge experiment --with-memory

# Force merge commit
gait merge experiment --no-ff
```

**Output:**
```
✅ Merged branch 'experiment' into 'main'
```

---

### `gait show`

Show details of a specific object (commit, turn, memory).

**Usage:**
```bash
gait show OBJECT_ID
```

**Examples:**

```bash
# Show commit details
gait show abc123def

# Show turn details (full ID)
gait show abc123def456789...
```

**Output:**

```json
{
  "schema": "gait.commit.v0",
  "parents": ["def456..."],
  "turn_ids": ["turn123..."],
  "branch": "main",
  "created_at": "2026-01-07T10:30:45Z",
  "kind": "auto",
  "message": "chat"
}
```

---

### `gait remote`

Manage remote repositories (GaitHub).

**Usage:**
```bash
gait remote [COMMAND] [OPTIONS]
```

**Commands:**

```bash
add NAME URL           Add a remote
remove NAME            Remove a remote
list                   List all remotes
```

**Examples:**

```bash
# Add GaitHub remote
gait remote add origin https://gaithub-server.com

# List remotes
gait remote list

# Remove remote
gait remote remove origin
```

---

### `gait push`

Push commits and memory to a remote repository.

**Usage:**
```bash
gait push REMOTE [OPTIONS]
```

**Options:**
```bash
--owner OWNER          Repository owner (required for GaitHub)
--repo REPO            Repository name (required for GaitHub)
--branch BRANCH        Branch to push (default: current branch)
--with-memory          Also push memory
```

**Examples:**

```bash
# Push to GaitHub
gait push origin --owner john --repo my-project

# Push with memory
gait push origin --owner john --repo my-project --with-memory

# Push specific branch
gait push origin --branch experiment --owner john --repo my-project
```

**Requires:**
- `GAITHUB_TOKEN` environment variable set

---

### `gait fetch`

Fetch commits and memory from a remote repository.

**Usage:**
```bash
gait fetch REMOTE [OPTIONS]
```

**Options:**
```bash
--owner OWNER          Repository owner
--repo REPO            Repository name  
--branch BRANCH        Branch to fetch (default: all branches)
```

**Examples:**

```bash
# Fetch from GaitHub
gait fetch origin --owner john --repo my-project

# Fetch specific branch
gait fetch origin --branch main --owner john --repo my-project
```

---

### `gait pull`

Fetch and merge changes from a remote repository.

**Usage:**
```bash
gait pull REMOTE [OPTIONS]
```

**Options:**
```bash
--owner OWNER          Repository owner
--repo REPO            Repository name
--branch BRANCH        Branch to pull (default: current branch)
--with-memory          Also pull memory
```

**Examples:**

```bash
# Pull from GaitHub
gait pull origin --owner john --repo my-project

# Pull with memory
gait pull origin --owner john --repo my-project --with-memory
```

---

### `gait clone`

Clone a repository from a remote.

**Usage:**
```bash
gait clone URL [OPTIONS]
```

**Options:**
```bash
--owner OWNER          Repository owner
--repo REPO            Repository name
--path PATH            Local destination path
--branch BRANCH        Branch to checkout (default: main)
```

**Examples:**

```bash
# Clone from GaitHub
gait clone https://gaithub-server.com --owner john --repo my-project --path ./my-project
```

---

### `gait verify`

Verify repository integrity.

**Usage:**
```bash
gait verify [OPTIONS]
```

**Options:**
```bash
--fix                  Attempt to fix issues
--verbose              Show detailed output
```

**Examples:**

```bash
# Check integrity
gait verify

# Check and fix issues
gait verify --fix
```

**Output:**
```
✅ Checking object storage...
✅ Checking ref integrity...
✅ Checking DAG structure...
✅ Repository is healthy!
```

---

## Environment Variables

### Provider Configuration

```bash
# Set default provider
export GAIT_PROVIDER=ollama           # ollama | chatgpt | gemini | anthropic | openai_compat

# Set default model
export GAIT_DEFAULT_MODEL=llama3.1

# OpenAI-compatible APIs (Foundry Local, LM Studio, OpenAI)
export GAIT_BASE_URL=http://127.0.0.1:1234
export OPENAI_API_KEY=sk-...          # For ChatGPT

# Google Gemini
export GEMINI_API_KEY=your-key

# Anthropic Claude
export ANTHROPIC_API_KEY=your-key
```

### GaitHub Configuration

```bash
# GaitHub authentication
export GAITHUB_TOKEN=your-token
```

### Debug Settings

```bash
# Enable debug logging
export GAIT_DEBUG=1

# Set log level
export GAIT_LOG_LEVEL=DEBUG           # DEBUG | INFO | WARNING | ERROR
```

---

## Quick Reference Cheat Sheet

```bash
# Initialize
gait init

# Start chatting
gait chat --model llama3.1

# View history
gait log

# Create branch
gait branch experiment
gait checkout experiment

# Merge branch
gait checkout main
gait merge experiment --with-memory

# Remote operations
gait remote add origin https://gaithub-server.com
gait push origin --owner you --repo proj
gait pull origin --owner you --repo proj

# Verify integrity
gait verify
```

---

## Exit Codes

GAIT uses standard Unix exit codes:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Command-line argument error |
| 3 | Repository not found |
| 4 | Network error |
| 5 | Authentication error |

**Example usage in scripts:**

```bash
if gait verify; then
    echo "Repository is healthy!"
else
    echo "Repository has issues (exit code: $?)"
fi
```

---

## Next Steps

- **[Chat Commands Reference](chat-commands)** - Interactive chat commands (`/pin`, `/undo`, etc.)
- **[Environment Variables](environment-variables)** - Complete environment configuration
- **[User Guide](../user-guide/interactive-chat)** - Learn how to use GAIT effectively
