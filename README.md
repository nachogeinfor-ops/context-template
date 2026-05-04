# context-template

[![CI](https://github.com/nachogeinfor-ops/context-template/actions/workflows/ci.yml/badge.svg)](https://github.com/nachogeinfor-ops/context-template/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/nachogeinfor-ops/context-template?include_prereleases&sort=semver)](https://github.com/nachogeinfor-ops/context-template/releases)

A stack-agnostic OSS template for giving [Claude Code](https://docs.claude.com/claude-code) durable per-repo context: a `CLAUDE.md` skeleton, a `.claude/memory/` structure, and a formal Tool Protocol contract for the optional `code-context` MCP server.

## What you get

- **`template/CLAUDE.md`** — 9-section skeleton you fill in (overview, architecture, conventions, commands, common workflows, anti-patterns, tool protocol, references).
- **`template/.claude/memory/`** — index + 4 categories (decisions, gotchas, glossary, playbooks) with examples.
- **`docs/tool-protocol.md`** — formal contract for the optional `code-context` MCP server.
- **`scripts/lint-template.sh`** — verifies that a repo has applied the template correctly.

The template is **standalone**: useful even if you don't install the MCP server. The Tool Protocol section unlocks additional capability when the MCP is present.

## Quickstart (30 seconds)

```bash
# 1. Clone this repo somewhere once.
git clone https://github.com/nachogeinfor-ops/context-template.git ~/tools/context-template

# 2. From your repo root, run the installer.
cd /path/to/your/repo
bash ~/tools/context-template/install.sh
#   ✓ Template applied to /path/to/your/repo

# 3. Fill in CLAUDE.md (replace every <YOUR_*> / <PROJECT_NAME> placeholder).

# 4. Verify.
bash ~/tools/context-template/scripts/lint-template.sh .
# → ✓ Template lint passed for .
```

`install.sh` refuses to overwrite an existing `CLAUDE.md` or `.claude/`. Use `--force` to overwrite.

Open Claude Code in your repo. The new `CLAUDE.md` is loaded automatically.

## Documentation

- [Customization guide](docs/customization.md) — how to fill in the skeleton.
- [Memory types](docs/memory-types.md) — when to use decision vs gotcha vs glossary vs playbook.
- [Tool Protocol](docs/tool-protocol.md) — contract the optional MCP must implement.
- [FAQ](docs/faq.md).

## Contributing

This is OSS — issues and PRs welcome. To run tests locally:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Git Bash on Windows; .venv/bin/activate on Unix
pip install -r tests/requirements.txt
pytest -v
```

The contract test (`tests/test_contract.py`) keeps `docs/tool-protocol.md` and `template/CLAUDE.md` §8 in sync. The lint test (`tests/test_lint.py`) verifies the bash script behaves correctly on good and bad fixtures.

## License

[MIT](LICENSE).
