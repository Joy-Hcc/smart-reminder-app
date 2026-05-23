import uuid
from sqlalchemy import Column, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ReminderHistory(Base):
    __tablename__ = "reminder_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reminder_id = Column(String(36), ForeignKey("reminders.id"), nullable=False)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    trigger_type = Column(String(50), nullable=True)
    content = Column(Text, nullable=True)
    email_sent = Column(Boolean, default=False)
    email_status = Column(String(50), nullable=True)

    reminder = relationship("Reminder", back_populates="histories")
