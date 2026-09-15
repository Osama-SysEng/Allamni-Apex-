from .contracts import LearnerSnapshot

def display_label(snapshot: LearnerSnapshot) -> str:
    return f"{snapshot.identifier} · {snapshot.status}"

def is_terminal(status: str) -> bool:
    return status.upper() in {"ARCHIVED", "COMPLETED", "REJECTED", "WITHDRAWN"}
