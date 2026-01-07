# GAIT Documentation Guide 📚

Welcome to the GAIT documentation! This guide will help you navigate our comprehensive documentation system.

## 📖 Where to Find Documentation

### 1. **Interactive Documentation Website** (Recommended!)

Visit **[https://automateyournetwork.github.io/gait](https://automateyournetwork.github.io/gait)** for:

- 🎨 Beautiful, searchable interface
- 📊 Interactive diagrams and visualizations
- 💡 Code examples you can copy-paste
- 🧪 Real-world recipes and use cases
- 🏗️ Deep-dive architecture guides
- 📱 Mobile-friendly responsive design

**Perfect for:** Learning GAIT, finding specific features, understanding architecture

### 2. **Quick Reference Files**

- **[README.md](README.md)** - Project overview and quick start
- **[AGENTS.md](AGENTS.md)** - Code style guidelines for contributors
- **[website/README.md](website/README.md)** - Documentation website development guide

**Perfect for:** Quick lookups, contributing to the project

### 3. **Built-in Help**

```bash
# Get help on any command
gait --help
gait chat --help
gait branch --help

# In chat, type /help
gait chat
> /help
```

**Perfect for:** Quick command syntax reminders

## 🗺️ Documentation Roadmap

### For New Users 🌱

Start here if you're new to GAIT:

1. **[Introduction](https://automateyournetwork.github.io/gait/docs/intro)** - What is GAIT and why use it?
2. **[Installation](https://automateyournetwork.github.io/gait/docs/getting-started/installation)** - Get GAIT running on your machine
3. **[Quickstart](https://automateyournetwork.github.io/gait/docs/getting-started/quickstart)** - Your first 5 minutes with GAIT
4. **[First Conversation](https://automateyournetwork.github.io/gait/docs/getting-started/first-conversation)** - Interactive walkthrough
5. **[Key Concepts](https://automateyournetwork.github.io/gait/docs/getting-started/key-concepts)** - Understand Turns, Commits, and Memory

### For Regular Users 👤

Once you're comfortable with basics:

- **[Interactive Chat Guide](https://automateyournetwork.github.io/gait/docs/user-guide/interactive-chat)** - Master chat commands
- **[Memory System](https://automateyournetwork.github.io/gait/docs/user-guide/memory-system)** - Persistent context management
- **[Branching & Merging](https://automateyournetwork.github.io/gait/docs/user-guide/branching-merging)** - Parallel conversation workflows
- **[Remote Sync](https://automateyournetwork.github.io/gait/docs/user-guide/remote-sync)** - GaitHub cloud sync

### For Power Users ⚡

Advanced techniques and workflows:

- **[Recipes](https://automateyournetwork.github.io/gait/docs/recipes/recovering-from-hallucinations)** - Real-world scenarios
  - Recovering from Hallucinations
  - Model Comparison
  - Knowledge Merging
  - Collaborative Reasoning
  - Squashing Conversations

### For Developers 🔧

Contributing or extending GAIT:

- **[Architecture Overview](https://automateyournetwork.github.io/gait/docs/architecture/overview)** - System design
- **[Content-Addressed Storage](https://automateyournetwork.github.io/gait/docs/architecture/content-addressed-storage)** - Object storage
- **[Commit DAG](https://automateyournetwork.github.io/gait/docs/architecture/commit-dag)** - Graph structure
- **[LLM Providers](https://automateyournetwork.github.io/gait/docs/architecture/llm-providers)** - Provider integration
- **[AGENTS.md](AGENTS.md)** - Coding standards and practices

### Need Help? 🆘

- **[Troubleshooting](https://automateyournetwork.github.io/gait/docs/troubleshooting/common-issues)** - Common issues and fixes
- **[Environment Setup](https://automateyournetwork.github.io/gait/docs/troubleshooting/environment-setup)** - Configuration help
- **[GitHub Issues](https://github.com/automateyournetwork/gait/issues)** - Report bugs or request features

## 📝 CLI Reference

Complete command documentation:

- **[CLI Commands](https://automateyournetwork.github.io/gait/docs/cli-reference/commands)** - `gait init`, `gait chat`, etc.
- **[Chat Commands](https://automateyournetwork.github.io/gait/docs/cli-reference/chat-commands)** - `/pin`, `/undo`, `/branch`, etc.
- **[Environment Variables](https://automateyournetwork.github.io/gait/docs/cli-reference/environment-variables)** - Configuration options

## 🎨 Documentation Features

Our documentation includes:

### 🎯 ELI5 (Explain Like I'm 5)
Every concept is explained with simple analogies:
- Turns are like photos 📸
- Commits are like pages in an album 📖
- Memory is like sticky notes 📌
- Branches are like parallel universes 🌌

### 📊 Interactive Diagrams
Mermaid diagrams show:
- Data flow
- Architecture
- Command workflows
- Branching strategies

### 💻 Real Code Examples
Copy-paste working examples:
```bash
gait init
gait chat --model llama3.1
> You are a helpful assistant
> /pin
```

### 🧪 Real-World Recipes
Practical scenarios like:
- Recovering from AI hallucinations
- Comparing different models
- Merging knowledge from branches
- Team collaboration workflows

### ✨ Fun & Engaging
- Emojis make content scannable
- Analogies make concepts clear
- Examples show real usage
- Tips and tricks throughout

## 🚀 Using the Documentation Website Locally

Want to run the docs website on your machine?

```bash
cd website
npm install
npm start
```

The site will open at `http://localhost:3000`

## 🤝 Contributing to Documentation

We welcome documentation improvements!

### Quick Fixes
For typos or small changes:
1. Click "Edit this page" at the bottom of any doc page
2. Make your changes on GitHub
3. Submit a pull request

### Major Changes
For new pages or major rewrites:
1. Clone the repository
2. Edit files in `website/docs/`
3. Test locally: `cd website && npm start`
4. Build to check for errors: `npm run build`
5. Submit a pull request

### Documentation Style Guide

- **Use emojis** for visual scanning 🎯
- **Keep it simple** - Explain like teaching a friend
- **Show examples** - Real commands and outputs
- **Add diagrams** - Mermaid for flows and architecture
- **Be comprehensive** - Cover edge cases and gotchas

## 📚 Documentation Structure

```
website/docs/
├── intro.md                     # Welcome & overview
├── getting-started/             # For beginners
│   ├── installation.md
│   ├── quickstart.md
│   ├── first-conversation.md
│   └── key-concepts.md
├── user-guide/                  # For regular users
│   ├── interactive-chat.md
│   ├── memory-system.md
│   ├── branching-merging.md
│   ├── remote-sync.md
│   ├── provider-setup.md
│   └── advanced-workflows.md
├── architecture/                # For developers
│   ├── overview.md
│   ├── content-addressed-storage.md
│   ├── commit-dag.md
│   ├── memory-reflog.md
│   ├── remote-protocol.md
│   ├── data-schemas.md
│   └── llm-providers.md
├── recipes/                     # For power users
│   ├── recovering-from-hallucinations.md
│   ├── model-comparison.md
│   ├── knowledge-merging.md
│   ├── collaborative-reasoning.md
│   └── squashing-conversations.md
├── cli-reference/               # Complete command reference
│   ├── commands.md
│   ├── chat-commands.md
│   └── environment-variables.md
└── troubleshooting/             # Help & debugging
    ├── common-issues.md
    └── environment-setup.md
```

## 🎓 Learning Paths

### Path 1: Casual User (30 minutes)
1. Read Introduction
2. Follow Installation
3. Complete Quickstart
4. Bookmark CLI Reference

### Path 2: Regular User (2 hours)
1. Complete Path 1
2. Read Key Concepts
3. Work through First Conversation
4. Read Interactive Chat Guide
5. Try a Recipe (Recovering from Hallucinations)

### Path 3: Power User (1 day)
1. Complete Path 2
2. Study Memory System
3. Master Branching & Merging
4. Set up Remote Sync
5. Work through all Recipes
6. Read Architecture Overview

### Path 4: Contributor (3 days)
1. Complete Path 3
2. Read all Architecture docs
3. Study AGENTS.md
4. Review codebase with architecture knowledge
5. Try adding a feature

## 🌟 Highlights

### Most Popular Pages

1. **[Quickstart](https://automateyournetwork.github.io/gait/docs/getting-started/quickstart)** - Get running in 5 minutes
2. **[Key Concepts](https://automateyournetwork.github.io/gait/docs/getting-started/key-concepts)** - Understand the fundamentals
3. **[Recovering from Hallucinations](https://automateyournetwork.github.io/gait/docs/recipes/recovering-from-hallucinations)** - Essential technique
4. **[Chat Commands](https://automateyournetwork.github.io/gait/docs/cli-reference/chat-commands)** - Quick reference

### Hidden Gems

- **Architecture Overview** - Beautifully illustrated system design
- **Memory System** - Deep dive into GAIT's "secret sauce"
- **Model Comparison Recipe** - A/B test different AIs

## 📱 Mobile Access

The documentation website is fully responsive! Access from:
- 📱 Phone
- 💻 Laptop
- 🖥️ Desktop
- 📱 Tablet

## 🔍 Search

Use the search bar (🔍) at the top of any documentation page to find:
- Commands
- Concepts
- Examples
- Recipes
- Architecture details

## 🎉 Start Learning!

Ready to dive in? Start here:

**→ [https://automateyournetwork.github.io/gait/docs/intro](https://automateyournetwork.github.io/gait/docs/intro)**

Welcome to GAIT! 🚀
