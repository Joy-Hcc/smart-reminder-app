import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=True)
    api_key_encrypted = Column(String(500), nullable=True)
    api_provider = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), onupdate=func.now())

    categories = relationship("Category", back_populates="user")
    reminders = relationship("Reminder", back_populates="user")

