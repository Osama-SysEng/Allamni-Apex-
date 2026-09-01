from datetime import datetime
from pydantic import BaseModel, Field

class GoalSnapshot(BaseModel):
    identifier: str = Field(min_length=1, max_length=150)
    status: str = Field(min_length=1, max_length=40)
    owner_id: str | None = None
    correlation_id: str | None = None
    updated_at: datetime | None = None

class GoalPage(BaseModel):
    items: list[GoalSnapshot] = Field(default_factory=list)
    next_cursor: str | None = None
