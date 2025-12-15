import uuid
from datetime import datetime
from typing import List, Optional

from app.database.schemas import SoftwareSolution  # Para tipado y manejo de la data IA
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import models, schemas


class HistoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_new_conversation(
        self, user_id: str, first_message_text: str
    ) -> models.Conversation:
        """
        Crea un nuevo registro de conversación en la BD.
        """
        new_id = str(uuid.uuid4())
        new_conv = models.Conversation(
            id=new_id,
            user_id=user_id,
            title=first_message_text[:50]
            + "...",  # Título basado en las primeras 50 letras
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(new_conv)
        self.db.commit()
        self.db.refresh(new_conv)
        return new_conv

    def add_message_to_conversation(
        self,
        conversation_id: str,
        tipo: str,
        texto: str,
        data_ia: Optional[SoftwareSolution] = None,
    ) -> models.Message:
        """
        Añade un mensaje (usuario o IA) a una conversación existente.
        """
        message_id = str(uuid.uuid4())

        # Convierte el esquema de IA a JSON (si existe) para el campo data_ia
        data_ia_json = data_ia.model_dump() if data_ia else None

        new_message = models.Message(
            id=message_id,
            conversation_id=conversation_id,
            tipo=tipo,
            texto=texto,
            data_ia=data_ia_json,
            timestamp=datetime.utcnow(),
        )

        self.db.add(new_message)

        # ⚠️ Actualizar la marca de tiempo de la conversación para ordenación
        self.db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id
        ).update({"updated_at": datetime.utcnow()})

        self.db.commit()
        self.db.refresh(new_message)
        return new_message

    def get_conversation_summary(
        self, user_id: str
    ) -> List[schemas.ConversationSummary]:
        """
        Obtiene la lista de conversaciones de un usuario, ordenada por la más reciente.
        """
        conversations_orm = (
            self.db.query(models.Conversation)
            .filter(models.Conversation.user_id == user_id)
            .order_by(desc(models.Conversation.updated_at))
            .all()
        )

        # Converte los modelos ORM a esquemas Pydantic
        return [
            schemas.ConversationSummary.model_validate(c) for c in conversations_orm
        ]

    def get_conversation_details(
        self, user_id: str, conversation_id: str
    ) -> Optional[models.Conversation]:
        """
        Obtiene una conversación completa y sus mensajes asociados.
        """
        # Asegura que la conversación pertenezca al usuario logueado
        conversation = (
            self.db.query(models.Conversation)
            .filter(
                models.Conversation.id == conversation_id,
                models.Conversation.user_id == user_id,
            )
            .first()
        )

        return conversation
