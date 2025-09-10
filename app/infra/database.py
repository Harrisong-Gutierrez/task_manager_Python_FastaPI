import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.infra.base import Base


SQLALCHEMY_DATABASE_URL = f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Obtiene una sesión de base de datos.
    Úsalo como dependencia en tus endpoints FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Database:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def create_tables(self):
        """Crea todas las tablas en la base de datos."""
        Base.metadata.create_all(bind=self.engine)


db = Database()


db.create_tables()
