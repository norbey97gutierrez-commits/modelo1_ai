import logging

from fastapi import APIRouter, Depends, HTTPException

from app.core.settings import SoftwareSolution
from app.service.ai_service import (
    SoftwareArchitectAssistant,
)

# Obtenemos la instancia del logger para este módulo
logger = logging.getLogger(__name__)

# Creamos un enrutador para agrupar rutas
router = APIRouter()

# Variable para almacenar la instancia del servicio de IA (Singleton)
# Usamos el nuevo nombre de la clase
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


# ENDPOINT
@router.post("/generate", response_model=SoftwareSolution)
def generate_ai_response(
    request: ChatRequest,  # 🆕 Usamos el nuevo esquema
    assistant_service: SoftwareArchitectAssistant = Depends(get_assistant_service),
    current_user: User = Depends(get_current_user),  # 🔒 Protección
    db: Session = Depends(get_db),  # 💾 Inyectamos la sesión de la BD
):
    pregunta_usuario = request.prompt

    try:
        solucion_ia_obj: SoftwareSolution = assistant_service.generate_code_solution(
            pregunta_usuario
        )

        # 3. 💾 PERSISTIR RESPUESTA DE LA IA (Guardamos la solución estructurada)
        history_service.add_message_to_conversation(
            conversation_id=conversation_id,
            tipo="ia",
            texto=solucion_ia_obj.explicacion_tecnica,  # Guardamos la explicación como texto principal
            data_ia=solucion_ia_obj,  # Guardamos el objeto SoftwareSolution completo en el campo JSON
        )

        logger.info(
            "Solicitud AI procesada y persistida exitosamente.",
            extra={
                "user_id": current_user.id,
                "conv_id": conversation_id,
                "status": 200,
            },
        )

        # Retornamos el modelo de respuesta esperado por el frontend
        return solucion_ia_obj

    except Exception as e:
        logger.error(
            "Falla crítica en el servicio de IA o al persistir.",
            exc_info=True,
            extra={
                "error_tipo": type(e).__name__,
                "pregunta_fallida": pregunta_usuario,
            },
        )
        # ⚠️ Si falla la IA, debemos intentar eliminar el mensaje del usuario
        # que fue guardado en el paso 1 para evitar estados incompletos.
        # Por simplicidad, por ahora solo elevamos la excepción.

        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la IA o guardar la conversación. Revise logs.",
        )
