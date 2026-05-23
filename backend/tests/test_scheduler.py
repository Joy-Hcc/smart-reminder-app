"""Scheduler and history tests."""

import pytest
from datetime import datetime, timedelta, timezone


class TestGetDueReminders:
    def test_get_due_reminders(self, db_session):
        """Reminders with past datetime are considered due."""
        from app.models.user import User
        from app.models.reminder import Reminder
        from app.services.reminder_service import get_due_reminders

        user = User(device_id="scheduler-test-user")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        past = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        future = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()

        due_reminder = Reminder(
            user_id=user.id,
            title="Due Task",
            trigger_type="scheduled",
            trigger_config={"datetime": past},
            status="active",
        )
        not_due_reminder = Reminder(
            user_id=user.id,
            title="Not Due Yet",
            trigger_type="scheduled",
            trigger_config={"datetime": future},
            status="active",
        )
        paused_reminder = Reminder(
            user_id=user.id,
            title="Paused Due",
            trigger_type="scheduled",
            trigger_config={"datetime": past},
            status="paused",
        )
        db_session.add_all([due_reminder, not_due_reminder, paused_reminder])
        db_session.commit()

        due = get_due_reminders(db_session)
        assert len(due) == 1
        assert due[0].title == "Due Task"

    def test_get_due_with_advance_notice(self, db_session):
        """Advance notice shifts the effective trigger time earlier."""
        from app.models.user import User
        from app.models.reminder import Reminder
        from app.services.reminder_service import get_due_reminders

        user = User(device_id="advance-test-user")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        now = datetime.now(timezone.utc)
        # 5 minutes from now, but 30 minutes advance notice -> effective time is 25 min ago
        trigger_time = (now + timedelta(minutes=5)).isoformat()

        reminder = Reminder(
            user_id=user.id,
            title="Advance Notice Task",
            trigger_type="scheduled",
            trigger_config={"datetime": trigger_time},
            advance_notice=30,
            status="active",
        )
        db_session.add(reminder)
        db_session.commit()

        due = get_due_reminders(db_session)
        assert len(due) == 1

    def test_get_due_invalid_config(self, db_session):
        """Reminders with invalid trigger_config are skipped."""
        from app.models.user import User
        from app.models.reminder import Reminder
        from app.services.reminder_service import get_due_reminders

        user = User(device_id="invalid-config-user")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        bad_reminder = Reminder(
            user_id=user.id,
            title="Bad Config",
            trigger_type="scheduled",
            trigger_config={"datetime": "not-a-date"},
            status="active",
        )
        db_session.add(bad_reminder)
        db_session.commit()

        due = get_due_reminders(db_session)
        assert len(due) == 0


class TestRecordHistory:
    def test_record_history(self, db_session):
        """Record history creates a ReminderHistory entry."""
        from app.models.user import User
        from app.models.reminder import Reminder
        from app.services.reminder_service import record_history

        user = User(device_id="history-test-user")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        reminder = Reminder(
            user_id=user.id,
            title="History Test",
            trigger_type="scheduled",
            trigger_config={},
        )
        db_session.add(reminder)
        db_session.commit()
        db_session.refresh(reminder)

        hist = record_history(
            db_session, reminder.id, "scheduled", "Take medicine"
        )
        assert hist.reminder_id == reminder.id
        assert hist.trigger_type == "scheduled"
        assert hist.content == "Take medicine"
        assert hist.email_sent is False
        assert hist.id is not None
