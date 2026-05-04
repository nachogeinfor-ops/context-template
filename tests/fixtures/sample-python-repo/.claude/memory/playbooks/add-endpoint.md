---
name: add-endpoint
description: Step-by-step recipe for adding a FastAPI endpoint
type: playbook
scope: api
created: 2026-04-15
---

# Add a new API endpoint

1. **Define request/response schemas** in `src/api/schemas/<feature>.py` as Pydantic models.
2. **Add the route handler** in `src/api/routes/<feature>.py`. Type the request body using your schema.
3. **Register the router** in `src/api/main.py` (`app.include_router(...)`).
4. **Write the test** in `tests/api/test_<feature>.py` using FastAPI's `TestClient`. At minimum: one happy-path case + one validation-failure case.
5. **Run** `pytest tests/api/test_<feature>.py -v`.
6. **Run** `ruff check src` to catch style issues.

Most-common pitfall: forgetting step 3, which produces a 404 in tests with no obvious cause.
