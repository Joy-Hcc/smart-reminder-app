import json
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderOut
from app.services import auth_service, reminder_service

router = APIRouter(prefix="/api/reminders", tags=["reminders"])


def get_current_user(x_device_id: str = Header(...), db: Session = Depends(get_db)):
    user = auth_service.get_user_by_device(db, x_device_id)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


@router.get("", response_model=list[ReminderOut])
def list_reminders(
    category_id: str | None = Query(None),
    status: str | None = Query(None),
    search: str | None = Query(None),
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
    rows = q.order_by(Reminder.created_at.desc()).all()
    for r in rows:
        r.trigger_config = json.loads(r.trigger_config)
    return rows


@router.post("", response_model=ReminderOut)
def create_reminder(data: ReminderCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = reminder_service.create_reminder(db, user.id, data)
    r.trigger_config = json.loads(r.trigger_config)
    return r


@router.get("/{reminder_id}", response_model=ReminderOut)
def get_reminder(reminder_id: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reminder not found")
    r.trigger_config = json.loads(r.trigger_config)
    return r


@router.put("/{reminder_id}", response_model=ReminderOut)
def update_reminder(reminder_id: str, data: ReminderUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.query(Reminder).filter(Reminder.id == reminder_id, Reminder.user_id == user.id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reminder not found")
    r = reminder_service.update_reminder(db, r, data)
    r.trigger_config = json.loads(r.trigger_config)
    return r


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
