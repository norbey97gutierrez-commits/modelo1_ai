# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import ai
from app.core.config import ALLOWED_ORIGINS


def create_app() -> FastAPI:
    """Crea y configura la instancia de la aplicación FastAPI."""
    app = FastAPI(
        title="Software Development AI Assistant API",
        description="Backend escalable y mantenible para un modelo de IA experto en desarrollo.",
        version="1.0.0",
    )

    # 1. Configuración de Middleware (CORS)
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
