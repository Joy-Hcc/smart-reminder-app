from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HistoryOut(BaseModel):
    id: str
    reminder_id: str
    triggered_at: datetime
    trigger_type: Optional[str] = None
    content: Optional[str] = None
    email_sent: bool
    email_status: Optional[str] = None

    class Config:
        from_attributes = True
