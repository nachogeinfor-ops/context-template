# Changelog

## v0.1.0 — 2026-05-04

Initial release.

- `template/CLAUDE.md` skeleton (9 sections).
- `template/.claude/memory/` structure with 4 categories + examples.
- `docs/tool-protocol.md` formal contract for the optional `code-context` MCP.
- `scripts/lint-template.sh` validates that a target repo applied the template correctly.
- Filled-in fixtures for Node (Fastify) and Python (FastAPI).
- GitHub Actions CI runs contract + lint tests on every push and PR.
