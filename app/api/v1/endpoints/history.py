from typing import List

# Importaciones de la Lógica de Negocio y Core
from app.database.db import get_db
from app.database.schemas import Conversation, ConversationSummary, User
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.service.history_service import HistoryService

# Creamos el router para el historial
router = APIRouter()


# Endpoint para obtener el resumen de conversaciones del usuario
@router.get(
    "/",
    response_model=List[ConversationSummary],  # Usamos el esquema Pydantic
    status_code=status.HTTP_200_OK,
)
async def get_history_summary(
    current_user: User = Depends(get_current_user),  # 🔒 Protección
    db: Session = Depends(get_db),
):
    """
    Devuelve un resumen (ID, Título, Fecha) de las conversaciones
    del usuario autenticado.
    """
    history_service = HistoryService(db)
    # Llama al servicio para obtener el historial del usuario
    summary = history_service.get_conversation_summary(current_user.id)

    return summary


# Endpoint para cargar una conversación completa por ID
@router.get(
    "/{conversation_id}",
    response_model=Conversation,  # Usamos el esquema de conversación completa
    status_code=status.HTTP_200_OK,
)
async def get_conversation_detail(
    conversation_id: str,
    current_user: User = Depends(get_current_user),  # 🔒 Protección
    db: Session = Depends(get_db),
):
    """
    Carga todos los mensajes de una conversación específica por ID.
    """
    history_service = HistoryService(db)

    conversation = history_service.get_conversation_details(
        user_id=current_user.id, conversation_id=conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversación con ID '{conversation_id}' no encontrada para este usuario.",
        )

    # El modelo ORM (conversation) se convertirá automáticamente al esquema Pydantic (Conversation)
    # gracias al 'response_model' y al from_attributes=True en el esquema.
    return conversation


# Endpoint para iniciar un nuevo chat (útil para la Sidebar del frontend)
@router.post("/new", status_code=status.HTTP_201_CREATED)
async def new_chat_create(
    current_user: User = Depends(get_current_user),  # 🔒 Protección
    db: Session = Depends(get_db),
):
    """
    Crea una nueva conversación vacía y devuelve su ID para empezar a chatear.
    """
    history_service = HistoryService(db)

    # Crea una conversación temporal con un título genérico
    new_conv = history_service.create_new_conversation(
        user_id=current_user.id,
        first_message_text="Nuevo Chat",  # Se actualizará con el primer prompt real
    )

    # Devuelve el ID de la nueva conversación al frontend
    return {"conversation_id": new_conv.id}
