import json

from fastapi import APIRouter, HTTPException

from app.core.settings import AIResponse, PromptRequest
from app.service.ai_service import assistant_service

# Creamos un enrutador para agrupar rutas
router = APIRouter()


@router.post("/generate", response_model=AIResponse)
def generate_ai_response(request: PromptRequest):
    pregunta_usuario = request.prompt

    try:
        analisis_ia_obj = assistant_service.generate_response(pregunta_usuario)

        # Convertimos el dict a string JSON
        respuesta_json_str = json.dumps(analisis_ia_obj, indent=None)

        return AIResponse(
            pregunta=pregunta_usuario, respuesta_generada=respuesta_json_str
        )
    except Exception as e:
        print(
            f"Error al procesar la solicitud para la pregunta: '{pregunta_usuario}' | Error: {e}"
        )

        # Lanza una excepción HTTP para el cliente
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al comunicarse con el modelo de IA. Revise logs.",
        )
