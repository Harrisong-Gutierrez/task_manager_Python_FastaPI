from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.task_service import TaskService
from app.infra.repositories.task_repository import TaskRepository
from app.domain.models import Task, TaskCreate
from app.core.auth import get_current_user
from app.domain.models import User
from typing import List
from app.infra.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)):
    repository = TaskRepository(db)
    return TaskService(repository)


@router.get("/", response_model=List[Task])
async def get_tasks(
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_all_tasks(current_user.id)


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    task = service.get_task_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    return service.create_task(task, current_user.id)


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    updated_task = service.update_task(task_id, task, current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    service: TaskService = Depends(get_task_service),
    current_user: User = Depends(get_current_user),
):
    if not service.delete_task(task_id, current_user.id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
