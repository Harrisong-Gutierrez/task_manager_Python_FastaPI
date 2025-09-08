from app.api.infra.database import db
from app.api.domain.models import Task, TaskCreate, Priority
from typing import List, Optional

class TaskRepository:
    def __init__(self):
        self.table = db.get_client().table('tasks')
    
    def get_all(self, user_id: str) -> List[Task]:
        response = self.table.select("*").eq('user_id', user_id).execute()
        return [self._map_to_task(task_data) for task_data in response.data]
    
    def get_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        response = self.table.select("*").eq('id', task_id).eq('user_id', user_id).execute()
        if response.data:
            return self._map_to_task(response.data[0])
        return None
    
    def create(self, task_data: dict) -> Task:
        response = self.table.insert(task_data).execute()
        return self._map_to_task(response.data[0])
    
    def update(self, task_id: str, task_data: dict, user_id: str) -> Optional[Task]:
        response = self.table.update(task_data).eq('id', task_id).eq('user_id', user_id).execute()
        if response.data:
            return self._map_to_task(response.data[0])
        return None
    
    def delete(self, task_id: str, user_id: str) -> bool:
        response = self.table.delete().eq('id', task_id).eq('user_id', user_id).execute()
        return len(response.data) > 0
    
    def _map_to_task(self, task_data: dict) -> Task:
        return Task(
            id=str(task_data['id']),
            user_id=str(task_data['user_id']),
            title=task_data['title'],
            description=task_data['description'],
            priority=Priority(task_data['priority']),
            completed=task_data['completed'],
            due_date=task_data['due_date'],
            task_type=task_data['task_type'],
            created_at=task_data['created_at'],
            updated_at=task_data.get('updated_at')
        )