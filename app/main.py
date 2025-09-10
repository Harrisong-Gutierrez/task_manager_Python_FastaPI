from fastapi import FastAPI
from sqlalchemy import text
from app.api.endpoints import tasks, auth, health, users
from app.infra.database import db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Iniciando aplicación Task Manager API...")

    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a la base de datos PostgreSQL")
    except Exception as e:
        print(f"❌ Error de conexión a la base de datos: {e}")

    yield

    print("🔻 Cerrando aplicación...")


app = FastAPI(title="Task Manager API", lifespan=lifespan)


app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(health.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Task Manager API"}
