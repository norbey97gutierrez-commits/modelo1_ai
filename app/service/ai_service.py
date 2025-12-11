
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from app.core.config import config

class SoftwareDevAssistant:
    """
    Servicio encargado de interactuar con el modelo de IA a través de LangChain.
    """
    def __init__(self):
        # Conexión y Configuración del Modelo
        self.llm = AzureChatOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            azure_deployment=config.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_key=config.AZURE_OPENAI_API_KEY,
            openai_api_version=config.AZURE_OPENAI_API_VERSION,
            temperature=0.7
        )

        # Plantilla de Prompt 
        self.template = PromptTemplate(
            input_variables=["pregunta"],
            template=(
                "Eres un experto en desarrollo de software y arquitectura de sistemas. "
                "Tu objetivo es ayudar a un desarrollador con su consulta, proporcionando "
                "código claro, mejores prácticas y explicaciones concisas. Responde a la siguiente consulta: {pregunta}"
            ),
        )

        # Creamos la cadena LCEL (LangChain Expression Language)
        self.cadena = self.template | self.llm

    def generate_response(self, consulta: str) -> str:
        """
        Ejecuta la cadena de LangChain y devuelve el contenido de la respuesta.
        Lógica desacoplada de FastAPI.
        """
        return self.cadena.invoke({"pregunta": consulta}).content

# Instancia Singleton
assistant_service = SoftwareDevAssistant()