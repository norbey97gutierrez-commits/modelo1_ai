from fastapi import APIRouter, HTTPException

from app.core.settings import AIResponse, PromptRequest
from app.service.ai_service import assistant_service

# Creamos un enrutador para agrupar rutas
router = APIRouter()


@router.post("/generate", response_model=AIResponse)
def generate_ai_response(request: PromptRequest):
    """
    Endpoint para generar una respuesta de la IA.
    Utiliza el servicio de IA y maneja los errores.
    """
    try:
        pregunta_usuario = request.prompt

        # Llama al servicio, que devuelve un objeto SoftwareDevAnalysis
        analisis_ia_obj = assistant_service.generate_response(pregunta_usuario)

        # Convertimos el objeto Pydantic devuelto por LangChain a un string JSON.
        # .json() es un método de Pydantic que hace esto eficientemente.
        respuesta_json_str = analisis_ia_obj.json()

        # Retorna el esquema de respuesta validado por la API
        return AIResponse(
            pregunta=pregunta_usuario, respuesta_generada=respuesta_json_str
        )
    except Exception as e:
        # Capturamos errores específicos (Azure/LangChain)
        print(f"Error al procesar la solicitud en el servicio de IA: {e}")
        # Lanza una excepción HTTP que FastAPI manejará automáticamente
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al comunicarse con el modelo de IA.",
        )
