import json

from fastapi import APIRouter, Depends, HTTPException

from app.core.settings import AIResponse, PromptRequest
from app.service.ai_service import SoftwareDevAssistant

# Creamos un enrutador para agrupar rutas
router = APIRouter()

# Variable para almacenar la instancia del servicio de IA (Singleton)
_assistant_service_instance: SoftwareDevAssistant | None = None


# Función de Inyección de Dependencias (El Getter del Singleton)
def get_assistant_service() -> SoftwareDevAssistant:
    """
    Crea o devuelve la instancia Singleton del SoftwareDevAssistant.
    Esta función se llama al inicio de la aplicación, pero solo inicializa
    la clase una única vez.
    """
    global _assistant_service_instance
    if _assistant_service_instance is None:
        print("INFO: Inicializando SoftwareDevAssistant (¡Una sola vez!)...")
        _assistant_service_instance = SoftwareDevAssistant()
    return _assistant_service_instance


@router.post("/generate", response_model=AIResponse)
def generate_ai_response(
    request: PromptRequest,
    assistant_service: SoftwareDevAssistant = Depends(
        get_assistant_service
    ),  # <-- ¡EL CAMBIO CLAVE!
):
    pregunta_usuario = request.prompt

    try:
        # El código aquí usa la instancia inyectada
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
