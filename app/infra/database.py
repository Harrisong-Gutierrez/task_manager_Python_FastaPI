import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import Settings
from app.infra.base import Base

# Crear la cadena de conexión usando las variables de Settings
SQLALCHEMY_DATABASE_URL = f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}"

# Crear el motor de base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función independiente para obtener la sesión de base de datos
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


# Instancia global de la base de datos
db = Database()

# Crear las tablas al importar este módulo
db.create_tables()