# 🧠 Backend | AI Architect Assistant API

API de lógica de negocio construida en **Python** para gestionar la comunicación con los modelos de lenguaje (LLMs) y estructurar las respuestas antes de enviarlas al frontend.

## 🛠️ Tecnologías Principales

* **Python 3.x**
* **FastAPI:** Framework moderno para construir la API (implícito por la estructura modular de la app).
* **LangChain / OpenAI SDK:** (Implícito) Framework para la orquestación de la lógica de IA, manejo de prompts y generación de respuestas estructuradas.

## 🏗️ Arquitectura y Componentes

El proyecto sigue una arquitectura modular separada en capas:

1.  **Capa de Endpoints (`app/api/v1/endpoints`):**
    * `ai.py`: Definimods los *endpoints* HTTP (`/v1/ai/chat`) que reciben las peticiones del frontend y delegan la lógica al servicio.

2.  **Capa de Servicio (`app/service`):**
    * `ai_service.py`: Contiene la lógica de negocio pura. Aquí se orquesta la llamada al modelo de IA, la gestión del historial de la conversación y, crucialmente, la función de **estructuración** de la respuesta del LLM a un formato JSON compatible con el frontend.

3.  **Capa Core (`app/core`):**
    * `config.py` / `settings.py`: Manejo de la configuración global, incluyendo la carga de variables de entorno (como la clave de la API de Gemini, por ejemplo).

4.  **Raíz:**
    * `main.py`: Punto de entrada principal de la aplicación (Uvicorn/FastAPI).
    * `requirements.txt`: Lista de dependencias de Python necesarias.

## ⚙️ Configuración del Entorno

### 1. Variables de Entorno

El archivo `.env` es crucial para la seguridad y la funcionalidad. Debe contener las credenciales necesarias para inicializar el modelo de IA.


Archivo .env

    AZURE_OPENAI_ENDPOINT="TU_ENDPOIN_AQUI"
    AZURE_OPENAI_API_KEY="TU_CLAVE_AQUI"
    AZURE_OPENAI_DEPLOYMENT_NAME="AQUI_TU_DEPLOYMENT"
    AZURE_OPENAI_API_VERSION="AQUI_TU_FECHA_DE_VESION"

2. Instalación de Dependencias
Ejecuta el siguiente comando para instalar todas las librerías necesarias de Python:

```sh
    pip install -r requirements.txt
```

## ▶️ Ejecución de la API
Para iniciar el servidor de la API utilizando Uvicorn:

    uvicorn app.main:app --reload

La API estará disponible en http://localhost:8000(o el puerto que se define en la configuración).

