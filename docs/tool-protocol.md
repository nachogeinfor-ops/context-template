# Tool Protocol — `code-context` MCP server

This document defines the contract that any MCP server claiming to be a `code-context` provider must implement. The same contract appears (in user-facing form) in §8 of the `CLAUDE.md` template.

If you change anything here, update `template/CLAUDE.md` §8 as well — the contract test will fail otherwise.

## Tools

| Tool | Signature | Returns |
|---|---|---|
| `search_repo` | `(query: str, top_k?: int = 5, scope?: str)` | `SearchResult[]` |
| `recent_changes` | `(since?: ISO8601, paths?: str[], max?: int = 20)` | `Change[]` |
| `get_summary` | `(scope?: "project" \| "module", path?: str)` | `ProjectSummary` |
| `find_definition` | `(name: str, language?: str, max?: int = 5)` | `SymbolDef[]` |
| `find_references` | `(name: str, max?: int = 50)` | `SymbolRef[]` |
| `get_file_tree` | `(path?: str, max_depth?: int = 4, include_hidden?: bool = false)` | `FileTreeNode` |
| `explain_diff` | `(ref: str, max_chunks?: int = 50)` | `DiffChunk[]` |

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

### `find_definition`

Locate the definition site(s) of a named symbol.

- `name` (required): exact identifier (function/class/method name).
- `language` (optional): hint to disambiguate same-name symbols across languages (e.g. `"python"`, `"javascript"`, `"typescript"`, `"go"`, `"rust"`, `"csharp"`).
- `max` (optional, default 5): cap on results.

### `find_references`

List every textual occurrence of a named symbol in the indexed corpus. Returns matches at line granularity. Word-boundary matched (so `"log"` does not return `"logger"`).

- `name` (required): exact identifier.
- `max` (optional, default 50): cap on results.

### `get_file_tree`

Return a hierarchical view of the repo's structure (gitignore-aware).

- `path` (optional): repo-relative subdirectory; defaults to root.
- `max_depth` (optional, default 4): cap on recursion depth.
- `include_hidden` (optional, default false): include dot-files / dot-dirs (`.git`, `.github`, `.env`, etc.).

Returns a single `FileTreeNode` (the requested root). Children are nested via `FileTreeNode.children`.

### `explain_diff`

Return AST-aligned chunks affected by the diff at `ref`. For each line range that changed in that commit, the chunker is consulted to find the enclosing function / class / method node. Useful for "what does this commit do" questions without reading the raw `git diff` line-by-line.

- `ref` (required): git ref (full SHA, short SHA, `HEAD`, `HEAD~N`, branch name).
- `max_chunks` (optional, default 50): cap on returned chunks.

Returns `DiffChunk[]`. Each chunk's `change` field is one of `"added"`, `"modified"`, `"deleted"`.

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

SymbolDef {
  name: str          # Identifier, exactly as written in the source.
  path: str          # Repo-relative.
  lines: [int, int]  # 1-indexed inclusive, like SearchResult.lines.
  kind: str          # "function" | "class" | "method" | "type" | "enum" | "interface" | "struct" | ...
  language: str      # "python" | "javascript" | "typescript" | "go" | "rust" | "csharp"
}

SymbolRef {
  path: str          # Repo-relative.
  line: int          # 1-indexed.
  snippet: str       # The matching line, trimmed.
}

FileTreeNode {
  path: str          # Repo-relative.
  kind: str          # "file" | "dir".
  children: FileTreeNode[]   # Empty for files; recursive for dirs (capped by max_depth).
  size: int | null   # Byte size for files; null for dirs.
}

DiffFile {
  path: str          # Repo-relative.
  hunks: [int, int][]   # Each hunk is [start_line, end_line] in the new file (1-indexed inclusive).
}

DiffChunk {
  path: str          # Repo-relative.
  lines: [int, int]  # 1-indexed inclusive, range of the AST node.
  snippet: str       # The chunk text.
  kind: str          # "function" | "class" | "method" | ... | "fragment" (if the chunker fell back to line-window).
  change: str        # "added" | "modified" | "deleted" — relative to the diff at `ref`.
}
```

`ISO8601` is a type alias for a string in ISO 8601 / RFC 3339 format (e.g., `2026-05-04T10:11:26+02:00`).

## Versioning

This contract is versioned via the document itself. Breaking changes (removing or renaming a tool, adding or promoting a required parameter, removing or renaming a required parameter, changing return type shapes) require a coordinated update with `mcp-core`. Additive changes (new tools, new optional parameters) do not.

The current version is **v1.2** (additive bump in v0.3.0 of `context-template`: adds `get_file_tree` and `explain_diff`).
