# Your First Conversation 💬

Let's have a real conversation with GAIT and learn all the features as we go! This guide will walk you through a complete session step-by-step. 🎯

## Prerequisites ✅

Before starting, make sure you've:
- ✅ Installed GAIT ([Installation Guide](installation))
- ✅ Set up an LLM provider (Ollama, ChatGPT, etc.)
- ✅ Have a terminal/command prompt open

## Starting Your First Chat 🚀

### 1. Create a Practice Project

```bash
mkdir ~/gait-practice
cd ~/gait-practice
gait init
```

```
✅ Initialized empty GAIT repository in /Users/you/gait-practice/.gait
```

:::tip What's a Repository?
Think of a GAIT repository like a notebook for one topic or project. Just like you might have separate notebooks for "School" and "Personal", you can have separate GAIT repositories for different projects!
:::

### 2. Launch the Chat Interface

```bash
gait chat --model llama3.1
```

You'll see this interface:

```
GAIT Interactive Chat (Ctrl+C or /exit to quit)
Branch: main | Model: llama3.1 | Provider: ollama

Commands:
  /pin /undo /branch /checkout /merge /memory /models /model /exit

> 
```

**Let's break down what you're seeing:**

- **Branch: main** - You're on the "main" timeline (like the main story)
- **Model: llama3.1** - The AI brain you're talking to
- **Provider: ollama** - Where the AI is running (local computer)
- **Commands:** - Quick reference of available commands
- **>** - The prompt (waiting for your input!)

## Having a Conversation 💭

### Normal Chatting (No Commands)

Just type naturally! Let's ask something:

```
> Tell me three fun facts about space
```

Press Enter and wait for the response:

```
AI: Here are three fun facts about space:

1. A day on Venus is longer than its year! Venus takes 243 Earth days to 
   rotate once, but only 225 Earth days to orbit the Sun.

2. There are more stars in the universe than grains of sand on all of 
   Earth's beaches - estimated at over 100 billion trillion stars!

3. If you could drive a car to the moon at 60mph, it would take about 
   160 days of non-stop driving!

> 
```

**That's it!** Chatting with GAIT is just like chatting with any AI. The magic comes from the commands. ✨

## Learning the Commands 🎮

### The /pin Command: Remember This! 📌

Let's set up some context that we want the AI to always remember:

```
> You are a space science tutor. Always explain things simply and use analogies. When I ask about planets, always mention their size compared to Earth.
```

```
AI: Understood! I'll be your space science tutor and follow those guidelines...
```

Now let's pin this so the AI NEVER forgets:

```
> /pin
```

```
✅ Pinned last turn to memory
```

**What just happened?**

That instruction is now "tattooed" into the AI's memory for this conversation! Even after 1000 turns, it will still:
- Explain things simply ✅
- Use analogies ✅
- Compare planets to Earth ✅

:::tip When to Use /pin
Pin whenever you want to set "ground rules" for the conversation:
- Personality/role ("You are a helpful teacher")
- Style rules ("Always use simple language")
- Project context ("We're building a recipe app")
- Important facts ("Our company name is TechCorp")
:::

### The /undo Command: Oops! ⏪

Let's say the AI makes a mistake. Watch:

```
> What's the largest planet in our solar system?
```

```
AI: The largest planet in our solar system is Mars.
```

**That's wrong!** (It's Jupiter) Let's fix it:

```
> /undo
```

```
✅ Reverted to previous commit
```

**Poof!** The wrong answer disappeared. It's like it never happened! Now ask again:

```
> What's the largest planet in our solar system?
```

```
AI: The largest planet in our solar system is Jupiter! It's so massive 
that you could fit about 1,300 Earths inside it. Think of Earth as a 
grape, and Jupiter as a basketball - that's roughly the size difference!
```

**Much better!** Notice how the AI still remembered to compare to Earth (because we pinned that instruction)! 🎉

:::caution /undo vs Telling the AI It's Wrong
**Bad approach:** "No, that's wrong. Jupiter is the largest."
- Now the conversation contains the wrong info (Mars)
- The AI might get confused and reference the mistake later

