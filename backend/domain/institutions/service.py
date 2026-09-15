from .contracts import InstitutionSnapshot

def display_label(snapshot: InstitutionSnapshot) -> str:
    return f"{snapshot.identifier} · {snapshot.status}"

def is_terminal(status: str) -> bool:
    return status.upper() in {"ARCHIVED", "COMPLETED", "REJECTED", "WITHDRAWN"}
