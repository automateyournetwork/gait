# Recovering from Hallucinations 🩹

**The Problem:** AI sometimes "hallucinates" - it makes things up that sound convincing but are completely wrong! This is one of the biggest challenges with AI. 😵

**The GAIT Solution:** The `/undo` command is your safety net! ✨

## What Are Hallucinations? 🤔

**Hallucinations** are when AI generates false information confidently.

### Examples of Hallucinations

```
❌ "The Eiffel Tower was built in 1999"
   (Actually: 1889)

❌ "Python was created by Tim Berners-Lee"
   (Actually: Guido van Rossum)

❌ "To sort in Python, use list.order()"
   (Actually: list.sort() or sorted())
```

The dangerous part? **AI says these with complete confidence!** 😱

## The Old Way (Without GAIT) 😰

```
You: "Who invented Python?"

AI: "Python was invented by Tim Berners-Lee in 1995."
     (This is WRONG! Tim created the Web, not Python)

You: "Tell me more about his work on Python"

AI: "Tim Berners-Lee designed Python to be a simple web scripting 
     language at CERN..."
     (Now it's building on the false information!)

You: "What other languages did he create?"

AI: "Besides Python, Tim also created JavaScript and HTML..."
     (Completely derailed! All following info is contaminated)
```

**Result:** The entire conversation is now built on false information. You'd have to start over. 🔄

## The GAIT Way ✨

```
You: "Who invented Python?"

AI: "Python was invented by Tim Berners-Lee in 1995."

You: (Hmm, that doesn't sound right...)
> /undo

✅ Reverted to previous commit

You: "Who invented Python?"

AI: "Python was created by Guido van Rossum and first released in 1991."
     (Correct!)

You: "Tell me about his design philosophy"

AI: "Guido van Rossum designed Python with the philosophy that code should
     be readable and simple. He wanted programming to be accessible..."
     (All correct! Clean conversation history)
```

**Result:** Clean conversation with accurate information! 🎉

## When to Use /undo 🎯

### 1. Factual Errors

```bash
> What's the capital of Australia?
AI: "The capital of Australia is Sydney."  ❌ (It's Canberra!)

> /undo
✅ Reverted

> What's the capital of Australia?
AI: "The capital of Australia is Canberra."  ✅
```

### 2. Code That Doesn't Work

```bash
> Show me how to read a file in Python
AI: "Use this code:
     f = open('file.txt')
     data = f.read_file()  # ❌ Wrong method!
     f.close()"

> /undo
✅ Reverted

> Show me how to read a file in Python
AI: "Use this code:
     f = open('file.txt')
     data = f.read()  # ✅ Correct!
     f.close()"
```

### 3. Wrong Tone or Style

```bash
> Explain quantum physics simply
AI: "Quantum superposition occurs when the wave function exists in a 
     Hilbert space representing a linear combination of eigenstates..."
     (Way too complex! 🤯)

> /undo
✅ Reverted

> Explain quantum physics simply, like I'm 10 years old
AI: "Imagine a coin spinning in the air. While it's spinning, it's both
     heads AND tails at the same time! That's kind of like quantum 
     superposition..."
     (Much better! 😊)
```

### 4. Off-Topic Responses

```bash
> Tell me about JavaScript promises
AI: "JavaScript is a programming language created by Brendan Eich. It was
     originally called LiveScript and was developed at Netscape..."
     (I didn't ask for history! 😤)

> /undo
✅ Reverted

> Explain JavaScript promises with a simple example
AI: "A Promise in JavaScript represents a value that might not be available
     yet. Here's a simple example:
     
     const promise = new Promise((resolve, reject) => {
       setTimeout(() => resolve('Done!'), 1000);
     });
     
     promise.then(result => console.log(result));"
     (Perfect! 🎯)
```

## Advanced Undo Techniques 🚀

### Chain Undoing

You can undo multiple times in a row!

```bash
> Tell me about dogs
AI: (Response about dogs)

> Tell me about cats  
AI: (Response about cats)

> Tell me about birds
AI: (Response about birds)

> /undo
✅ Back before "birds"

> /undo
✅ Back before "cats"

> /undo
✅ Back before "dogs"
```

**Use case:** You went down a rabbit hole and want to get back to where you were.

### Undo + Pin Workflow

```bash
> You are a Python expert. Always show type hints.
AI: "Understood! I'll include type hints in all Python code."

> /pin
✅ Pinned to memory

> Write a function to add two numbers
AI: "def add(a, b):  # ❌ No type hints!
         return a + b"

> /undo
✅ Reverted

> Write a function to add two numbers
AI: "def add(a: int, b: int) -> int:  # ✅ Type hints included!
         return a + b"
```

**Why this works:** The pinned instruction persists, but the bad response is removed!

### Undo + Branch Workflow

```bash
> Explain recursion
AI: (Gives a confusing explanation)

> /branch better-explanation
> /undo  # Undo on the branch
> Explain recursion with a simple example
AI: (Gives better explanation)

# Now you have:
# - main: Confusing explanation (kept for reference)
# - better-explanation: Clear explanation (for actual use)
```

