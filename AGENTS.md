# GAIT Agent Guidelines

This repository is **GAIT** (Git for AI Turns) - a Python package for version-controlled AI conversations.

## Build & Development Commands

### Installation & Build
```bash
pip install -e .                 # Install in development mode
python -m build                  # Build distribution (uses hatchling)
pip install -r pyproject.toml      # Install with dev dependencies
```

### Testing
**No test suite exists** - this project currently has no tests.
When adding tests, use pytest and place them in `tests/` directory.

### Linting & Formatting
No linting/formatting configuration currently exists (no ruff, black, mypy, flake8 configured).
**Recommendation**: Consider adding `ruff` for linting and `black` for formatting.

## Code Style Guidelines

### Imports & Modules
- **Always** start files with: `from __future__ import annotations`
- Use absolute imports within package: `from .repo import GaitRepo`
- Standard library imports grouped before third-party imports
- No wildcard imports (`from x import *` is forbidden)

```python
# Correct order
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .repo import GaitRepo
from .objects import object_id
```

### Type System
- **Always** use type hints (Python 3.10+)
- Use `typing` module types: `Dict`, `List`, `Optional`, `Any`, `Union`
- Return types on ALL functions (even if None)
- Use `-> "ClassName"` for factory methods (forward reference)

```python
def store_object(objects_dir: Path, obj: Dict[str, Any]) -> str:
    ...

@staticmethod
def v0(
    parents: List[str],
    turn_ids: List[str],
    branch: str,
) -> "Commit":
    ...
```

### Naming Conventions
- **Functions/variables**: `snake_case` (e.g., `store_object`, `objects_dir`)
- **Classes**: `PascalCase` (e.g., `GaitRepo`, `Turn`, `Commit`)
- **Constants**: `UPPER_SNAKE_CASE` (rare in this codebase)
- **Private members**: `_leading_underscore` (internal use only)

### Data Structures
- Use `@dataclass(frozen=True)` for schema objects
- Use `field(default_factory=list/dict)` for mutable defaults
- Implement `to_dict()` method for serialization

```python
@dataclass(frozen=True)
class Turn:
    schema: str
    created_at: str
    user: Dict[str, Any]
    tokens: Tokens = field(default_factory=Tokens)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
```

### Error Handling
- Use descriptive exception messages with context
- Raise `RuntimeError` for expected failures (API errors, validation)
- Raise `FileNotFoundError` for missing resources
- Raise `ValueError` for invalid arguments
- **Never** suppress exceptions with empty `except: pass` blocks

```python
if not path.exists():
    raise FileNotFoundError(f"Object not found: {oid}")

if len(matches) > 1:
    raise ValueError(f"Ambiguous prefix {prefix} matches {len(matches)} objects")
```

### File I/O & Paths
- **Always** use `pathlib.Path` for file operations
- Use `read_text(encoding="utf-8")` and `write_text(..., encoding="utf-8")`
- Use `mkdir(parents=True, exist_ok=True)` for directory creation
- Use `rglob("*")` for recursive directory traversal

```python
path = objects_dir / oid[:2] / oid[2:4] / oid
path.parent.mkdir(parents=True, exist_ok=True)
raw = path.read_text(encoding="utf-8").strip()
```

### JSON Handling
- Use `json.dumps(sort_keys=True, separators=(",", ":"), ensure_ascii=False)` for canonical JSON
- Use `json.loads()` for parsing with proper error handling
- Canonical JSON is critical for content-addressed hashing (see `objects.py`)

### String Formatting
- Use f-strings for interpolation: `f"Object not found: {oid}"`
- Use `.strip()` for cleaning user input
- Use `"".join(list)` for concatenation (not `+` in loops)

### Code Organization
- Each file in `src/gait/` is a focused module
- Section comments use `# ====` for major sections, `# ----` for subsections
- Utility functions at top of file, classes below
- Static factory methods (`@staticmethod`) named `v0` for versioning

### Concurrency & Performance
- Use `timeout` parameter for HTTP requests (60s default, 600s for LLM)
- No async/await patterns - all synchronous code
- Content-addressed storage (sha256 hashing) for deduplication

### Documentation
- Docstrings are sparse but exist for complex functions
- Use triple-quoted strings for multi-line documentation
- Inline comments for non-obvious logic

## Project Structure

```
src/gait/
  __init__.py          # Package init, version export
  cli.py               # Command-line interface (largest file)
  repo.py              # Core repository logic
  llm.py               # LLM provider integrations (Ollama, OpenAI, Gemini, Anthropic)
  schema.py            # Dataclass definitions (Turn, Commit, Memory)
  objects.py            # Content-addressed storage primitives
  memory.py            # Memory pinning system
  remote.py            # GaitHub remote sync
  tokens.py            # Token counting utilities
  log.py               # Logging utilities
  verify.py            # Repository integrity verification
.gait/                 # Repository metadata (objects, refs, turns)
```

## Key Architecture Patterns

1. **Content-Addressed Storage**: All objects stored by SHA-256 hash of canonical JSON
2. **Immutable Data**: `@dataclass(frozen=True)` ensures dataclasses can't be modified after creation
3. **Ref-based Pointers**: Branches/refs are text files containing object hashes
4. **Memory Reflog**: `.gait/memory.jsonl` tracks pin/unpin operations as audit trail
5. **Fanout Directory Structure**: Objects stored in `.gait/objects/ab/cd/abcdef...` for filesystem efficiency

## Important Constraints

- **Python 3.10+ only** - no compatibility with earlier versions
- **No test coverage** - this is a gap; new features should include tests
- **Zero-config philosophy** - prefers sensible defaults over configuration files
- **GPL-3.0-only license** - all code must remain GPL compatible
