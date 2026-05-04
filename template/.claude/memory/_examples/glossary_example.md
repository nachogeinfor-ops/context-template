---
name: tenant
description: A customer organization with isolated data and billing
type: glossary
scope: global
created: 2026-04-08
---

# Tenant

A **tenant** is a customer organization. Every row in our database has a
`tenant_id` column. Cross-tenant queries are not allowed except in admin tools.

- A tenant has many **users**.
- A tenant has one **billing account**.
- A tenant has one or more **workspaces**.

Not the same as: **organization** (a marketing term we don't use in code) or
**account** (which means user account, not tenant).
