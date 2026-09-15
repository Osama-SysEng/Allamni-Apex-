# Allamni-Apex Operational Hardening Runbook

Allamni-Apex now issues access and refresh tokens bound to server-side sessions. A refresh replay revokes its session. Personalized recommendations, learner memory, cognitive snapshots, and adaptive assessment updates require a versioned consent purpose. Institution reporting returns aggregates only for learners with that consent; it deliberately omits individual student risk rows.

| Control | Implementation | Required production action |
|---|---|---|
| Identity | Revocable session with refresh rotation | Replace the development memory adapter with PostgreSQL and revoke sessions on suspension or consent incident. |
| Consent | `personalized_learning` is purpose- and version-scoped | Present a real learner/guardian consent flow and persist revocation before using cognitive signals. |
| Assessment | User/key idempotency cache blocks double mastery updates | Persist `assessment_attempts` and enforce the unique database constraint. |
| Integration | idempotent outbox and blocked/deferred state | Use an approved worker and credentials; do not treat missing Odoo configuration as a successful sync. |
| Data | PostgreSQL migration `0002_operational_learning.sql` | Run as an independent migration job after backup and restore rehearsal. |
| Load | bounded `tools/load_probe.py` | Run only against local or approved staging target with a short-lived account. |

> The in-memory store remains a development/test adapter. It must not be treated as durable learning-record storage. Production activation requires repository implementations over the migration schema, managed backups, retention policy, and a tested consent-revocation path.
