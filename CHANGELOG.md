# Changelog

## v0.3.0 — 2026-05-05

Tool Protocol contract bump from **v1.1** to **v1.2** (additive — no breaking changes).

- feat(protocol): add `get_file_tree(path?, max_depth?, include_hidden?)` returning `FileTreeNode`. Repo-relative directory tree with gitignore awareness; intended to replace `Bash: ls -R` / `Bash: tree` for orientation prompts.
- feat(protocol): add `explain_diff(ref, max_chunks?)` returning `DiffChunk[]`. AST-aligned chunks affected by the diff at `ref` (full SHA, `HEAD`, `HEAD~N`, branch); intended to replace `Bash: git show <sha>` for "what does this commit do" questions. Each `DiffChunk.change` is `"added"`, `"modified"`, or `"deleted"`.
- feat(protocol): three new return types — `FileTreeNode` (path, kind, children, size), `DiffFile` (path, hunks), `DiffChunk` (path, lines, snippet, kind, change) — documented alongside the existing return types.
- feat(template): `template/CLAUDE.md` §8 grows two bullets describing the new tools, with prescriptive language to nudge Claude away from the Bash fallbacks.
- test(contract): `EXPECTED_TOOLS` set in `tests/test_contract.py` now includes `get_file_tree` and `explain_diff`. Compatible servers must declare all seven tools.

`code-context` v0.7.0 will be the reference implementation.

## v0.2.0 — 2026-05-05

Tool Protocol contract bump from **v1** to **v1.1** (additive — no breaking changes).

- feat(protocol): add `find_definition(name, language?, max?)` returning `SymbolDef[]`. Locates the definition site of a named symbol; intended to replace `grep "def X"`-style queries from Claude Code.
- feat(protocol): add `find_references(name, max?)` returning `SymbolRef[]`. Lists textual references with word-boundary matching (so `log` doesn't match `logger`).
- feat(protocol): two new return types — `SymbolDef` (name, path, lines, kind, language) and `SymbolRef` (path, line, snippet) — documented alongside the existing return types.
- feat(template): `template/CLAUDE.md` §8 grows two bullets describing the new tools, with prescriptive language ("Use INSTEAD of grep when…") to nudge Claude away from built-ins.
- test(contract): `EXPECTED_TOOLS` set in `tests/test_contract.py` now includes `find_definition` and `find_references`. Compatible servers must declare all five tools.

`code-context` v0.5.0 will be the reference implementation. Existing `code-context` v0.4.x users continue to work — the bump is additive, so a server lacking the new tools simply doesn't expose them.

## v0.1.0 — 2026-05-04

Initial release.

- `template/CLAUDE.md` skeleton (9 sections).
- `template/.claude/memory/` structure with 4 categories + examples.
- `docs/tool-protocol.md` formal contract for the optional `code-context` MCP.
- `scripts/lint-template.sh` validates that a target repo applied the template correctly.
- Filled-in fixtures for Node (Fastify) and Python (FastAPI).
- GitHub Actions CI runs contract + lint tests on every push and PR.
