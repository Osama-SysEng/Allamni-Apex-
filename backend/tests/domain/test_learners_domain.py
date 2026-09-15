from domain.learners.contracts import LearnerSnapshot
from domain.learners.policies import requires_human_review
from domain.learners.service import display_label, is_terminal

def test_learners_contract_and_safeguards():
    snapshot = LearnerSnapshot(identifier="learners-001", status="ACTIVE", correlation_id="req-learners")
    assert display_label(snapshot) == "learners-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_human_review("PUBLISH_CONTENT")
    assert not requires_human_review("READ")
