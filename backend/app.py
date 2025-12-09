import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI
from pydantic import BaseModel

# Carga lobal
load_dotenv()


class AsistenteIA:
    def __init__(self):
        # Conexion con Azure
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        )

        # Plantilla base
        self.template = PromptTemplate(
            input_variables=["pregunta"],
            template="Eres un experto en programación Python. Responde a la siguiente consulta: {pregunta}",
        )

        # Creamos la cadena LCEL
        self.cadena = self.template | self.llm

    def responder(self, consulta):
        """Ejecuta la cadena y devuelve el contenido de la respuesta."""
        return self.cadena.invoke({"pregunta": consulta}).content


# Esquema de validación para la API
class PromptRequest(BaseModel):
    """Define que el cliente debe enviar un JSON con la clave 'prompt'."""

    prompt: str


# Inicialización de servicios
app = FastAPI()
asistente = AsistenteIA()


@app.post("/generate")
def handle_generate(request: PromptRequest):
    """
    Recibe el objeto PromptRequest, extrae el texto y
    utiliza el asistente para generar la respuesta.
    """
    try:
        # Se extrae el texto del esquema Pydantic
        pregunta_usuario = request.prompt
        # Se llama a la lógica de LangChain
        respuesta_ia = asistente.responder(request.prompt)
        # Retorna un diccionario que FastAPI convierte automáticamente a JSON
        return {"pregunta": pregunta_usuario, "respuesta_generada": respuesta_ia}
    except Exception as e:
        # Capturamos cualquier error de la API de Azure o LangChain
        print(f"Error al procesar la solicitud: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al comunicarse con el modelo de IA.",
        )


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
