---
name: timezone-mismatch
description: Comparing local-time strings to TIMESTAMPTZ values silently drops rows around midnight
type: gotcha
scope: global
created: 2026-04-10
---

# Timezone mismatch in handlers

**Trap:** any DB column declared `TIMESTAMP WITH TIME ZONE` is normalized to UTC.
Comparing such a value to a local-time string (e.g. via `req.query.from = "2026-04-10"`) silently drops or duplicates rows around midnight.

**Fix:** always parse `req.query.*` date inputs as ISO 8601 with offset, or assume UTC.
The helper in `src/lib/time.ts` (when added) enforces this.

**Why this is here:** we've hit it twice, both in production. Documented to avoid a third.
