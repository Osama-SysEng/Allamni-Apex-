# Managed Learning Data Contract

The application currently keeps a development-mode in-memory implementation for fast local tests. Production state must move behind the PostgreSQL schema and repository interfaces, with Redis used only for cache, rate limits, or ephemeral fan-out. The migration `infrastructure/postgres/migrations/0002_operational_learning.sql` is deliberately separate from startup so schema change, backup, and rollback have independent operational approval.

| Record | Invariant | Operational rule |
|---|---|---|
| Session | A token must map to an unrevoked, unexpired server session. | Revoke sessions on logout, suspected refresh replay, or account suspension. |
| Consent | Consent is scoped by learner and processing purpose/version. | Personalized recommendations, learner memory, and cognitive risk signals require explicit consent. |
| Assessment attempt | `(student_id, idempotency_key)` is unique. | A mobile retry returns the first recorded result and must not update mastery twice. |
| Audit event | Sensitive changes have actor/action/entity evidence. | Retain according to education privacy policy; never write raw passwords or access tokens. |
| Integration outbox | Each idempotency key appears once. | Background workers retry only retryable failures; use dead-letter review for terminal failures. |

> This migration establishes the durable production data contract. It does not itself migrate development memory state or grant consent on a learner's behalf. Staging must validate restore, query plans, retention, and consent revocation before production activation.
