from fastapi import FastAPI, HTTPException
from app.database import supabase, test_connection
from app.models import Task, TaskCreate, Priority

app = FastAPI(title="Task Manager API")

# Evento de startup para probar la conexión
@app.on_event("startup")
async def startup_event():
    test_connection()

@app.get("/")
async def root():
    return {"message": "Task Manager API"}

# Obtener todas las tareas
@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    response = supabase.table('tasks').select("*").execute()
    if not response.data:
        return []
    
    tasks = []
    for task_data in response.data:
        task = Task(
            id=str(task_data['id']),  # Convertir a string
            title=task_data['title'],
            description=task_data['description'],
            priority=Priority(task_data['priority']),
            completed=task_data['completed'],
            due_date=task_data['due_date'],
            task_type=task_data['task_type'],
            created_at=task_data['created_at'],
            updated_at=task_data.get('updated_at')
        )
        tasks.append(task)
    return tasks

# Obtener una tarea por ID (cambiado a string)
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str):  # Cambiado a string
    response = supabase.table('tasks').select("*").eq('id', task_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = response.data[0]
    return Task(
        id=str(task_data['id']),  # Convertir a string
        title=task_data['title'],
        description=task_data['description'],
        priority=Priority(task_data['priority']),
        completed=task_data['completed'],
        due_date=task_data['due_date'],
        task_type=task_data['task_type'],
        created_at=task_data['created_at'],
        updated_at=task_data.get('updated_at')
    )

# Crear una nueva tarea
@app.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate):
    # Convertir el modelo a un diccionario y el priority a su valor entero
    task_data = task.dict()
    task_data['priority'] = task_data['priority'].value
    response = supabase.table('tasks').insert(task_data).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error creating task")
    created_task = response.data[0]
    return Task(
        id=str(created_task['id']),  # Convertir a string
        title=created_task['title'],
        description=created_task['description'],
        priority=Priority(created_task['priority']),
        completed=created_task['completed'],
        due_date=created_task['due_date'],
        task_type=created_task['task_type'],
        created_at=created_task['created_at'],
        updated_at=created_task.get('updated_at')
    )

# Actualizar una tarea (cambiado a string)
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskCreate):  # Cambiado a string
    # Convertir el modelo a un diccionario y el priority a su valor entero
    task_data = task.dict()
    task_data['priority'] = task_data['priority'].value
    # Actualizar la tarea
    response = supabase.table('tasks').update(task_data).eq('id', task_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = response.data[0]
    return Task(
        id=str(updated_task['id']),  # Convertir a string
        title=updated_task['title'],
        description=updated_task['description'],
        priority=Priority(updated_task['priority']),
        completed=updated_task['completed'],
        due_date=updated_task['due_date'],
        task_type=updated_task['task_type'],
        created_at=updated_task['created_at'],
        updated_at=updated_task.get('updated_at')
    )

# Eliminar una tarea (cambiado a string)
@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):  # Cambiado a string
    response = supabase.table('tasks').delete().eq('id', task_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}