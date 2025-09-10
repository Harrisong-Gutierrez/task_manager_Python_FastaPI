from app.infra.repositories.task_repository import TaskRepository
from app.domain.models import Task, TaskCreate
from typing import List, Optional


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def get_all_tasks(self, user_id: str) -> List[Task]:
        return self.task_repository.get_all(user_id)

    def get_task_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        return self.task_repository.get_by_id(task_id, user_id)

    def create_task(self, task: TaskCreate, user_id: str) -> Task:
        task_data = {
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value,
            "completed": task.completed,
            "due_date": task.due_date,
            "task_type": task.task_type,
            "user_id": user_id,
        }
        return self.task_repository.create(task_data)

    def update_task(
        self, task_id: str, task: TaskCreate, user_id: str
    ) -> Optional[Task]:
        task_data = {
            "title": task.title,
            "description": task.description,
            "priority": task.priority.value,
            "completed": task.completed,
            "due_date": task.due_date,
            "task_type": task.task_type,
        }
        return self.task_repository.update(task_id, task_data, user_id)

    def delete_task(self, task_id: str, user_id: str) -> bool:
        return self.task_repository.delete(task_id, user_id)
