from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass
class MemoryRecord:
    subject_id: str
    kind: str
    content: dict[str, Any]
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class LearningMemory:
    def __init__(self): self._items: list[MemoryRecord] = []
    def remember(self, subject_id: str, kind: str, content: dict[str, Any]) -> MemoryRecord:
        item=MemoryRecord(subject_id,kind,content); self._items.append(item); return item
    def recall(self, subject_id: str, kind: str | None = None, limit: int = 20) -> list[dict[str, Any]]:
        items=[x for x in self._items if x.subject_id==subject_id and (kind is None or x.kind==kind)]
        return [x.__dict__ for x in items[-limit:]]
