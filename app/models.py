from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import IntEnum
import uuid

class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    @property
    def name(self):
        return {1: "Baja", 2: "Media", 3: "Alta"}[self.value]

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.LOW
    completed: bool = False
    due_date: Optional[datetime] = None
    task_type: str = "normal"

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))  # Cambiado a string
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True