import math
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.history import ReminderHistory
from app.schemas.history import HistoryOut
from app.schemas.pagination import PaginatedResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=PaginatedResponse[HistoryOut])
def list_history(
    reminder_id: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.models.reminder import Reminder
    q = db.query(ReminderHistory).join(Reminder).filter(Reminder.user_id == user.id)
    if reminder_id:
        q = q.filter(ReminderHistory.reminder_id == reminder_id)

    total = q.count()
    pages = math.ceil(total / page_size) if total > 0 else 1
    items = q.order_by(ReminderHistory.triggered_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )
