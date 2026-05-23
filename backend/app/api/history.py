from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.history import ReminderHistory
from app.schemas.history import HistoryOut
from app.services import auth_service

router = APIRouter(prefix="/api/history", tags=["history"])


def get_current_user(x_device_id: str = Header(...), db: Session = Depends(get_db)):
    user = auth_service.get_user_by_device(db, x_device_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@router.get("", response_model=list[HistoryOut])
def list_history(
    reminder_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    from app.models.reminder import Reminder
    q = db.query(ReminderHistory).join(Reminder).filter(Reminder.user_id == user.id)
    if reminder_id:
        q = q.filter(ReminderHistory.reminder_id == reminder_id)
    return q.order_by(ReminderHistory.triggered_at.desc()).offset(offset).limit(limit).all()
