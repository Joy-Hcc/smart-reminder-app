import json
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.database import SessionLocal
from app.services import reminder_service, email_service

scheduler = BackgroundScheduler()


def check_scheduled_reminders():
    db = SessionLocal()
    try:
        due = reminder_service.get_due_reminders(db)
        for r in due:
            # TODO: send actual email when user email is stored
            # For now just record history
            hist = reminder_service.record_history(db, r.id, "scheduled", r.description)
            # Mark as triggered or keep for repeat rules
            if not r.repeat_rule:
                r.status = "triggered"
                db.commit()
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        check_scheduled_reminders,
        trigger=IntervalTrigger(minutes=1),
        id="check_reminders",
        replace_existing=True,
    )
    scheduler.start()


def shutdown_scheduler():
    scheduler.shutdown()
