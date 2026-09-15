from domain.institutions.contracts import InstitutionSnapshot
from domain.institutions.policies import requires_human_review
from domain.institutions.service import display_label, is_terminal

def test_institutions_contract_and_safeguards():
    snapshot = InstitutionSnapshot(identifier="institutions-001", status="ACTIVE", correlation_id="req-institutions")
    assert display_label(snapshot) == "institutions-001 · ACTIVE"
    assert is_terminal("COMPLETED")
    assert requires_human_review("PUBLISH_CONTENT")
    assert not requires_human_review("READ")
