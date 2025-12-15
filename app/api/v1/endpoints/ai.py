import logging

from fastapi import APIRouter, Depends, HTTPException

from app.core.settings import PromptRequest, SoftwareSolution
from app.service.ai_service import (
    SoftwareArchitectAssistant,
)

# Obtenemos la instancia del logger para este módulo
logger = logging.getLogger(__name__)

# Creamos un enrutador para agrupar rutas
router = APIRouter()

# Variable para almacenar la instancia del servicio de IA (Singleton)
_assistant_service_instance: SoftwareArchitectAssistant | None = None


# Función de Inyección de Dependencias
def get_assistant_service() -> SoftwareArchitectAssistant:
    """
    Crea o devuelve la instancia Singleton del SoftwareArchitectAssistant.
    """
    global _assistant_service_instance
    if _assistant_service_instance is None:
        print("INFO: Inicializando SoftwareArchitectAssistant (¡Una sola vez!)...")
        # Instanciamos la clase con el nuevo nombre
        _assistant_service_instance = SoftwareArchitectAssistant()
    return _assistant_service_instance


# ENDPOINT
@router.post("/generate", response_model=SoftwareSolution)
def generate_ai_response(
    request: PromptRequest,
    assistant_service: SoftwareArchitectAssistant = Depends(get_assistant_service),
):
    pregunta_usuario = request.prompt

    try:
        solucion_ia_obj: SoftwareSolution = assistant_service.generate_code_solution(
            pregunta_usuario
        )

        logger.info(
            "Solicitud AI procesada exitosamente.",
            extra={"pregunta": pregunta_usuario, "status": 200},
        )

        # Retornamos el modelo de respuesta esperado por el frontend
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
            detail="Error interno del servidor al comunicarse con el modelo de IA. Revise logs.",
        )
