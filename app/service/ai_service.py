from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from app.core.config import config
from app.core.settings import SoftwareDevAnalysis


class SoftwareDevAssistant:
    """
    Servicio encargado de interactuar con el modelo de IA a través de LangChain.
    Utiliza LCEL para encadenamiento y Structured Output.
    """

    def __init__(self):
        # Conexión y Configuración del Modelo
        self.llm = AzureChatOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            azure_deployment=config.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_key=config.AZURE_OPENAI_API_KEY,
            openai_api_version=config.AZURE_OPENAI_API_VERSION,
            temperature=0.0,
        )

        # Definición del Parser
        self.parser = JsonOutputParser(pydantic_object=SoftwareDevAnalysis)

        # Plantilla de Prompt
        self.template = PromptTemplate(
            input_variables=["pregunta"],
            template=(
                "Eres un experto en desarrollo de software y arquitectura de sistemas. "
                "Tu objetivo es analizar la siguiente consulta: '{pregunta}'. "
                "Genera la respuesta estrictamente en el formato JSON proporcionado, sin texto adicional. "
                "\n\n{format_instructions}\n"
            ),
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        # Creamos la Cadena LCEL
        # El parser se encarga de convertir la salida de texto del LLM a un objeto SoftwareDevAnalysis.
        self.cadena = self.template | self.llm | self.parser

    def generate_response(self, consulta: str) -> SoftwareDevAnalysis:
        """
        Ejecuta la cadena LCEL y devuelve el objeto Pydantic SoftwareDevAnalysis directamente.
        """
        return self.cadena.invoke({"pregunta": consulta})


# Instancia Singleton
assistant_service = SoftwareDevAssistant()
