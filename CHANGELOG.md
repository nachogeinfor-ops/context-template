# Changelog

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
