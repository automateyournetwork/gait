# gait
An open source version and source control system, inspired by Git, for Artificial Intelligence Agents

# GAIT (v0)

GAIT is a local, git-like store for AI interactions.

## Quick start (dev)
```bash

python -m venv .venv

source .venv/bin/activate  

# windows: .venv\Scripts\activate

pip install -e .
pip install pytest
```

Create a GAIT project

```bash

mkdir /tmp/my_gait_project && cd /tmp/my_gait_project
gait init
gait status

```

Record a turn (auto-commit)

```bash

gait record-turn --user "Hello" --assistant "Hi!"
gait log

```

Run tests
```bash
pytest
```
``` yaml
---

# `src/gait/__init__.py`
```python
__all__ = ["__version__"]
__version__ = "0.0.1"

```