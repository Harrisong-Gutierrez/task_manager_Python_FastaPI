from fastapi import FastAPI
from sqlalchemy import text
from app.api.endpoints import tasks, auth, health, users
from app.infra.database import db

app = FastAPI(title="Task Manager API")

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(health.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_event():

    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión exitosa a la base de datos PostgreSQL")
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")


@app.get("/")
async def root():
    return {"message": "Task Manager API"}
