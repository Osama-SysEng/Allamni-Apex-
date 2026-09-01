from typing import Any

HIGH_IMPACT_ACTIONS = {"change_grade", "delete_student", "modify_billing", "publish_policy", "bulk_enrollment"}

def authorize_action(role: str, action: str, target_owner: str | None, actor: str) -> dict[str, Any]:
    if role == "admin": return {"allowed": True, "requires_approval": action in HIGH_IMPACT_ACTIONS}
    if role == "institution_manager" and action not in HIGH_IMPACT_ACTIONS: return {"allowed": True, "requires_approval": False}
    if role == "student" and target_owner == actor and action in {"read_profile", "submit_assessment", "start_resource"}:
        return {"allowed": True, "requires_approval": False}
    return {"allowed": False, "requires_approval": False}
