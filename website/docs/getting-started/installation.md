# Installation 📦

Let's get GAIT on your computer! This is easier than making a sandwich. 🥪

## Before You Start ✋

You need **Python 3.10 or newer** on your computer. Think of Python like the electricity that makes GAIT work!

### Check if You Have Python 🐍

Open your terminal (the black or white box where you type commands) and type:

```bash
python --version
```

You should see something like:
```
Python 3.11.5
```

If the number after "Python" is **3.10 or higher**, you're good to go! 🎉

:::tip What if I don't have Python?

**Mac Users:** Python 3 comes with your Mac! If not, download from [python.org](https://www.python.org/downloads/)

**Windows Users:** Download from [python.org](https://www.python.org/downloads/)

**Linux Users:** You probably already have it! If not:
```bash
sudo apt install python3  # Ubuntu/Debian
sudo dnf install python3  # Fedora
```
:::

## Step 1: Install GAIT 🚀

Super simple! Just type this in your terminal:

```bash
pip install gait-ai
```

:::info What's happening?
`pip` is like the app store for Python programs. When you type this command:
1. 📡 It connects to the internet
2. 📦 Downloads GAIT
3. 🔧 Installs it on your computer
4. ✅ Makes the `gait` command available everywhere!
:::

You'll see text scrolling by - that's normal! When it's done (usually 10-30 seconds), you're ready!

## Step 2: Verify Installation ✅

Let's make sure GAIT is working! Type:

```bash
gait --version
```

You should see something like:
```
gait version 0.0.9
```

**If you see this, congratulations! GAIT is installed!** 🎊

## Step 3: Set Up Your LLM Provider 🤖

GAIT needs an AI to talk to! You have two choices:

### Option A: Local AI (Runs on Your Computer) 🏠

**Best for:** Privacy, no internet needed, it's free!

**Easiest option: Ollama**

1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Install it (just double-click the installer)
3. Download a model:

```bash
ollama pull llama3.1
```

:::tip What model should I use?
- **llama3.1** - Great all-around model (8GB RAM needed)
- **gemma2** - Smaller, works on most computers (4GB RAM needed)
- **qwen2.5** - Very smart, needs more power (16GB RAM needed)

Don't worry if you don't know which to pick! Start with `llama3.1` - it's like the "medium" option. 😊
:::

### Option B: Cloud AI (Runs on the Internet) ☁️

**Best for:** More powerful, always available, costs money

**Popular options:**

#### OpenAI (ChatGPT)

```bash
# Get your API key from https://platform.openai.com/api-keys
export GAIT_PROVIDER=chatgpt
export OPENAI_API_KEY="sk-your-key-here"
```

#### Google Gemini

```bash
# Get your API key from https://makersuite.google.com/app/apikey
export GAIT_PROVIDER=gemini
export GEMINI_API_KEY="your-key-here"
```

#### Anthropic Claude

```bash
# Get your API key from https://console.anthropic.com/
export GAIT_PROVIDER=anthropic
export ANTHROPIC_API_KEY="your-key-here"
```

:::caution Keep Your Keys Secret! 🔐
API keys are like passwords - never share them or post them online!
:::

## Step 4: Test Everything! 🧪

Let's make sure everything works! 

1. Create a test folder:

```bash
mkdir ~/gait-test
cd ~/gait-test
```

2. Initialize GAIT:

```bash
gait init
```

You should see:
```
Initialized empty GAIT repository in /Users/yourname/gait-test/.gait
```

This creates a hidden `.gait` folder - it's where GAIT saves all your conversations!

3. Start chatting:

```bash
# If using Ollama
gait chat --model llama3.1

# If using ChatGPT
gait chat --model gpt-4.1-mini
```

You should see:
```
GAIT Interactive Chat (Ctrl+C to exit)
Branch: main | Model: llama3.1
>
```

**Type something and press Enter!** Try: "Tell me a short joke"

If the AI responds, **EVERYTHING IS WORKING!** 🎉

Type `/exit` or press `Ctrl+C` to leave the chat.

## Troubleshooting Installation Issues 🔧

### "gait: command not found"

This means `pip` installed GAIT in a place your terminal can't find.

**Fix:**
```bash
python -m pip install --user gait-ai
```

Then add this to your `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### "Could not detect a provider"

GAIT can't find any AI to talk to.

**Fix:** Make sure you completed Step 3!
- If using Ollama: Check if it's running with `ollama list`
- If using cloud: Check your API key is set with `echo $OPENAI_API_KEY`

### Port Already in Use

If you see "port 11434 already in use":

**Fix:**
```bash
# Stop Ollama
pkill ollama
# Start it again
ollama serve
```

## What's Next? 🗺️

Now that GAIT is installed, let's learn how to use it!

👉 **[Quickstart Guide](quickstart)** - Your first 5 minutes with GAIT

---

## Installation Cheat Sheet 📋

```bash
# Quick installation (copy-paste this)
pip install gait-ai
ollama pull llama3.1
mkdir ~/my-gait-project
cd ~/my-gait-project
gait init
gait chat --model llama3.1
```

**That's it!** You're now a GAIT user! 🎊
