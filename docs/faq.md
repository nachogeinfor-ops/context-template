# FAQ

## Why is this Claude Code-specific?

Because Claude Code already has the four primitives this template uses: `CLAUDE.md` loading, per-project memory, MCP support, and hooks. Other coding assistants either lack them or implement them differently. A "universal" template would be the least common denominator and therefore worse than what Claude Code natively supports.

## Do I need the `code-context` MCP server to use this?

No. The template is useful standalone — `CLAUDE.md` and `.claude/memory/` provide value with zero extra installation. The Tool Protocol section (§8) only matters if you install the MCP. If you don't, delete §8.

## Can I add my own memory categories beyond the four?

Yes, but think twice. The four categories (decision/gotcha/glossary/playbook) cover the kinds of knowledge that get lost when people leave teams. If you find yourself wanting a fifth, ask: is this knowledge actually durable, or is it really an issue/PR/comment in disguise?

If you do add one, update the `type:` enum check in your local copy of the lint script and document the new type in your repo's `customization.md`.

## My `MEMORY.md` is over 200 lines. What now?

The 200-line cap exists because Claude Code truncates the file after that. Two options:

1. **Prune** — most likely many entries are stale. Delete them.
2. **Split** — if entries are still relevant, factor by component or module: `MEMORY.md` becomes a top-level pointer to `MEMORY-api.md`, `MEMORY-frontend.md`, etc. (You lose some discoverability. Pruning is better when possible.)

## Why can't the Tool Protocol section just say "use whatever tools the MCP exposes"?

Because the **timing** of tool use is what matters most, and that's project-specific. "Call `search_repo` before editing" is a habit Claude only forms if you tell it explicitly in `CLAUDE.md`. Generic "use available tools" instructions get ignored.

## Is the lint script run automatically?

Not by this project. The user (or their CI) runs it. Many teams add it as a pre-commit hook. The script is dependency-free bash so it's easy to wire up.

## What's the relationship between this and Claude Code's built-in `/init`?

`/init` is fine — it generates a `CLAUDE.md` from the current state of your repo. It's a one-shot scaffolder. This template is a **structure** you maintain over time, with a memory layer and a contract for the optional MCP. They're complementary: you can run `/init` to get a starting `CLAUDE.md`, then merge it into the structure here.

## Why version-control `.claude/memory/`?

Because it's repo knowledge, not personal knowledge. New team members benefit from cloning it. Personal preferences (about working style, communication, etc.) live in user-level memory at `~/.claude/`, outside the repo.

## What about `~/.claude/` per-user memory?

Out of scope for this template. Claude Code already manages user-level memory natively. This template only structures repo-level memory.