**Good approach:** `/undo` then ask again
- The wrong answer is completely erased
- Clean conversation history
- No confusion!
:::

### The /branch Command: Parallel Universes 🌌

Sometimes you want to try different conversation directions without losing your current one. Let's try:

```
> /branch solar-system
```

```
✅ Created branch 'solar-system'
✅ Switched to branch 'solar-system'
```

Notice the prompt changed:

```
Branch: solar-system | Model: llama3.1 | Provider: ollama
> 
```

Now let's explore:

```
> Tell me about the planets in order from the Sun
```

```
AI: Here are the planets in order from the Sun:

1. Mercury (smallest, about 38% of Earth's size)
2. Venus (similar size to Earth, 95% of Earth's diameter)
3. Earth (our home!)
4. Mars (about half Earth's size)
...
```

Great! But what if we want to go back to our original conversation?

### The /checkout Command: Timeline Jumping 🔄

```
> /checkout main
```

```
✅ Switched to branch 'main'
```

Look at your conversation - the planet list is gone! You're back to where you were before creating the branch.

But don't worry, the planet list still exists:

```
> /checkout solar-system
```

```
✅ Switched to branch 'solar-system'
```

And the planet list is back! 🎉

:::info Understanding Branches
Think of branches like parallel dimensions in a movie:

**Main Timeline:** You asked about Jupiter
**Solar-System Timeline:** You asked for a planet list

Both timelines exist! You can jump between them anytime. They're completely separate but share the same history up to the point where you branched.
:::

### The /memory Command: What Do You Remember? 🧠

```
> /memory
```

```json
{
  "schema": "gait.memory.v0",
  "items": [
    {
      "turn_id": "abc123...",
      "commit_id": "def456...",
      "note": "Space science tutor instructions",
      "pinned_at": "2026-01-07T10:30:45Z"
    }
  ]
}
```

This shows everything you've pinned! Right now, just our tutor instructions.

Let's pin something else:

```
> Jupiter is 11 times wider than Earth
> /pin
```

```
> /memory
```

```json
{
  "schema": "gait.memory.v0",
  "items": [
    {
      "turn_id": "abc123...",
      "note": "Space science tutor instructions",
      "pinned_at": "2026-01-07T10:30:45Z"
    },
    {
      "turn_id": "xyz789...",
      "note": "Jupiter size comparison",
      "pinned_at": "2026-01-07T10:35:12Z"
    }
  ]
}
```

Now we have TWO pinned memories! 📌📌

### The /models and /model Commands: Switching Brains 🧠

Want to see what AI models are available?

```
> /models
```

```
Available models for provider 'ollama':
  - llama3.1
  - llama3.3
  - gemma2
  - qwen2.5
  - mistral
  ...
```

Want to try a different model?

```
> /model gemma2
```

```
✅ Switched to model 'gemma2'
```

**Now the conversation continues, but with a different AI!** You can compare how different models answer the same questions. 🤖 vs 🤖

:::tip Model Comparison
This is SUPER useful for:
- Testing which model works best for your task
- Comparing response quality
- Finding the fastest model
- Discovering which model understands your topic best
:::

## Advanced Commands 🚀

### /merge: Combining Timelines 🔗

Remember our `solar-system` branch? Let's bring that information into `main`:

```
> /checkout main
> /merge solar-system
```

```
✅ Merged branch 'solar-system' into 'main'
```

Now `main` has both:
- The Jupiter conversation ✅
- The planet list ✅

### /exit: Saving and Leaving 💾

```
> /exit
```

```
Goodbye! 👋
```

**Everything is automatically saved!** You can come back anytime:

```bash
gait chat --model llama3.1
```

And your entire conversation history and pinned memories will still be there! 🎉

## Understanding the Interface Better 🎛️

### The Status Bar

```
Branch: main | Model: llama3.1 | Provider: ollama
```

This always shows:
1. **Branch**: Which timeline you're on
2. **Model**: Which AI brain you're using
3. **Provider**: Where it's running (local or cloud)

### The Prompt Symbol

```
> 
```

The `>` means GAIT is waiting for input. You can type either:
- **Regular text**: Have a normal conversation
- **/command**: Use a special GAIT command

