import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from json_log_formatter import JSONFormatter

from app.api.v1.endpoints import ai
from app.core.config import ALLOWED_ORIGINS


# CONFIGURACIÓN DE LOGS ESTRUCTURADOS
def configure_json_logging():
    """Configura el manejador de logs para usar formato JSON."""

    # Obtenemos el logger raíz de Python
    root = logging.getLogger()

    # Si ya tiene un handler, lo eliminamos para evitar duplicados
    if root.handlers:
        for handler in root.handlers:
            root.removeHandler(handler)

    # Creamos el handler que escribe a la salida estándar (consola)
    # Usaremos stdout para que Uvicorn los capture.
    handler = logging.StreamHandler(sys.stdout)

    # Aplicamos el formateador JSON
    json_formatter = JSONFormatter()
    handler.setFormatter(json_formatter)

    # Establecemos el nivel mínimo y añadir el handler al logger raíz
    root.setLevel(logging.INFO)  # Capturamos INFO, WARNING, ERROR, CRITICAL
    root.addHandler(handler)


# Llamamos a la función de configuración justo al inicio de la ejecución del script
configure_json_logging()


def create_app() -> FastAPI:
    """Crea y configura la instancia de la aplicación FastAPI."""
    app = FastAPI(
        title="Software Development AI Assistant",
        description="Backend escalable y mantenible para un modelo de IA experto en desarrollo.",
        version="1.0.0",
    )

    # Configuración de Middleware (CORS)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Inclusión de Rutas (Endpoints)
    app.include_router(ai.router, prefix="/v1", tags=["Generación AI"])

    # Rutas de salud
    @app.get("/health")
    def health_check():
        return {"status": "ok", "message": "API running smoothly"}

    return app


# Instancia de la aplicación
app = create_app()

# Ejecuor de la app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)
