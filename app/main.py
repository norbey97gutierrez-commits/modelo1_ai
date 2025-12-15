import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from json_log_formatter import JSONFormatter

from app.api.v1.endpoints import ai, auth, history

# 🔑 Importaciones de la Configuración y DB
from app.database.db import init_db


# CONFIGURACIÓN DE LOGS ESTRUCTURADOS
def configure_json_logging():
    """Configura el manejador de logs para usar formato JSON."""
    root = logging.getLogger()

    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    json_formatter = JSONFormatter()
    handler.setFormatter(json_formatter)

    root.setLevel(logging.INFO)
    root.addHandler(handler)


# Llamamos a la función de configuración justo al inicio de la ejecución del script
configure_json_logging()


# 1. 💾 Definir el Lifespan (Inicialización de la DB)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Función que maneja los eventos de inicio y apagado de la aplicación.
    """
    # Lógica de Inicio: Inicializa la Base de Datos (Crea tablas)
    print("Inicializando la Base de Datos (Creando Tablas si no existen)...")
    init_db()  # 👈 Llamada a la función de la capa database
    print("Base de Datos Inicializada.")
    yield
    # Lógica de Cierre (por si necesitas limpiar recursos al apagar)
    print("Apagando la aplicación...")


def create_app() -> FastAPI:
    """Crea y configura la instancia de la aplicación FastAPI."""
    app = FastAPI(
        title="Software Development AI Assistant",
        description="Backend escalable y mantenible para un modelo de IA experto en desarrollo.",
        version="1.0.0",
        lifespan=lifespan,  # 👈 Asignamos el lifespan aquí
    )

    # Configuración de Middleware (CORS)
    # ⚠️ Usamos settings.ALLOWED_ORIGINS si la tienes definida en settings.py
    # Si no la tienes definida, usa una lista vacía o tu dominio frontend.
    ALLOWED_ORIGINS = ["*"]  # Temporalmente amplio, si usabas config.ALLOWED_ORIGINS

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 2. Inclusión de Routers

    # Endpoints de Autenticación
    app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])

    # Endpoints de Historial
    app.include_router(history.router, prefix="/v1/history", tags=["History"])

    # Endpoint de Generación
    # ⚠️ Hemos ajustado el prefix para que los endpoints sean /v1/generate
    app.include_router(ai.router, prefix="/v1/generate", tags=["AI Generation"])

    # Rutas de salud
    @app.get("/health")
    def health_check():
        return {"status": "ok", "message": "API running smoothly"}

    # Endpoint raíz (si lo tienes)
    @app.get("/")
    def read_root():
        return {"message": "API del Arquitecto IA funcionando"}

    return app


# Instancia de la aplicación
app = create_app()

# Ejecutor de la app (Esto es manejado usualmente por un comando de consola, pero se mantiene si lo necesitas)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
