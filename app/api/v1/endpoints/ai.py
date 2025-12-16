import logging

from fastapi import APIRouter, Depends, HTTPException

# 🔑 Importaciones mínimas requeridas
from app.core.settings import (
    ChatRequest,  # El esquema de entrada (con solo 'prompt' si simplificamos)
    SoftwareSolution,  # Para el response_model
)
from app.service.ai_service import SoftwareArchitectAssistant  # El servicio de la IA

# Obtenemos la instancia del logger para este módulo
logger = logging.getLogger(__name__)

# Creamos un enrutador para agrupar rutas
router = APIRouter()

# ⚠️ Nota: El Singleton sigue siendo útil para la IA, lo mantenemos
_assistant_service_instance: SoftwareArchitectAssistant | None = None


# Función de Inyección de Dependencias (El Getter del Singleton)
def get_assistant_service() -> SoftwareArchitectAssistant:
    """
    Crea o devuelve la instancia Singleton del SoftwareArchitectAssistant.
    """
    global _assistant_service_instance
    if _assistant_service_instance is None:
        print("INFO: Inicializando SoftwareArchitectAssistant (¡Una sola vez!)...")
        _assistant_service_instance = SoftwareArchitectAssistant()
    return _assistant_service_instance


# ENDPOINT SIMPLE DE GENERACIÓN DE IA
@router.post("/generate", response_model=SoftwareSolution)
def generate_ai_response(
    # 1. Entrada: Solo el esquema de la solicitud (prompt)
    request: ChatRequest,
    # 2. Dependencia: Solo el servicio de la IA (Singleton)
    assistant_service: SoftwareArchitectAssistant = Depends(get_assistant_service),
):
    pregunta_usuario = request.prompt

    try:
        # 🔑 Lógica de la IA: Solo llamamos al servicio
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
