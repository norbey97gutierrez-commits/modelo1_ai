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
from app.core.settings import SoftwareSolution


class SoftwareArchitectAssistant:
    """
    Motor de generación de software universal con salida estructurada.
    """

    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
            azure_deployment=config.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_key=config.AZURE_OPENAI_API_KEY,
            openai_api_version=config.AZURE_OPENAI_API_VERSION,
            temperature=0.2,
        )

        self.parser = JsonOutputParser(pydantic_object=SoftwareSolution)

        self.template = PromptTemplate(
            input_variables=["pregunta"],
            template=(
                "Eres un Arquitecto de Software Senior y Desarrollador Full-Stack Experto. "
                "Tu misión es resolver el siguiente requerimiento técnico: '{pregunta}'. "
                "Puedes trabajar en cualquier lenguaje (C#, Python, JS, Go, Rust, etc.) y framework. "
                "Genera código limpio, documentado y siguiendo principios SOLID. "
                "Responde EXCLUSIVAMENTE en formato JSON siguiendo estas instrucciones:\n\n"
                "{format_instructions}\n"
            ),
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.cadena = self.template | self.llm | self.parser

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(
            (APIError, RateLimitError, OutputParserException)
        ),
        reraise=True,
    )
    @lru_cache(maxsize=32)
    def generate_code_solution(self, consulta: str) -> SoftwareSolution:
        print(f"INFO: Generando solución de software para: {consulta}")
        try:
            # Invocación de la cadena
            return self.cadena.invoke({"pregunta": consulta})

        except OutputParserException as e:
            print(
                "ADVERTENCIA: Falló el parseo automático. Intentando recuperación manual..."
            )
            try:
                # Intento de extracción de JSON crudo
                raw_content = (
                    e.response.content
                    if hasattr(e.response, "content")
                    else str(e.response)
                )
                if "```json" in raw_content:
                    raw_json_string = (
                        raw_content.split("```json")[1].split("```")[0].strip()
                    )
                else:
                    raw_json_string = raw_content.strip()

                cleaned_dict = json.loads(raw_json_string)

                return SoftwareSolution.model_validate(cleaned_dict)
            except Exception:
                raise e
