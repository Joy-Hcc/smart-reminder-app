from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any


class ReminderCreate(BaseModel):
    category_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    trigger_type: str
    trigger_config: Dict[str, Any]
    advance_notice: int = 0
    repeat_rule: Optional[str] = None


class ReminderUpdate(BaseModel):
    category_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    trigger_type: Optional[str] = None
    trigger_config: Optional[Dict[str, Any]] = None
    advance_notice: Optional[int] = None
    repeat_rule: Optional[str] = None
    status: Optional[str] = None


class ReminderOut(BaseModel):
    id: str
    user_id: str
    category_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    priority: str
    trigger_type: str
    trigger_config: Dict[str, Any]
    advance_notice: int
    repeat_rule: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
