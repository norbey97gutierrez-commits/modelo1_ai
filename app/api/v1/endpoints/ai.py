import logging

from fastapi import APIRouter, Depends, HTTPException

from app.core.settings import (
    ChatRequest,
    SoftwareSolution,
)
from app.service.ai_service import SoftwareArchitectAssistant

# Obtenemos la instancia del logger para este módulo
logger = logging.getLogger(__name__)

# Creamos un enrutador para agrupar rutas
router = APIRouter()

# Instancia inglenton
_assistant_service_instance: SoftwareArchitectAssistant | None = None


# Función de Inyección de Dependencias
def get_assistant_service() -> SoftwareArchitectAssistant:
    """
    Crea o devuelve la instancia Singleton del SoftwareArchitectAssistant.
    """
    global _assistant_service_instance
    if _assistant_service_instance is None:
        print("INFO: Inicializando SoftwareArchitectAssistant (¡Una sola vez!)...")
        _assistant_service_instance = SoftwareArchitectAssistant()
    return _assistant_service_instance


# ENDPOINT DE GENERACIÓN DE IA
@router.post("/generate", response_model=SoftwareSolution)
def generate_ai_response(
    # Entrada del (prompt)
    request: ChatRequest,
    # Dependencia Singleton
    assistant_service: SoftwareArchitectAssistant = Depends(get_assistant_service),
):
    pregunta_usuario = request.prompt

    try:
        # Lógica de la IA llamamos al servicio
        solucion_ia_obj: SoftwareSolution = assistant_service.generate_code_solution(
            pregunta_usuario
        )

        logger.info(
            "Solicitud AI procesada exitosamente.",
            extra={
                "pregunta": pregunta_usuario,
                "status": 200,
            },
        )

        # Retornamos el modelo de respuesta esperado
        return solucion_ia_obj

    except Exception as e:
        logger.error(
            "Falla crítica en el servicio de IA.",
            exc_info=True,
            extra={
                "error_tipo": type(e).__name__,
                "pregunta_fallida": pregunta_usuario,
            },
        )
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la IA. Revise logs.",
        )
