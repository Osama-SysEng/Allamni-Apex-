from dataclasses import dataclass

@dataclass(frozen=True)
class CreateTutoring:
    actor_id: str
    correlation_id: str
    reason: str | None = None

@dataclass(frozen=True)
class ReviewTutoring:
    identifier: str
    actor_id: str
    decision: str
    reason: str
