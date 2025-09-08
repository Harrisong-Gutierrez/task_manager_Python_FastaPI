from pydantic import BaseModel, Field, EmailStr
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


class UserBase(BaseModel):
    email: EmailStr
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority = Priority.LOW
    completed: bool = False
    due_date: Optional[str] = None
    task_type: str = "normal"


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
