# context-template

A stack-agnostic OSS template for giving [Claude Code](https://docs.claude.com/claude-code) durable per-repo context: a `CLAUDE.md` skeleton, a `.claude/memory/` structure, and a formal Tool Protocol contract for the optional `code-context` MCP server.

## What you get

- **`template/CLAUDE.md`** — 9-section skeleton you fill in (overview, architecture, conventions, commands, common workflows, anti-patterns, tool protocol, references).
- **`template/.claude/memory/`** — index + 4 categories (decisions, gotchas, glossary, playbooks) with examples.
- **`docs/tool-protocol.md`** — formal contract for the optional `code-context` MCP server.
- **`scripts/lint-template.sh`** — verifies that a repo has applied the template correctly.

The template is **standalone**: useful even if you don't install the MCP server. The Tool Protocol section unlocks additional capability when the MCP is present.

## Quickstart (30 seconds)

```bash
# 1. Clone this repo somewhere.
git clone https://github.com/<you>/context-template.git ~/tools/context-template

# 2. Copy the skeleton into your repo.
cd /path/to/your/repo
cp ~/tools/context-template/template/CLAUDE.md .
cp -R ~/tools/context-template/template/.claude .

# 3. Fill in CLAUDE.md (replace every <PLACEHOLDER>).

# 4. Verify.
bash ~/tools/context-template/scripts/lint-template.sh .
# → ✓ Template lint passed for .
```

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
