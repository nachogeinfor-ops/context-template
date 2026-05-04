# Contributing

Thanks for considering a contribution to `context-template`.

## Scope

This project is intentionally small and stack-agnostic. Pull requests welcome for:

- Bug fixes (lint script edge cases, contract test issues, fixture problems).
- Documentation improvements.
- Filled-in fixtures for additional stacks (Go, Rust, etc.) — kept under `tests/fixtures/sample-<stack>-repo/`.
- Tightening or clarifying the Tool Protocol contract (coordinated with `mcp-core` consumers).

Out of scope for now:

- Stack-specific overlays of the skeleton (the skeleton stays universal).
- Built-in CLI scaffolders (those belong to a separate `distribution` sub-project).
- New memory categories beyond decisions/gotchas/glossary/playbooks (open an issue first).

## Local setup

```bash
git clone https://github.com/nachogeinfor-ops/context-template.git
cd context-template
python -m venv .venv
source .venv/bin/activate          # Unix/macOS
# OR:
source .venv/Scripts/activate      # Git Bash on Windows
pip install -r tests/requirements.txt
```

## Running tests

```bash
pytest -v
```

There are 18 tests across two modules:

- `tests/test_contract.py` — verifies `docs/tool-protocol.md` and `template/CLAUDE.md` §8 declare the same tools/parameters/optionality.
- `tests/test_lint.py` — runs `scripts/lint-template.sh` against the skeleton + 4 bad fixtures + 2 sample fixtures and asserts exit codes.

## Running the lint script manually

```bash
bash scripts/lint-template.sh tests/fixtures/sample-node-repo
bash scripts/lint-template.sh tests/fixtures/sample-python-repo
bash scripts/lint-template.sh template       # should fail (placeholders)
```

## Editing the Tool Protocol

If you change tool names, parameters, or optionality, update **both**:

1. `docs/tool-protocol.md` (the canonical contract — table + return types).
2. `template/CLAUDE.md` §8 (the user-facing description with bullets).

The contract test will fail otherwise. This rule keeps `mcp-core` (the future MCP server sub-project) bound to a single source of truth.

## Pull request checklist

- [ ] Tests pass locally (`pytest -v`).
- [ ] Lint clean on both sample fixtures.
- [ ] Skeleton still fails lint (this is expected — placeholders are part of the design).
- [ ] If you touched the Tool Protocol, both files are updated and the contract test still passes.
- [ ] Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`).
- [ ] No bumping of `v0.1.0` tag — releases are tagged on the maintainer side.

## Reporting issues

Use GitHub Issues. A useful issue includes:

- What you tried (commands run, fixture used).
- What you expected vs. what happened.
- OS + bash version (`bash --version`) and Python version (`python --version`) if relevant.

Thanks!
