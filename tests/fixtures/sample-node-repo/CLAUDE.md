# sample-node-api

A minimal Fastify HTTP API used as a fixture for the `context-template` project.

## 1. Project Overview

`sample-node-api` is a TypeScript service exposing a single `/health` endpoint over HTTP.
Its only purpose is to demonstrate what a real, filled-in `CLAUDE.md` looks like for a Node repo.
It has no production users — it's a fixture inside the `context-template` test suite.

## 2. Architecture

```mermaid
graph LR
  Client --> Fastify[Fastify HTTP server]
  Fastify --> Routes[/health route handler]
```

The service is a single Fastify instance. Routes live as inline handlers in `src/server.ts`.
There is no database, no auth, and no business logic — this is by design.

## 3. Key Directories

| Path | Purpose |
|---|---|
| `src/` | All TypeScript source. |
| `src/server.ts` | Entry point + route definitions. |

## 4. Conventions

- **Code style:** ESLint + Prettier (defaults).
- **Naming:** camelCase for variables, kebab-case for files.
- **Tests:** vitest, colocated with source as `*.test.ts`.

## 5. Commands

| Command | Purpose |
|---|---|
| `npm run build` | TypeScript compile. |
| `npm run test` | Run vitest. |
| `npm run lint` | ESLint check. |
| `npm run dev` | Start the server with tsx. |

## 6. Common Workflows

### How to add a new route

1. Add the handler in `src/server.ts` next to the existing `/health` route.
2. Write a vitest test that calls `app.inject({ method, url })` and asserts the response.
3. Run `npm test`.

### How to fix a typical bug

1. Reproduce with a vitest test (failing).
2. Fix the code.
3. Confirm the test passes.

## 7. Anti-Patterns

- **Don't add Express middleware** — this repo uses Fastify, and the two have different lifecycle semantics. See `.claude/memory/decisions/use-fastify.md`.
- **Don't pass timestamps as strings** — see `.claude/memory/gotchas/timezone-mismatch.md`.

## 8. Tool Protocol  <!-- mcp:code-context | OPTIONAL -->

<!-- Only if you have the `code-context` MCP installed.
     If not, delete this entire section.
     If you change tool signatures here, update docs/tool-protocol.md too —
     the contract test will fail otherwise. -->

You have three tools from the `code-context` MCP server. Use them proactively:

- **`search_repo(query, top_k?, scope?)`** — call this BEFORE editing or reading
  large amounts of code. The query should describe the task in natural language.
  Example: search_repo("where do we validate user emails on signup")

- **`recent_changes(since?, paths?, max?)`** — call when the user mentions "recent",
  "the new", "what changed", or before suggesting changes that might conflict
  with in-flight work.

- **`get_summary(scope?, path?)`** — call ONCE at the start of an unfamiliar
  task to orient yourself. Don't call repeatedly.

Prefer these tools over Glob/Grep when the question is semantic
("how do we do X") rather than literal ("where is the string Y").

## 9. References & Memory

### External resources

- **Fastify docs:** https://fastify.dev/docs/latest/
- **TypeScript docs:** https://www.typescriptlang.org/docs/

### Dynamic memory

Per-repo memory lives in `.claude/memory/`. Start with `.claude/memory/MEMORY.md`.
