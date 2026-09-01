from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any
from uuid import uuid4

from shared.models import LearningProfile, Skill


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


def cognitive_snapshot(profile: LearningProfile) -> dict[str, Any]:
    skills = profile.skills
    if not skills:
        return {"mastery": 0.0, "confidence": 0.0, "gap": 0.0, "stability": 0.0, "signals": []}
    mastery = sum(s.level for s in skills) / len(skills)
    confidence = sum(s.confidence for s in skills) / len(skills)
    gap = sum(max(0, s.target - s.level) for s in skills) / len(skills)
    stability = sum(1 - abs(s.level - s.confidence) for s in skills) / len(skills)
    signals = []
    if confidence < 0.45: signals.append("low_confidence")
    if gap > 0.35: signals.append("large_learning_gap")
    if stability < 0.55: signals.append("uncertain_mastery")
    return {"mastery": round(mastery, 4), "confidence": round(confidence, 4), "gap": round(gap, 4), "stability": round(stability, 4), "signals": signals}


def risk_score(profile: LearningProfile) -> dict[str, Any]:
    snap = cognitive_snapshot(profile)
    score = clamp(0.45 * snap["gap"] + 0.35 * (1 - snap["confidence"]) + 0.20 * (1 - snap["stability"]))
    level = "critical" if score >= .70 else "high" if score >= .50 else "medium" if score >= .30 else "low"
    return {"score": round(score, 4), "level": level, "signals": snap["signals"]}


def adaptive_difficulty(current: float, performance: float, confidence: float) -> float:
    # Deterministic control loop: good performance raises difficulty; weak performance lowers it.
    delta = (performance - 0.65) * 0.35 + (confidence - 0.5) * 0.10
    return round(clamp(current + delta, 0.05, 0.95), 4)


def choose_next_skill(profile: LearningProfile) -> Skill | None:
    gaps = [s for s in profile.skills if s.target > s.level + .02]
    if not gaps:
        return None
    return max(gaps, key=lambda s: (s.target - s.level) * s.importance * (1 + (1 - s.confidence)))


@dataclass
class AgentDecision:
    agent: str
    action: str
    confidence: float
    evidence: list[str]
    requires_approval: bool = False

    def dump(self) -> dict[str, Any]:
        return self.__dict__.copy()


class StudentAgent:
    name = "student_agent"
    def run(self, profile: LearningProfile) -> AgentDecision:
        skill = choose_next_skill(profile)
        if not skill:
            return AgentDecision(self.name, "advance_to_mastery", .92, ["all_current_targets_reached"])
        return AgentDecision(self.name, "focus_skill", .90, [skill.code, f"gap={skill.target-skill.level:.3f}"])


class AssessmentAgent:
    name = "assessment_agent"
    def run(self, profile: LearningProfile, performance: float, difficulty: float) -> AgentDecision:
        nxt = adaptive_difficulty(difficulty, performance, sum(s.confidence for s in profile.skills) / max(1, len(profile.skills)))
        return AgentDecision(self.name, "retune_assessment", .88, [f"performance={performance:.3f}", f"next_difficulty={nxt:.3f}"])


class TutorAgent:
    name = "tutor_agent"
    def run(self, profile: LearningProfile) -> AgentDecision:
        skill = choose_next_skill(profile)
        return AgentDecision(self.name, "teach_with_adaptive_content" if skill else "enrichment", .86,
                             [skill.code if skill else "mastery_complete", *profile.learning_preferences.content_format])


class ContentAgent:
    name = "content_agent"
    def run(self, profile: LearningProfile) -> AgentDecision:
        return AgentDecision(self.name, "compose_multimodal_lesson", .84,
                             ["mind_map", "interactive_game", "visual_explanation", "validated_resource"])


class InstitutionAgent:
    name = "institution_agent"
    def run(self, profile: LearningProfile) -> AgentDecision:
        risk = risk_score(profile)
        return AgentDecision(self.name, "notify_intervention_team" if risk["level"] in {"high", "critical"} else "monitor",
                             .82, risk["signals"], requires_approval=risk["level"] == "critical")


class AgentOrchestrator:
    def __init__(self):
        self.agents = [StudentAgent(), TutorAgent(), ContentAgent(), InstitutionAgent()]

    def run(self, profile: LearningProfile) -> dict[str, Any]:
        decisions = [a.run(profile).dump() for a in self.agents]
        return {"trace_id": str(uuid4()), "timestamp": datetime.now(timezone.utc).isoformat(), "decisions": decisions}


def idempotency_key(event_type: str, subject_id: str, payload: dict[str, Any]) -> str:
    raw = f"{event_type}:{subject_id}:{sorted(payload.items())}".encode()
    return sha256(raw).hexdigest()