### Visual Feedback

GAIT always tells you what happened:
- ✅ Success messages (green checkmark)
- ❌ Error messages (red X)
- 📌 Pin confirmations
- 🔀 Branch switches

## Complete Workflow Example 🎬

Let's put everything together in one complete session:

```bash
# Start
gait init
gait chat --model llama3.1

# Set up context
> You are helping me learn astronomy. Use simple explanations.
> /pin

# Have some conversations
> What is a black hole?
(AI explains)

> What are galaxies?
(AI explains)

# Create experimental branch
> /branch deep-dive

# Explore deeply on branch
> Tell me about the formation of black holes in detail
(AI gives detailed explanation)

# Go back to main for high-level learning
> /checkout main

# Continue with simpler questions
> What's a supernova?
(AI explains simply)

# Check what's pinned
> /memory

# Try different model
> /model gemma2
> Explain neutron stars
(See how gemma2 explains it)

# Switch back
> /model llama3.1

# Save and exit
> /exit
```

**Result:** You now have:
- ✅ A `main` branch with simple astronomy learning
- ✅ A `deep-dive` branch with detailed black hole info
- ✅ Pinned instructions that persist across everything
- ✅ Experience with two different AI models
- ✅ Complete history saved forever

## Tips for Your First Session 💡

### Start Small

Don't try to learn everything in one session! Start with:
1. Normal chatting
2. Using `/pin` for context
3. Using `/undo` for mistakes

Then gradually add:
4. Creating branches
5. Switching models
6. Using memory

### Pin Early, Pin Often

The earlier you pin important context, the better your conversation will be. Good things to pin:
- Your role/persona for the AI
- Project context
- Style preferences
- Important facts or constraints

### Don't Fear Experimentation

**You can't break anything!** The worst that happens:
- You delete the `.gait` folder and start fresh
- You `/undo` something you didn't mean to

GAIT is designed to be safe. Try things! 🧪

### Use Branches for "What If" Questions

Anytime you think "I wonder what would happen if...", create a branch!

```
> /branch what-if
> (try your experiment)
> /checkout main
> (back to safety)
```

### Name Your Branches Clearly

Instead of:
- `test` ❌
- `branch1` ❌
- `asdf` ❌

Use:
- `mobile-responsive` ✅
- `bug-investigation` ✅
- `model-comparison` ✅

Future you will thank present you! 😊

## Common First-Time Issues 🐛

### "I pinned something by accident!"

No problem! You can unpin with:
```
> /unpin 0
```
(The number is the index in `/memory` output)

### "I created too many branches!"

List them:
```bash
gait branch
```

Delete one:
```bash
gait branch -d branch-name
```

### "The AI doesn't remember what I pinned!"

Make sure you're on the right branch:
```
> /checkout main
> /memory
```

Memory is branch-specific! Different branches have different memories.

### "I want to start completely over"

```bash
# Exit the chat first
> /exit

# Delete everything
rm -rf .gait

# Start fresh
gait init
gait chat --model llama3.1
```

## Next Steps 🗺️

Congratulations! You've had your first GAIT conversation. Now you can:

1. **[Master the User Guide](../user-guide/interactive-chat)** - Learn every command in detail
2. **[Explore Recipes](../recipes/recovering-from-hallucinations)** - See real-world use cases
3. **[Understand the Architecture](../architecture/overview)** - Learn how GAIT works under the hood

---

## First Conversation Checklist ✅

Did you try all these?

- ☐ Start a chat with `gait chat`
- ☐ Ask the AI a question (normal text)
- ☐ Pin something with `/pin`
- ☐ Undo a response with `/undo`
- ☐ Create a branch with `/branch`
- ☐ Switch branches with `/checkout`
- ☐ Check memory with `/memory`
- ☐ List models with `/models`
- ☐ Exit with `/exit`
- ☐ Restart and see your history is saved

**If you checked all these boxes, you're ready to use GAIT for real work!** 🎉

---

:::tip Share Your Experience!
Having trouble? Have a cool use case? Open an issue on [GitHub](https://github.com/automateyournetwork/gait/issues) - we'd love to hear from you! 💌
:::
