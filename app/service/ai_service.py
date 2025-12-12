import json
from functools import lru_cache

from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from openai import APIError, RateLimitError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

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

    # Aplicamos la lógica de reintentos (DECORADOR DE TENACITY)
    # para la conexion de OpenAI
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(
            (APIError, RateLimitError, OutputParserException)
        ),
        reraise=True,  # Vuelve a lanzar la excepción si los 3 intentos fallan.
    )
    # Usamos almacenamiento en cache para preguntas repetitivas con (lru_cache)
    @lru_cache(maxsize=32)
    def generate_response(self, consulta: str) -> SoftwareDevAnalysis:
        """
        Ejecuta la cadena LCEL con lógica de reintentos para manejar fallas de API y de parseo.
        """
        print(f"INFO: Intentando consultar Azure OpenAI para la pregunta: {consulta}")

        try:
            # La cadena LCEL se ejecuta. Si el JSON es malo, lanza OutputParserException.
            structured_data = self.cadena.invoke({"pregunta": consulta})

            # Si llega aquí, la validación del parser fue exitosa.
            return structured_data

        except OutputParserException as e:
            # 2. Lógica Defensiva: Si el parseo falla (JSON malo)
            print(
                "ADVERTENCIA: Falló el parseo automático. Intentando limpieza manual..."
            )

            # El mensaje de error de LangChain a menudo incluye el JSON crudo fallido.
            # Intentamos aislar el JSON crudo del error para forzar la carga.
            try:
                # Esta línea intenta encontrar el JSON entre comillas o bloques de texto
                # Es un intento heurístico, no 100% garantizado, pero es una buena defensa.
                raw_json_string = e.response.split("```json")[1].split("```")[0].strip()

                # Intentamos cargar el JSON manualmente
                cleaned_dict = json.loads(raw_json_string)

                # Si se carga, lo convertimos a la clase Pydantic y lo devolvemos
                # Esto evita que el reintento tenga que llamar a Azure de nuevo.
                return SoftwareDevAnalysis.parse_obj(cleaned_dict)

            except (IndexError, json.JSONDecodeError, AttributeError, KeyError):
                # 3. Si la limpieza manual falla, elevamos la excepción original.
                # El decorador @retry capturará esto y lo intentará de nuevo (Reintento Curativo).
                print(
                    "ADVERTENCIA: La limpieza manual falló. Reintentando la llamada completa a Azure..."
                )
                raise e
