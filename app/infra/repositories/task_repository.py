from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.domain.models import Task, TaskCreate, Priority
from app.infra.database_models import Task as TaskDB
from typing import List, Optional


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, user_id: str) -> List[Task]:
        try:
            tasks_db = self.db.query(TaskDB).filter(TaskDB.user_id == user_id).all()
            return [self._map_to_task(task_db) for task_db in tasks_db]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, task_id: str, user_id: str) -> Optional[Task]:
        try:
            task_db = self.db.query(TaskDB).filter(
                and_(TaskDB.id == task_id, TaskDB.user_id == user_id)
            ).first()
            
            if task_db:
                return self._map_to_task(task_db)
            return None
        except Exception as e:
            self.db.rollback()
            raise e

    def create(self, task_data: dict) -> Task:
        try:
            task_db = TaskDB(**task_data)
            self.db.add(task_db)
            self.db.commit()
            self.db.refresh(task_db)
            return self._map_to_task(task_db)
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, task_id: str, task_data: dict, user_id: str) -> Optional[Task]:
        try:
            task_db = self.db.query(TaskDB).filter(
                and_(TaskDB.id == task_id, TaskDB.user_id == user_id)
            ).first()
            
            if task_db:
                for key, value in task_data.items():
                    setattr(task_db, key, value)
                
                self.db.commit()
                self.db.refresh(task_db)
                return self._map_to_task(task_db)
            return None
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, task_id: str, user_id: str) -> bool:
        try:
            task_db = self.db.query(TaskDB).filter(
                and_(TaskDB.id == task_id, TaskDB.user_id == user_id)
            ).first()
            
            if task_db:
                self.db.delete(task_db)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise e

    def _map_to_task(self, task_db: TaskDB) -> Task:
        return Task(
            id=str(task_db.id),
            user_id=str(task_db.user_id),
            title=task_db.title,
            description=task_db.description,
            priority=Priority(task_db.priority),
            completed=task_db.completed,
            due_date=task_db.due_date,
            task_type=task_db.task_type,
            created_at=task_db.created_at,
            updated_at=task_db.updated_at,
        )