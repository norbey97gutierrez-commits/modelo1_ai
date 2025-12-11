from pydantic import BaseModel

class PromptRequest(BaseModel):
    """Define el esquema de entrada para la consulta del usuario."""
    prompt: str

class AIResponse(BaseModel):
    """Define el esquema de salida de la respuesta de la IA."""
    pregunta: str
    respuesta_generada: str