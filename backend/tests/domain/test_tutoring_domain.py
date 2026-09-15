from domain.tutoring.contracts import TutoringSnapshot
from domain.tutoring.policies import requires_human_review
from domain.tutoring.service import display_label, is_terminal

def test_tutoring_contract_and_safeguards():
    snapshot = TutoringSnapshot(identifier="tutoring-001", status="ACTIVE", correlation_id="req-tutoring")
    assert display_label(snapshot) == "tutoring-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_human_review("PUBLISH_CONTENT")
    assert not requires_human_review("READ")
