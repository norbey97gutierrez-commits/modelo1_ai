import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user  # 🔒 Para proteger el endpoint

# Importaciones de Core, DB y Servicios
from app.core.settings import SoftwareSolution
from app.database.db import get_db
from app.database.models import (
    ChatRequest,  # 🆕 Nuevo esquema de entrada
    User,  # Para el usuario autenticado
)
from app.service.ai_service import SoftwareArchitectAssistant
from app.service.history_service import HistoryService

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
        _assistant_service_instance = SoftwareArchitectAssistant()
    return _assistant_service_instance


# 🆕 ENDPOINT (Ahora recibe el ID de conversación y requiere autenticación)
@router.post("/", response_model=SoftwareSolution, status_code=status.HTTP_200_OK)
def generate_ai_response(
    request: ChatRequest,  # 🆕 Usamos el nuevo esquema
    assistant_service: SoftwareArchitectAssistant = Depends(get_assistant_service),
    current_user: User = Depends(get_current_user),  # 🔒 Protección
    db: Session = Depends(get_db),  # 💾 Inyectamos la sesión de la BD
):
    pregunta_usuario = request.prompt
    conversation_id = request.conversation_id

    history_service = HistoryService(db)

    try:
        # 1. 💾 PERSISTIR MENSAJE DEL USUARIO
        # Si es el primer mensaje, actualizamos el título de la conversación
        history_service.add_message_to_conversation(
            conversation_id=conversation_id, tipo="usuario", texto=pregunta_usuario
        )

        # 2. 🧠 GENERAR RESPUESTA DE LA IA
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
