---
name: add-a-new-api-endpoint
description: Step-by-step recipe for adding an HTTP endpoint to the API service
type: playbook
scope: api
created: 2026-04-15
---

# Add a new API endpoint

1. **Define the route schema** in `api/schemas/<feature>.py` (Pydantic model).
2. **Add the handler** in `api/routes/<feature>.py`. Inject dependencies via
   FastAPI's `Depends`.
3. **Register the route** in `api/app.py` under the appropriate prefix.
4. **Write the test** in `tests/api/test_<feature>.py`. Use `TestClient`
   and at least one happy-path + one auth-failure case.
5. **Run** `make test-api` locally.
6. **Update** `docs/api/openapi.yaml` if the schema changed (the CI lint
   will fail otherwise).

Most-common pitfalls: forgetting step 6 (CI failure), or forgetting to
add the route to the router (404 in tests).
