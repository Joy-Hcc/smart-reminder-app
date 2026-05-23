from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    device_id: str
    api_key: Optional[str] = None
    api_provider: Optional[str] = None


class UserOut(BaseModel):
    id: str
    device_id: str
    api_provider: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
