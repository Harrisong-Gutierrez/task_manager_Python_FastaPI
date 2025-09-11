from datetime import timezone
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.infra.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    due_date = Column(String, nullable=True)
    task_type = Column(String, default="normal")
    user_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="tasks")
