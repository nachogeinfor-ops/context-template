---
name: tenant
description: A customer organization with isolated data and billing
type: glossary
scope: global
created: 2026-04-05
---

# Tenant

A **tenant** is a customer organization. Every domain row in the database has a `tenant_id` column.

- A tenant has many **users**.
- A tenant has one **billing account**.

Not the same as: **organization** (a marketing word we don't use in code).
