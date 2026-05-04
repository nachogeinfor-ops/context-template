---
name: use-postgres-over-mysql
description: Why we chose Postgres for the primary store
type: decision
scope: global
created: 2026-04-12
---

# Use Postgres over MySQL

**Decision:** All new services use PostgreSQL 16.

**Why:**
- We already operate Postgres in production and have monitoring/runbooks.
- We need `JSONB` and partial indexes; MySQL's JSON support is weaker.
- Logical replication is more mature on Postgres for our event-sourcing needs.

**Consequences:**
- Anyone joining writes Postgres SQL by default; no MySQL examples in this repo.
- ORM choice is constrained to drivers with strong Postgres support.

**Revisit if:** we adopt a managed MySQL with feature parity, or our access
patterns become heavily key-value (in which case we'd consider DynamoDB).
