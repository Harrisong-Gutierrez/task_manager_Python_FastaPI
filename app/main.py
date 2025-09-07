from fastapi import FastAPI
from app.api.endpoints import tasks, health
from app.api.infra.database import db

app = FastAPI(title="Task Manager API")

# Include routers
app.include_router(tasks.router)
app.include_router(health.router)

@app.on_event("startup")
async def startup_event():
    # Test connection
    try:
        response = db.get_client().table('tasks').select("*").limit(1).execute()
        print("Conexión exitosa a Supabase")
    except Exception as e:
        print(f"Error de conexión: {e}")

@app.get("/")
async def root():
    return {"message": "Task Manager API"}