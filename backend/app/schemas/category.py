from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None


class CategoryOut(BaseModel):
    id: str
    user_id: str
    name: str
    parent_id: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int
    created_at: datetime
    children: List["CategoryOut"] = []

    class Config:
        from_attributes = True


CategoryOut.model_rebuild()
