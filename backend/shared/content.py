from __future__ import annotations
from typing import Any
from shared.models import LearningProfile, Resource
from shared.intelligence import choose_next_skill


def lesson_blueprint(profile: LearningProfile, resources: list[Resource]) -> dict[str, Any]:
    skill = choose_next_skill(profile)
    if not skill:
        return {"status": "mastery", "message": "لا توجد فجوة حرجة حاليًا."}
    matches = [r for r in resources if skill.code in r.skills]
    matches.sort(key=lambda r: (r.quality_score, -((r.duration_minutes or 999) / 999)), reverse=True)
    formats = profile.learning_preferences.content_format or ["text"]
    return {
        "skill": skill.model_dump(),
        "sequence": [
            {"type": "warmup", "purpose": "activate_prior_knowledge"},
            {"type": "mind_map", "purpose": "connect_concepts"},
            {"type": "visual_explanation", "purpose": "concrete_explanation", "formats": formats},
            {"type": "interactive_game", "purpose": "retrieval_practice"},
            {"type": "real_life_question", "purpose": "transfer"},
            {"type": "micro_assessment", "purpose": "mastery_update"},
        ],
        "resources": [r.model_dump() for r in matches[:5]],
        "validation": {"required": ["source_quality", "age_fit", "language_fit", "skill_alignment"]},
    }
