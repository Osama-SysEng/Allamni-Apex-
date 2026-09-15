from domain.content.contracts import ContentSnapshot
from domain.content.policies import requires_human_review
from domain.content.service import display_label, is_terminal

def test_content_contract_and_safeguards():
    snapshot = ContentSnapshot(identifier="content-001", status="ACTIVE", correlation_id="req-content")
    assert display_label(snapshot) == "content-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_human_review("PUBLISH_CONTENT")
    assert not requires_human_review("READ")
