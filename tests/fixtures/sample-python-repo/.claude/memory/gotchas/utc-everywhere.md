---
name: utc-everywhere
description: Naive datetimes leak local timezone — store and pass timezone-aware UTC
type: gotcha
scope: global
created: 2026-04-10
---

# UTC everywhere; no naive datetimes

**Trap:** `datetime.now()` returns a naive datetime in the system's local timezone.
If this leaks into the database (which expects UTC) or into a comparison with a UTC value, results are subtly wrong.

**Fix:** always use `datetime.now(timezone.utc)` and require timezone-aware datetimes at function boundaries.
A `mypy` plugin would catch this at type-check time; for now we rely on review and tests.

**Why this is here:** we've hit this multiple times. Documented to make the pattern stick.
