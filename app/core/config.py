import os
from dotenv import load_dotenv
from typing import List

# Carga variables de entorno al iniciar
load_dotenv()


# Orígenes permitidos para CORS
ALLOWED_ORIGINS_STR = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
ALLOWED_ORIGINS: List[str] = [origin.strip() for origin in ALLOWED_ORIGINS_STR.split(',')]

# Configuración de LangChain/Azure OpenAI
class AzureOpenAISettings:
    """Clase para agrupar la configuración de Azure OpenAI."""
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION")

# Instancia de configuración
config = AzureOpenAISettings()