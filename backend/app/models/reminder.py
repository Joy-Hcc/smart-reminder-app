import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), default="medium")
    trigger_type = Column(String(50), nullable=False)
    trigger_config = Column(Text, nullable=False, default="{}")
    advance_notice = Column(Integer, default=0)
    repeat_rule = Column(String(50), nullable=True)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="reminders")
    category = relationship("Category", back_populates="reminders")
    event_trigger = relationship("EventTrigger", back_populates="reminder", uselist=False, cascade="all, delete-orphan")
    histories = relationship("ReminderHistory", back_populates="reminder", cascade="all, delete-orphan")


class EventTrigger(Base):
    __tablename__ = "event_triggers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reminder_id = Column(String(36), ForeignKey("reminders.id"), nullable=False, unique=True)
    event_type = Column(String(50), nullable=False)
    config = Column(Text, nullable=False, default="{}")
    last_checked = Column(DateTime(timezone=True), nullable=True)
    last_triggered = Column(DateTime(timezone=True), nullable=True)

    reminder = relationship("Reminder", back_populates="event_trigger")
