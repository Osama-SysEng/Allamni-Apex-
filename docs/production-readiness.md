# Allamni Production Readiness Contract

## Core loop
`Observe -> Profile -> Assess -> Reason -> Plan -> Teach -> Measure -> Adapt -> Act -> Verify -> Learn`

## Safety boundary
- LLM output is advisory by default.
- Deterministic mastery, scoring, authorization, idempotency and state transitions remain outside LLM control.
- High-impact institutional actions require explicit approval.
- Student-owned operations are owner-scoped.

## Agent layer
- Student Agent: next learning focus.
- Tutor Agent: adaptive teaching mode.
- Content Agent: multimodal lesson blueprint.
- Institution Agent: intervention/monitoring signal.
- Assessment Agent: difficulty control loop.

## Memory
Every assessment, content plan and agent trace can be retained as structured learning memory. Memory is subject-scoped and can be replaced by PostgreSQL/Qdrant adapters without changing engine contracts.

## Content
Content planning supports mind maps, interactive games, visual explanations, real-life questions and micro-assessments. External media must pass source quality, age-fit, language-fit and skill-alignment validation before publication.

## Integrations
Odoo uses an outbox/event model. Production connector must provide retries, idempotency, reconciliation and dead-letter handling. Credentials are environment-only; no secrets are committed.

## Remaining environment work
Real LLM credentials, real Odoo endpoint, production PostgreSQL repositories, object storage and deployment secrets depend on target infrastructure. Development mode remains deterministic rather than pretending these integrations are live.
