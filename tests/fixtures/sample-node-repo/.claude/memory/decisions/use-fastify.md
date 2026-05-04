---
name: use-fastify
description: Why we chose Fastify over Express for the HTTP layer
type: decision
scope: global
created: 2026-04-01
---

# Use Fastify, not Express

**Decision:** All HTTP services use Fastify 4+.

**Why:**
- Fastify is ~2x faster than Express in synthetic benchmarks and ~30% in our load tests.
- Built-in JSON Schema validation removes the need for a separate validator library.
- Plugins have an explicit lifecycle (encapsulation), which Express middleware lacks.

**Consequences:**
- Don't import `express` or any `express-*` middleware. Use Fastify equivalents.
- Schemas live next to route handlers as JSON Schema, not Joi/Zod.

**Revisit if:** we need a feature only available in the Express ecosystem and unavailable as a Fastify plugin.
