# Tool Protocol — `code-context` MCP server

This document defines the contract that any MCP server claiming to be a `code-context` provider must implement. The same contract appears (in user-facing form) in §8 of the `CLAUDE.md` template.

If you change anything here, update `template/CLAUDE.md` §8 as well — the contract test will fail otherwise.

## Tools

| Tool | Signature | Returns |
|---|---|---|
| `search_repo` | `(query: str, top_k?: int = 5, scope?: str)` | `SearchResult[]` |
| `recent_changes` | `(since?: ISO8601, paths?: str[], max?: int = 20)` | `Change[]` |
| `get_summary` | `(scope?: "project" \| "module", path?: str)` | `ProjectSummary` |

### `search_repo`

Retrieve code fragments semantically relevant to a natural-language query.

- `query` (required): natural-language description of the task or question.
- `top_k` (optional, default 5): maximum number of results.
- `scope` (optional): repo-relative path prefix to constrain the search (e.g. `"packages/api"`).

### `recent_changes`

Return recent commits/diffs, optionally filtered.

- `since` (optional, ISO8601): cutoff. Defaults to "last 7 days" if omitted.
- `paths` (optional): list of repo-relative paths to filter by.
- `max` (optional, default 20): cap on results.

### `get_summary`

Return a structured project or module summary, intended for orientation at session start.

- `scope` (optional): `"project"` (default) or `"module"`.
- `path` (optional): required if `scope == "module"`.

## Return types

```
SearchResult {
  path: str          # Repo-relative path of the source file.
  lines: [int, int]  # [start, end], 1-indexed, inclusive on both ends (single line: [n, n]).
  snippet: str       # The matched fragment, verbatim.
  score: float       # Implementation-defined relevance score, higher = more relevant.
  why: str           # One sentence explaining why this fragment is relevant to the query.
}

Change {
  sha: str           # Full commit SHA.
  date: ISO8601      # Commit timestamp.
  author: str        # Commit author (display name).
  paths: str[]       # Files touched by this commit.
  summary: str       # First line of the commit message, trimmed.
}

ProjectSummary {
  name: str                                  # Project name (matches CLAUDE.md heading).
  purpose: str                               # One paragraph: what this project does and for whom.
  stack: str[]                               # Languages/frameworks/runtimes (e.g., ["Python 3.11", "FastAPI"]).
  entry_points: str[]                        # Repo-relative file paths of main executables/entrypoints.
  key_modules: { path: str, purpose: str }[] # Top-level modules with one-line purposes.
  stats: { files: int, loc: int, languages: str[] }  # Repo-wide aggregate stats.
}
```

`ISO8601` is a type alias for a string in ISO 8601 / RFC 3339 format (e.g., `2026-05-04T10:11:26+02:00`).

## Versioning

This contract is versioned via the document itself. Breaking changes (removing or renaming a tool, adding or promoting a required parameter, removing or renaming a required parameter, changing return type shapes) require a coordinated update with `mcp-core`. Additive changes (new tools, new optional parameters) do not.

The current version is **v1**.
