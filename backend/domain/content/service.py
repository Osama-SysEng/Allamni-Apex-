from .contracts import ContentSnapshot

def display_label(snapshot: ContentSnapshot) -> str:
    return f"{snapshot.identifier} · {snapshot.status}"

def is_terminal(status: str) -> bool:
    return status.upper() in {"ARCHIVED", "COMPLETED", "REJECTED", "WITHDRAWN"}