## Preventing Hallucinations with /pin 📌

You can reduce hallucinations by pinning important context!

### Example: Math Helper

```bash
> You are a math tutor. IMPORTANT: Always double-check calculations. 
  If unsure, say "let me verify that" instead of guessing.
> /pin

# Now the AI is less likely to hallucinate answers!
```

### Example: Code Helper

```bash
> You are a coding assistant for Python 3.11. IMPORTANT: Only suggest
  features that exist in Python 3.11. If unsure, say "I'm not certain
  that feature exists in Python 3.11".
> /pin

# Reduces hallucinations about non-existent features!
```

## The Cost of Not Using /undo 💸

### Wasted Time

```
Without /undo:
1. AI hallucinates (30 seconds)
2. You try to correct it (2 minutes)
3. AI gets confused (1 minute)  
4. You start a new chat (30 seconds)
5. You copy context over (3 minutes)
Total: ~7 minutes wasted!

With /undo:
1. AI hallucinates (30 seconds)
2. You /undo (1 second!)
3. AI gives correct answer (30 seconds)
Total: ~1 minute!
```

### Context Pollution

**Without /undo:** Every bad response stays in the conversation, potentially affecting future responses.

**With /undo:** Clean history means better future responses!

## Real-World Examples 🌍

### Example 1: Learning History

```bash
gait chat --model llama3.1

> When was the Declaration of Independence signed?
AI: "The Declaration of Independence was signed on July 1, 1776."
    ❌ (Slightly wrong! It was July 4)

> /undo
> When was the Declaration of Independence signed?
AI: "The Declaration of Independence was signed on July 4, 1776."
    ✅

> Who signed it first?
AI: "John Hancock signed first, with his famously large signature."
    ✅ (Correct! Clean history led to correct follow-up)
```

### Example 2: Coding Project

```bash
> How do I make an HTTP request in Python?
AI: "Use the http module like this:
     import http
     response = http.get('https://api.example.com')"
     ❌ (Wrong! Should use `requests` or `urllib`)

> /undo
> How do I make an HTTP request in Python using the requests library?
AI: "Use the requests library:
     import requests
     response = requests.get('https://api.example.com')
     print(response.json())"
     ✅ (Correct!)
```

### Example 3: Recipe Helper

```bash
> How long do I bake cookies at 350°F?
AI: "Bake cookies at 350°F for 45 minutes."
    ❌ (Too long! Most cookies burn after 45 min)

> /undo
> How long do I bake chocolate chip cookies at 350°F?
AI: "Bake chocolate chip cookies at 350°F for 10-12 minutes, until the
     edges are golden but the center is still soft."
     ✅ (Much better!)
```

## Tips for Effective Hallucination Recovery 💡

### 1. Verify First, Undo Second

Don't blindly trust AI! If something seems off:
- Check it yourself (Google, documentation, etc.)
- If wrong, `/undo` immediately
- Rephrase your question for clarity

### 2. Be Specific After Undoing

```bash
❌ "Tell me about that"  # Vague
✅ "Tell me about Python's list comprehension syntax"  # Specific
```

### 3. Add Context in Your Next Attempt

```bash
# First attempt (hallucinated)
> How do I do X?

> /undo

# Second attempt (with context)
> How do I do X using Python 3.11's standard library?
```

### 4. Use /pin to Set Expectations

```bash
> If you're not certain about something, say "I'm not sure" instead of
  guessing.
> /pin
```

### 5. Create a "Testing" Branch

```bash
> /branch test-answers

# Test the AI's answer here first
> (Ask your question)

# If it hallucinates, just checkout main
> /checkout main

# No need to undo! The hallucination is isolated on the branch.
```

## Comparison with Other Approaches ⚖️

| Approach | Time to Fix | Clean History? | Learning Curve |
|----------|------------|----------------|----------------|
| **GAIT /undo** | 1 second | ✅ Yes | Low |
| **Correct via chat** | 2-5 minutes | ❌ No | Low |
| **Start new chat** | 5+ minutes | ✅ Yes | Low |
| **Edit message (ChatGPT)** | 30 seconds | ⚠️ Partial | Medium |
| **Regenerate (ChatGPT)** | 30 seconds | ❌ No | Low |

**GAIT's `/undo` is the fastest and cleanest solution!** 🏆

## Summary Checklist ✅

Use `/undo` when:
- ☐ AI gives factually incorrect information
- ☐ Code doesn't work or has bugs
- ☐ Response is off-topic
- ☐ Tone/style is wrong
- ☐ You want to try asking differently

Don't use `/undo` when:
- ☐ Answer is correct but incomplete (just ask for more detail)
- ☐ You want to explore alternatives (use `/branch` instead)
- ☐ You're testing multiple approaches (use branches!)

---

## Next Steps 🗺️

- **[Model Comparison](model-comparison)** - Compare different AI models
- **[Knowledge Merging](knowledge-merging)** - Merge information from branches
- **[Interactive Chat Guide](../user-guide/interactive-chat)** - All chat commands

**Remember:** `/undo` is your safety net. Don't be afraid to use it liberally! 🎪
