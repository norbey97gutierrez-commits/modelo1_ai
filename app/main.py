import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from json_log_formatter import JSONFormatter

# 🔑 Importaciones mínimas: Solo necesitamos el router 'ai'
from app.api.v1.endpoints import ai


# CONFIGURACIÓN DE LOGS ESTRUCTURADOS (Se mantiene)
def configure_json_logging():
    """Configura el manejador de logs para usar formato JSON."""
    root = logging.getLogger()

    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    json_formatter = JSONFormatter()
    handler.setFormatter(json_formatter)

    # Establecemos el nivel mínimo y añadir el handler al logger raíz
    root.setLevel(logging.INFO)
    root.addHandler(handler)


# Llamamos a la función de configuración justo al inicio de la ejecución del script
configure_json_logging()


# 1. 💾 Definir el Lifespan (SIMPLIFICADO: Eliminamos la inicialización de la DB)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Función que maneja los eventos de inicio y apagado de la aplicación.
    """
    # ⚠️ Eliminamos la llamada a init_db() para evitar errores de conexión a PostgreSQL
    print("Iniciando la aplicación...")
    yield
    # Lógica de Cierre
    print("Apagando la aplicación...")


def create_app() -> FastAPI:
    """Crea y configura la instancia de la aplicación FastAPI."""
    app = FastAPI(
        title="Software Development AI Assistant",
        description="Backend centrado en la generación de IA estructurada.",
        version="1.0.0",
        lifespan=lifespan,  # Asignamos el lifespan simplificado
    )

    # Configuración de Middleware (CORS)
    ALLOWED_ORIGINS = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Endpoint de Generación (AI)
    app.include_router(ai.router, prefix="/v1", tags=["AI Generation"])

    # Rutas de salud
    @app.get("/health")
    def health_check():
        return {"status": "ok", "message": "API running smoothly"}

    # Endpoint raíz
    @app.get("/")
    def read_root():
        return {"message": "API del Arquitecto IA funcionando"}

    return app


# Instancia de la aplicación
app = create_app()

# Ejecutor de la app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
