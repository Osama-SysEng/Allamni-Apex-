from dataclasses import dataclass

@dataclass(frozen=True)
class CreateAssessment:
    actor_id: str
    correlation_id: str
    reason: str | None = None

@dataclass(frozen=True)
class ReviewAssessment:
    identifier: str
    actor_id: str
    decision: str
    reason: str
