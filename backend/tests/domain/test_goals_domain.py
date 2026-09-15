from domain.goals.contracts import GoalSnapshot
from domain.goals.policies import requires_human_review
from domain.goals.service import display_label, is_terminal

def test_goals_contract_and_safeguards():
    snapshot = GoalSnapshot(identifier="goals-001", status="ACTIVE", correlation_id="req-goals")
    assert display_label(snapshot) == "goals-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_human_review("PUBLISH_CONTENT")
    assert not requires_human_review("READ")
