from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from shared.intelligence import idempotency_key

@dataclass
class DomainEvent:
    id: str
    type: str
    subject_id: str
    payload: dict[str, Any]
    key: str
    created_at: str
    status: str = "pending"

class EventBus:
    def __init__(self, store): self.store=store
    def publish(self, event_type: str, subject_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        key=idempotency_key(event_type,subject_id,payload)
        if any(e.get("key")==key for e in self.store.events): return next(e for e in self.store.events if e.get("key")==key)
        event=DomainEvent(str(uuid4()),event_type,subject_id,payload,key,datetime.now(timezone.utc).isoformat()).__dict__
        self.store.events.append(event); return event
