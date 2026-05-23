import logging
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import httpx
from app.database import SessionLocal
from app.services import reminder_service, email_service
from app.models.reminder import Reminder, EventTrigger
from app.models.user import User

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def check_scheduled_reminders():
    db = SessionLocal()
    try:
        due = reminder_service.get_due_reminders(db)
        for r in due:
            try:
                hist = reminder_service.record_history(db, r.id, "scheduled", r.description)

                # Send email if user has an email address
                user = db.query(User).filter(User.id == r.user_id).first()
                if user and user.email:
                    from app.schemas.reminder import ReminderOut
                    cat_name = ""
                    if r.category:
                        cat_name = r.category.name
                    success, status = email_service.send_reminder_email(
                        to_email=user.email,
                        title=r.title,
                        category=cat_name,
                        description=r.description,
                        priority=r.priority,
                    )
                    hist.email_sent = success
                    hist.email_status = status
                    db.commit()

                if not r.repeat_rule:
                    r.status = "triggered"
                    db.commit()
                logger.info("Triggered reminder: %s (%s)", r.title, r.id)
            except Exception:
                logger.error("Failed to process reminder %s", r.id, exc_info=True)
                db.rollback()
    except Exception:
        logger.error("Scheduler check failed", exc_info=True)
    finally:
        db.close()


def check_event_triggers():
    from app.config import get_settings
    settings = get_settings()
    if not settings.qweather_key:
        return

    db = SessionLocal()
    try:
        triggers = db.query(EventTrigger).all()
        for et in triggers:
            try:
                if et.event_type == "weather":
                    _check_weather_trigger(db, et, settings.qweather_key)
            except Exception:
                logger.error("Failed to check event trigger %s", et.id, exc_info=True)
                db.rollback()
    except Exception:
        logger.error("Event trigger check failed", exc_info=True)
    finally:
        db.close()


def _check_weather_trigger(db, et: EventTrigger, api_key: str):
    config = et.config or {}
    city = config.get("city")
    condition_type = config.get("condition_type", "temperature")
    condition_op = config.get("condition_op", ">")
    condition_value = config.get("condition_value")

    if not city or condition_value is None:
        return

    resp = httpx.get(
        "https://devapi.qweather.com/v7/weather/now",
        params={"location": city, "key": api_key},
        timeout=10,
    )
    data = resp.json()
    if data.get("code") != "200":
        logger.warning("QWeather API error for city %s: %s", city, data.get("code"))
        return

    now_weather = data.get("now", {})
    actual_value = _extract_weather_value(now_weather, condition_type)
    if actual_value is None:
        return

    triggered = _compare_value(actual_value, condition_op, condition_value)

    # Update last_checked
    et.last_checked = datetime.now(timezone.utc)
    db.commit()

    if triggered:
        reminder = et.reminder
        if reminder and reminder.status == "active":
            hist = reminder_service.record_history(
                db, reminder.id, "event",
                f"Weather condition met: {condition_type} {condition_op} {condition_value} (actual: {actual_value})"
            )
            # Send email
            user = db.query(User).filter(User.id == reminder.user_id).first()
            if user and user.email:
                cat_name = reminder.category.name if reminder.category else ""
                success, status = email_service.send_reminder_email(
                    to_email=user.email,
                    title=reminder.title,
                    category=cat_name,
                    description=f"{condition_type} condition met in {city}: {actual_value}",
                    priority=reminder.priority,
                )
                hist.email_sent = success
                hist.email_status = status
            et.last_triggered = datetime.now(timezone.utc)
            if not reminder.repeat_rule:
                reminder.status = "triggered"
            db.commit()
            logger.info("Event trigger fired: %s for reminder %s", et.id, reminder.id)


def _extract_weather_value(now_weather: dict, condition_type: str) -> float | None:
    mapping = {
        "temperature": "temp",
        "humidity": "humidity",
        "wind_speed": "windSpeed",
        "wind_scale": "windScale",
    }
    raw = now_weather.get(mapping.get(condition_type, condition_type))
    if raw is None:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None


def _compare_value(actual: float, op: str, target: float) -> bool:
    if op == ">":
        return actual > target
    elif op == ">=":
        return actual >= target
    elif op == "<":
        return actual < target
    elif op == "<=":
        return actual <= target
    elif op == "==":
        return actual == target
    return False


def start_scheduler():
    scheduler.add_job(
        check_scheduled_reminders,
        trigger=IntervalTrigger(minutes=1),
        id="check_reminders",
        replace_existing=True,
    )
    scheduler.add_job(
        check_event_triggers,
        trigger=IntervalTrigger(minutes=5),
        id="check_event_triggers",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started")


def shutdown_scheduler():
    scheduler.shutdown()
    logger.info("Scheduler stopped")
