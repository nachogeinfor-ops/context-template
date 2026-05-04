---
name: timezone-mismatch-in-reports
description: Reports compare UTC timestamps to local-time strings — silent truncation
type: gotcha
scope: reports
created: 2026-04-20
---

# Timezone mismatch in `reports/daily.py`

**Trap:** the `created_at` column is `TIMESTAMP WITH TIME ZONE` (stored as UTC),
but the daily-report query filters with a string literal in the system's local
time. On a UTC server this looks fine; in a non-UTC region it silently drops
or duplicates rows around midnight.

**Fix:** always pass timezone-aware `datetime` objects, never strings. The
query helper in `lib/db/time.py` enforces this.

**Why this is here:** we hit it twice (Q1 2026, then again after the report
rewrite). Documented so the third time doesn't happen.
