from typing import List

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    """Define el esquema de entrada para la consulta del usuario."""

    prompt: str


class AIResponse(BaseModel):
    """Define el esquema de salida de la respuesta de la IA."""

    pregunta: str
    respuesta_generada: str


# Esquemas de Salida ESTRUCTURADA para LangChain
class SoftwareDevAnalysis(BaseModel):
    """
    Define el esquema de Pydantic que la IA debe rellenar.
    Este es el formato de Salida Estructurada.
    """

    rol_sugerido: str = Field(
        description="Un solo rol profesional sugerido basado en la consulta del usuario."
    )
    habilidades_clave: List[str] = Field(
        description="Una lista de 3 a 5 habilidades técnicas esenciales para el rol sugerido."
    )
    justificacion_rol: str = Field(
        description="Una justificación concisa de por qué el rol es el más adecuado para la consulta en un solo párrafo."
    )
