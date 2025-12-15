import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carga las variables de entorno desde el archivo .env
load_dotenv()


# Define la configuración de tu aplicación usando Pydantic BaseSettings
class Settings(BaseSettings):
    # ===============================================
    # 🔒 CONFIGURACIÓN DE SEGURIDAD (JWT)
    # ===============================================

    # Clave secreta para firmar los JWTs. Debe ser SECRETA y cargarse desde .env
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    # Tiempo de expiración del token (en minutos)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")

    # ===============================================
    # 🧠 CONFIGURACIÓN DE LA IA (Azure OpenAI)
    # ===============================================

    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    # ===============================================
    # 💾 CONFIGURACIÓN DE LA BASE DE DATOS
    # ===============================================

    # Cadena de conexión a la BD (ajusta según tu motor: SQLite, Postgres, etc.)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")


# Instancia global de configuración
settings = Settings()
