from .contracts import CurriculumSnapshot

def display_label(snapshot: CurriculumSnapshot) -> str:
    return f"{snapshot.identifier} · {snapshot.status}"

def is_terminal(status: str) -> bool:
    return status.upper() in {"ARCHIVED", "COMPLETED", "REJECTED", "WITHDRAWN"}
