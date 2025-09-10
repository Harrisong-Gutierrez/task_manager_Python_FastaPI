import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Configuración de base de datos para SQLAlchemy
    DB_USER: str = os.environ.get("user")
    DB_PASSWORD: str = os.environ.get("password")
    DB_HOST: str = os.environ.get("host")
    DB_PORT: str = os.environ.get("port")
    DB_NAME: str = os.environ.get("dbname")
    
    # Configuración de JWT (mantienes estas si las usas para autenticación)
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()