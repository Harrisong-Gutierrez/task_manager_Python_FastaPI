
from typing import List, Optional

from app.api.domain.models import Priority, Task, TaskCreate
from app.api.infra.database import db  # Import db from your database module

class TaskRepository:
    def __init__(self):
        self.table = db.get_client().table('tasks')
    
    def get_all(self) -> List[Task]:
        response = self.table.select("*").execute()
        return [self._map_to_task(task_data) for task_data in response.data]
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        response = self.table.select("*").eq('id', task_id).execute()
        if response.data:
            return self._map_to_task(response.data[0])
        return None
    
    def create(self, task: TaskCreate) -> Task:
        task_data = task.dict()
        response = self.table.insert(task_data).execute()
        return self._map_to_task(response.data[0])
    
    def update(self, task_id: str, task: TaskCreate) -> Optional[Task]:
        task_data = task.dict()
        response = self.table.update(task_data).eq('id', task_id).execute()
        if response.data:
            return self._map_to_task(response.data[0])
        return None
    
    def delete(self, task_id: str) -> bool:
        response = self.table.delete().eq('id', task_id).execute()
        return len(response.data) > 0
    
    def _map_to_task(self, task_data: dict) -> Task:
        return Task(
            id=str(task_data['id']),
            title=task_data['title'],
            description=task_data['description'],
            priority=Priority(task_data['priority']),
            completed=task_data['completed'],
            due_date=task_data['due_date'],
            task_type=task_data['task_type'],
            created_at=task_data['created_at'],
            updated_at=task_data.get('updated_at')
        )