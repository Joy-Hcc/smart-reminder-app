import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderOut
from app.schemas.pagination import PaginatedResponse
from app.services import reminder_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/reminders", tags=["reminders"])


@router.get("", response_model=PaginatedResponse[ReminderOut])
def list_reminders(
    category_id: str | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Reminder).filter(Reminder.user_id == user.id)
    if category_id:
        q = q.filter(Reminder.category_id == category_id)
    if status:
        q = q.filter(Reminder.status == status)
    if search:
        q = q.filter(Reminder.title.contains(search))

    total = q.count()
    pages = math.ceil(total / page_size) if total > 0 else 1
    items = q.order_by(Reminder.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=pages,
    )


@router.post("", response_model=ReminderOut)
def create_reminder(data: ReminderCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    return reminder_service.create_reminder(db, user.id, data)


@router.get("/{reminder_id}", response_model=ReminderOut)
def get_reminder(reminder_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return r


@router.put("/{reminder_id}", response_model=ReminderOut)
def update_reminder(reminder_id: str, data: ReminderUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return reminder_service.update_reminder(db, r, data)


@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reminder not found")
    reminder_service.delete_reminder(db, r)
    return {"ok": True}


@router.post("/{reminder_id}/pause")
def pause_reminder(reminder_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reminder not found")
    r.status = "paused"
    db.commit()
    return {"ok": True}


@router.post("/{reminder_id}/resume")
def resume_reminder(reminder_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reminder not found")
    r.status = "active"
    db.commit()
    return {"ok": True}
