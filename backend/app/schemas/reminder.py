from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReminderCreate(BaseModel):
    application_id: int
    reminder_type: str = "follow_up"
    remind_at: datetime
    note: Optional[str] = None

class ReminderResponse(BaseModel):
    id: int
    application_id: int
    reminder_type: str
    remind_at: datetime
    is_sent: bool
    note: Optional[str]

    class Config:
        from_attributes = True