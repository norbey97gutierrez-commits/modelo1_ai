from langchain.chains.structured_output import create_structured_output_chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from app.core.config import config
from app.core.settings import SoftwareDevAnalysis


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
            temperature=0.7,
        )

        # Plantilla de Prompt
        self.template = PromptTemplate(
            input_variables=["pregunta"],
            template=(
                "Eres un experto en desarrollo de software y arquitectura de sistemas. "
                "Tu objetivo es analizar la siguiente consulta: '{pregunta}'. "
                "Basado en ella, sugiere un rol, habilidades y una justificación."
            ),
        )

        # LLMChain para encadenamiento
        self.cadena = create_structured_output_chain(
            output_schema=SoftwareDevAnalysis,  # Le pasamos el esquema Pydantic deseado
            llm=self.llm,
            prompt=self.template,
        )

    def generate_response(self, consulta: str) -> SoftwareDevAnalysis:
        """
        Ejecuta la cadena y devuelve el objeto Pydantic SoftwareDevAnalysis.
        """
        response = self.cadena.invoke({"pregunta": consulta})
        return response["output"]


# Instancia Singleton
assistant_service = SoftwareDevAssistant()
