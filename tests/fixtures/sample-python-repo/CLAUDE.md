# sample-python-api

A minimal FastAPI service used as a fixture for the `context-template` project.

## 1. Project Overview

`sample-python-api` is a Python 3.11+ HTTP service exposing a single `/health` endpoint.
Its only purpose is to demonstrate what a real, filled-in `CLAUDE.md` looks like for a Python repo.
It has no production users — it's a fixture inside the `context-template` test suite.

## 2. Architecture

```mermaid
graph LR
  Client --> Uvicorn
  Uvicorn --> FastAPI
  FastAPI --> Health[/health]
```

A single FastAPI app served by uvicorn. No database, no auth, no background workers — by design.

## 3. Key Directories

| Path | Purpose |
|---|---|
| `src/api/` | Application package. |
| `src/api/main.py` | App factory + route definitions. |

## 4. Conventions

- **Code style:** Ruff (config in `pyproject.toml`).
- **Naming:** snake_case for everything except classes (PascalCase).
- **Tests:** pytest, located under `tests/`, mirror source layout.

## 5. Commands

| Command | Purpose |
|---|---|
| `pip install -e .[dev]` | Install in editable mode with dev deps. |
| `pytest` | Run the test suite. |
| `ruff check src` | Lint. |
| `uvicorn api.main:app --reload` | Run dev server. |

## 6. Common Workflows

### How to add a new endpoint

See [add-endpoint playbook](.claude/memory/playbooks/add-endpoint.md).

### How to fix a typical bug

1. Add a failing pytest case under `tests/api/test_<module>.py`.
2. Fix the code in `src/api/`.
3. Run `pytest`.

## 7. Anti-Patterns

- **Don't store naive datetimes** — see `.claude/memory/gotchas/utc-everywhere.md`.
- **Don't import Flask** — this repo uses FastAPI, see `.claude/memory/decisions/use-fastapi.md`.

## 8. Tool Protocol  <!-- mcp:code-context | OPTIONAL -->

<!-- Only if you have the `code-context` MCP installed.
     If not, delete this entire section.
     If you change tool signatures here, update docs/tool-protocol.md too —
     the contract test will fail otherwise. -->

You have three tools from the `code-context` MCP server. Use them proactively:

- **`search_repo(query, top_k?, scope?)`** — call this BEFORE editing or reading
  large amounts of code. The query should describe the task in natural language.
  Example: search_repo("where do we validate user emails on signup")

- **`recent_changes(since?, paths?, max?)`** — call when the user mentions "recent",
  "the new", "what changed", or before suggesting changes that might conflict
  with in-flight work.

- **`get_summary(scope?, path?)`** — call ONCE at the start of an unfamiliar
  task to orient yourself. Don't call repeatedly.

Prefer these tools over Glob/Grep when the question is semantic
("how do we do X") rather than literal ("where is the string Y").

## 9. References & Memory

### External resources

- **FastAPI docs:** https://fastapi.tiangolo.com/
- **Pydantic docs:** https://docs.pydantic.dev/

### Dynamic memory

Per-repo memory lives in `.claude/memory/`. Start with `.claude/memory/MEMORY.md`.
