from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# ===============================================
# A. ESQUEMAS DE GENERACIÓN DE IA (Software Solution)
# ===============================================


class PromptRequest(BaseModel):
    """Esquema de entrada para el endpoint de generación."""

    prompt: str


class SoftwareSolution(BaseModel):
    """
    Define el esquema para la salida estructurada del modelo de IA.
    Este esquema se usa para la validación y tipado de la respuesta de la IA.
    """

    proyecto_nombre: str = Field(
        description="Nombre breve del módulo o funcionalidad desarrollada."
    )
    lenguaje: str = Field(
        description="Lenguaje de programación utilizado (ej. Python, JavaScript)."
    )
    framework: str = Field(
        description="Framework utilizado o 'None' si es código puro."
    )
    estructura_archivos: List[str] = Field(
        description="Lista de archivos necesarios para implementar la solución."
    )
    codigo_principal: str = Field(description="El código fuente principal generado.")
    explicacion_tecnica: str = Field(
        description="Explicación detallada de la arquitectura y lógica utilizada (Markdown)."
    )
    dependencias: List[str] = Field(
        description="Lista de librerías o paquetes externos necesarios (ej. npm install X, pip install Y)."
    )


# ===============================================
# B. ESQUEMAS DE AUTENTICACIÓN Y USUARIO
# ===============================================


class UserBase(BaseModel):
    """Esquema base para la información mínima del usuario."""

    email: str
    name: Optional[str] = None
    picture: Optional[str] = None  # URL de la imagen de perfil de Google


class User(UserBase):
    """Esquema completo del usuario (lo que se almacena en la BD y se devuelve)."""

    id: str  # ID único de Google (sub claim)

    class Config:
        # Permite la conversión desde modelos ORM (necesario para FastAPI)
        from_attributes = True


# ===============================================
# C. ESQUEMAS DE HISTORIAL (Conversación y Mensajes)
# ===============================================


class Message(BaseModel):
    """
    Define la estructura de un mensaje individual en la conversación.
    Incluye un campo opcional para la data estructurada de la IA.
    """

    id: Optional[str] = None
    tipo: str  # 'usuario' o 'ia'
    texto: str
    timestamp: datetime = Field(default_factory=datetime.now)

    # 🆕 Campo Opcional: Almacena la data estructurada de la IA si existe.
    # Usamos Dict[str, Any] o SoftwareSolution.dict() si se asegura la conversión.
    data_ia: Optional[Dict[str, Any]] = None


class Conversation(BaseModel):
    """Define el esquema de una conversación completa."""

    id: Optional[str] = None  # ID único de la conversación
    user_id: str  # Clave foránea al usuario
    title: str  # Primer mensaje del usuario (título)
    messages: List[Message]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True


class ConversationSummary(BaseModel):
    """Esquema para la lista de historial que se muestra en la Sidebar."""

    id: str
    title: str
    date: datetime = Field(alias="updated_at")

    class Config:
        from_attributes = True
