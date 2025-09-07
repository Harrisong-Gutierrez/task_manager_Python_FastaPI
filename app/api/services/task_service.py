# Añadir 'app.'
from typing import List, Optional

from app.api.domain.models import Task, TaskCreate
from app.api.infra.repositories.task_repository import TaskRepository

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def get_all_tasks(self) -> List[Task]:
        return self.task_repository.get_all()
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        return self.task_repository.get_by_id(task_id)
    
    def create_task(self, task: TaskCreate) -> Task:
        # Aquí puedes añadir lógica de negocio adicional
        return self.task_repository.create(task)
    
    def update_task(self, task_id: str, task: TaskCreate) -> Optional[Task]:
        return self.task_repository.update(task_id, task)
    
    def delete_task(self, task_id: str) -> bool:
        return self.task_repository.delete(task_id)