from fastapi import APIRouter, HTTPException, Depends

from app.api.infra.repositories.task_repository import TaskRepository
from app.api.services.task_service import TaskService
from app.api.domain.models import Task, TaskCreate
from typing import List

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service():
    repository = TaskRepository()
    return TaskService(repository)


@router.get("/", response_model=List[Task])
async def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.get_all_tasks()


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str, service: TaskService = Depends(get_task_service)):
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/", response_model=Task)
async def create_task(
    task: TaskCreate, service: TaskService = Depends(get_task_service)
):
    return service.create_task(task)


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str, task: TaskCreate, service: TaskService = Depends(get_task_service)
):
    updated_task = service.update_task(task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_task(task_id: str, service: TaskService = Depends(get_task_service)):
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
