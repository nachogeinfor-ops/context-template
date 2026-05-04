# Memory Types: when to use which

Repo memory has four categories. Picking the right one matters because Claude Code uses the category to decide relevance and load order.

## Decision

A choice that **closes off other options**. Use this when someone might later ask "why did we go with X instead of Y?" and the answer would otherwise be lost.

- ADRs go here, but lighter — no need for an Adoption Decision Record template.
- Don't write a decision file for changes that don't lock anything in. "We renamed `User` to `Account`" is not a decision; it's a refactor.

**Filename:** `decisions/<short-slug>.md`. Example: `decisions/use-postgres.md`.

## Gotcha

A non-obvious **trap** that has bitten you (or that a maintainer would walk into without warning). Use this when someone could repeat a past mistake by following surface-level logic.

- Always include the **why**: what made the trap non-obvious.
- Reference the file or function involved.
- If the gotcha was caused by a specific bug, link to the issue/PR.

**Filename:** `gotchas/<short-slug>.md`. Example: `gotchas/timezone-mismatch-in-reports.md`.

## Glossary

Domain vocabulary specific to your project. Use this when a word means something **in this codebase** that's different from its everyday meaning, OR when the term is internal jargon a newcomer won't know.

- Keep entries short — one paragraph plus relationships ("a tenant has many users").
- Don't define generic CS terms. "What is a hash map" is not a glossary entry.

**Filename:** `glossary/<term>.md`. Example: `glossary/tenant.md`.

## Playbook

A repeatable **how-to** for a workflow you (or your team) execute often: adding an endpoint, deploying a service, rotating a secret.

- Numbered steps. Each step is one action.
- Include the most-common pitfall at the end.
- Don't write a playbook for one-off operations.

**Filename:** `playbooks/<verb-noun>.md`. Example: `playbooks/add-a-new-api-endpoint.md`.

## Frontmatter

Every memory file (except those in `_examples/`) starts with YAML frontmatter:

```yaml
---
name: <slug-matching-filename>
description: <one-sentence hook used to judge relevance>
type: decision | gotcha | glossary | playbook
scope: <module-or-component-name | "global">
created: YYYY-MM-DD
---
```

The `description` ends up in `MEMORY.md` as the line hook. Make it specific — "auth stuff" is useless; "Why we chose JWTs over sessions for the public API" is searchable.

## What does NOT go in memory

- Anything already in code (the code is authoritative — don't duplicate).
- Anything in CLAUDE.md (overview/architecture/commands — that's static repo context).
- Personal preferences (those go in user-level memory, outside this repo).
- Ephemeral state ("currently debugging X") — use issues, not memory.

## Pruning

When a memory entry stops being true, **delete it** rather than annotating it. Stale memory is worse than no memory because Claude treats it as authoritative. The git history preserves the old content if you need it.
