from domain.curriculum.contracts import CurriculumSnapshot
from domain.curriculum.policies import requires_human_review
from domain.curriculum.service import display_label, is_terminal

def test_curriculum_contract_and_safeguards():
    snapshot = CurriculumSnapshot(identifier="curriculum-001", status="ACTIVE", correlation_id="req-curriculum")
    assert display_label(snapshot) == "curriculum-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_human_review("PUBLISH_CONTENT")
    assert not requires_human_review("READ")
