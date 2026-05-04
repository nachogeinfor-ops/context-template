# Customization Guide

How to take the skeleton in `template/` and turn it into your repo's filled-in `CLAUDE.md` and `.claude/memory/`.

## Step 1: Copy the template into your repo

From your repo root:

```bash
# Replace <CONTEXT_TEMPLATE_PATH> with where you cloned context-template/.
cp <CONTEXT_TEMPLATE_PATH>/template/CLAUDE.md ./CLAUDE.md
cp -R <CONTEXT_TEMPLATE_PATH>/template/.claude ./.claude
```

## Step 2: Fill in `CLAUDE.md`

Open `CLAUDE.md` and replace every angle-bracket placeholder. The lint script flags any you miss:

```bash
bash <CONTEXT_TEMPLATE_PATH>/scripts/lint-template.sh .
```

Sections to fill (in order — top-down works fine):

1. **Title and tagline** — `<PROJECT_NAME>` and the one-line description.
2. **Project Overview** — 3-5 sentences. Resist marketing language.
3. **Architecture** — replace the placeholder mermaid block with a real diagram, OR delete the diagram and write 5-10 sentences. Either is fine.
4. **Key Directories** — only the ones that matter. Don't dump the full tree.
5. **Conventions** — link to `.editorconfig`, `eslint.config`, `ruff.toml`, etc. instead of duplicating their content.
6. **Commands** — the 3-5 commands a developer uses every day. Not exhaustive — daily.
7. **Common Workflows** — two or three. More belongs in `.claude/memory/playbooks/`.
8. **Anti-Patterns** — give the **why** for every "don't". A rule without a reason invites being ignored.
9. **Tool Protocol (§8)** — keep this section if you've installed the `code-context` MCP. Delete it otherwise.
10. **References** — at minimum, link to your project's main external docs. Internal trackers go in private memory files, not here (this file may be public).

## Step 3: Decide what goes in `.claude/memory/`

Anything that is **dynamic** (changes more often than monthly), or **opinionated** (a judgment call rather than a fact), or **non-obvious** (a future maintainer wouldn't infer it from the code) belongs in memory, not in `CLAUDE.md`.

Use the right category — see [memory-types](memory-types.md).

## Step 4: Verify

Run the lint script. Fix every reported issue.

```bash
bash <CONTEXT_TEMPLATE_PATH>/scripts/lint-template.sh .
```

Expected on success: `✓ Template lint passed for .`

## Step 5: Commit it

`.claude/memory/` is meant to be committed and shared with your team. Don't `.gitignore` it.

## When to revise

- Update `CLAUDE.md` when architecture, key commands, or conventions actually change. Not for in-flight work.
- Update memory files freely — that's what they're for.
- If `MEMORY.md` exceeds ~200 lines, prune or split. Claude Code truncates it after that.
