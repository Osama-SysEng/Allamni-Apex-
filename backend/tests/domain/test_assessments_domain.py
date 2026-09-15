from domain.assessments.contracts import AssessmentSnapshot
from domain.assessments.policies import requires_human_review
from domain.assessments.service import display_label, is_terminal

def test_assessments_contract_and_safeguards():
    snapshot = AssessmentSnapshot(identifier="assessments-001", status="ACTIVE", correlation_id="req-assessments")
    assert display_label(snapshot) == "assessments-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_human_review("PUBLISH_CONTENT")
    assert not requires_human_review("READ")
