# app/database/models.py

import uuid
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship

# ⚠️ Asumiendo que Base está definida en db.py, la importamos.
# Si Base está definida aquí, asegúrate de que db.py la use.
from app.database.db import Base

# ===============================================
# 1. MODELO DE USUARIO (Tabla 'users')
# ===============================================


class User(Base):
    """Modelo ORM para la tabla de usuarios."""

    __tablename__ = "users"

    # id es el sub claim de Google, un identificador largo de string.
    # Usamos String, ya que el ID de Google no es un UUID estándar de la DB.
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con las conversaciones: Un usuario tiene muchas conversaciones.
    conversations = relationship("Conversation", back_populates="user")


# ===============================================
# 2. MODELO DE CONVERSACIÓN (Tabla 'conversations')
# ===============================================


class Conversation(Base):
    """Modelo ORM para la tabla de conversaciones."""

    __tablename__ = "conversations"

    # Usamos UUID generado por Python/PostgreSQL como ID primario.
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    user = relationship("User", back_populates="conversations")
    messages = relationship(
        "Message", back_populates="conversation", order_by="Message.timestamp"
    )


# ===============================================
# 3. MODELO DE MENSAJE (Tabla 'messages')
# ===============================================


class Message(Base):
    """Modelo ORM para la tabla de mensajes."""

    __tablename__ = "messages"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )
    tipo = Column(String, nullable=False)  # 'usuario' o 'ia'
    texto = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # El campo data_ia guarda la respuesta estructurada del modelo de IA (JSON).
    data_ia = Column(JSON, nullable=True)

    # Relación
    conversation = relationship("Conversation", back_populates="messages")
