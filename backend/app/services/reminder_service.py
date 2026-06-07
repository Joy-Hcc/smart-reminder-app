import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.reminder import Reminder, EventTrigger
from app.models.history import ReminderHistory
from app.schemas.reminder import ReminderCreate, ReminderUpdate

logger = logging.getLogger(__name__)


def create_reminder(db: Session, user_id: str, data: ReminderCreate) -> Reminder:
    reminder = Reminder(
        user_id=user_id,
        category_id=data.category_id,
        title=data.title,
        description=data.description,
        priority=data.priority,
        trigger_type=data.trigger_type,
        trigger_config=data.trigger_config,
        advance_notice=data.advance_notice,
        repeat_rule=data.repeat_rule,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    if data.trigger_type == "event" and data.trigger_config.get("event_type"):
        event = EventTrigger(
            reminder_id=reminder.id,
            event_type=data.trigger_config["event_type"],
            config=data.trigger_config.get("event_config", {}),
        )
        db.add(event)
        db.commit()

    return reminder


def update_reminder(db: Session, reminder: Reminder, data: ReminderUpdate) -> Reminder:
    if data.title is not None:
        reminder.title = data.title
    if data.description is not None:
        reminder.description = data.description
    if data.priority is not None:
        reminder.priority = data.priority
    if data.trigger_type is not None:
        reminder.trigger_type = data.trigger_type
    if data.trigger_config is not None:
        reminder.trigger_config = data.trigger_config
    if data.advance_notice is not None:
        reminder.advance_notice = data.advance_notice
    if data.repeat_rule is not None:
        reminder.repeat_rule = data.repeat_rule
    if data.status is not None:
        reminder.status = data.status
    if data.category_id is not None:
        reminder.category_id = data.category_id

    db.commit()
    db.refresh(reminder)
    return reminder


def delete_reminder(db: Session, reminder: Reminder):
    db.delete(reminder)
    db.commit()


def pause_reminder(db: Session, reminder: Reminder) -> Reminder:
    reminder.status = "paused"
    db.commit()
    db.refresh(reminder)
    return reminder


def resume_reminder(db: Session, reminder: Reminder) -> Reminder:
    reminder.status = "active"
    db.commit()
    db.refresh(reminder)
    return reminder


def get_due_reminders(db: Session) -> list[Reminder]:
    now = datetime.now(timezone.utc)
    # 分批处理，避免一次性加载所有提醒到内存
    batch_size = 100
    offset = 0
    due = []

    while True:
        reminders = db.query(Reminder).filter(
            Reminder.status == "active",
            Reminder.trigger_type == "scheduled"
        ).offset(offset).limit(batch_size).all()

        if not reminders:
            break

        # 预查询已触发的非重复提醒 ID（避免 N+1 查询）
        non_repeat_ids = [r.id for r in reminders if not r.repeat_rule]
        triggered_ids: set[str] = set()
        if non_repeat_ids:
            triggered_ids = {
                row[0] for row in db.query(ReminderHistory.reminder_id)
                .filter(
                    ReminderHistory.reminder_id.in_(non_repeat_ids),
                    ReminderHistory.trigger_type == "scheduled"
                ).distinct().all()
            }

        for r in reminders:
            try:
                cfg = r.trigger_config or {}
                target = datetime.fromisoformat(cfg.get("datetime", ""))
                if target.tzinfo is None:
                    target = target.replace(tzinfo=timezone.utc)
                advance = timedelta(minutes=r.advance_notice)

                # 跳过已触发的非重复提醒
                if not r.repeat_rule and r.id in triggered_ids:
                    continue

                if target - advance <= now:
                    due.append(r)
            except Exception:
                logger.warning("Failed to parse trigger config for reminder %s", r.id, exc_info=True)
                continue

        offset += batch_size

    return due


def record_history(db: Session, reminder_id: str, trigger_type: str, content: str | None = None) -> ReminderHistory:
    hist = ReminderHistory(reminder_id=reminder_id, trigger_type=trigger_type, content=content)
    db.add(hist)
    db.commit()
    db.refresh(hist)
    return hist
