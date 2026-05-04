---
name: use-fastapi
description: Why we chose FastAPI over Flask
type: decision
scope: global
created: 2026-04-01
---

# Use FastAPI, not Flask

**Decision:** All HTTP services use FastAPI 0.110+.

**Why:**
- Pydantic-based request/response validation removes a whole class of bugs.
- Native async support — Flask's async story is bolted on.
- Auto-generated OpenAPI is good enough that we don't maintain a separate spec.

**Consequences:**
- Don't import `flask` or `flask-*` extensions. Use FastAPI equivalents.
- All request bodies are Pydantic models, not dicts.

**Revisit if:** Pydantic 3 changes the validation contract in a way we can't accommodate, or if we need a feature only available in the Flask ecosystem.
