# 🐍 Asistente de IA Experto en Python

## 📜 Descripción del Proyecto

Este proyecto es una aplicación web de chat que funciona como un asistente conversacional especializado en el lenguaje de programación Python.

El sistema está dividido en dos partes:

    1. Frontend (React+vitae): Interfaz de usuario moderna y responsiva.

    2. Backend (Python/Uvicorn/FastAPI): Servidor API que maneja la lógica de la inteligencia artificial y genera respuestas a las consultas.

## 🛠️ Requisitos previos

Antes de comenzar, asegúrese de tener instalado lo siguiente:

    Node.js y npm/yarn: Para ejecutar la aplicación React (Frontend).

    Python (3.8+): Para ejecutar la API del servidor (Backend).

    pip (o pipenv/poetry): Para gestionar las dependencias de Python.


## 🚀 Instalación y configuración

El proyecto se estructura en dos directorios principales ( frontend-ia y backend ). Debes instalar las dependencias por separado para cada uno.

1. Configuración del backend (API de Python)
El backend exponen el endpoint /generateque será consumido por el frontend.

    1. Navegar al directorio del Backend:

    ```sh
    cd backend/
    ```

    2. Instalar dependencias de Python:

        Si usas pip:

        ```sh
        pip install -r requirements.txt
        ```
    3. Configurar Variables de Entorno (Opcional pero recomendado):

        Crea un archivo .enven el directorio raíz del backend y define variables sensibles (ej., claves API, URL de bases de datos, etc.).

2. Configuración del Frontend (Aplicación React)
El frontend contiene el código de la interfaz de usuario.

    1. Navegar al directorio del Frontend:

    ```sh
        cd frontend/
        cd frontend-ia/
    ```

    2. Instalar dependencias de Node:

    ```sh
        npm install 
    ```

    3. Asegurar la conexión al Backend:

    Asegúrese de que la URL del backend en el archivo useChatLogic.js sea correcta (por defecto http://localhost:8000/generate).


## ▶️ Ejecución de la Aplicación

Para que la aplicación funcione completamente, debes ejecutar el backend y el frontend simultáneamente en dos terminales separados.

### Paso 1: Iniciar el Servidor del Backend
    Abra la primera terminal y navegue al directorio del backend ( backend/ ).

    Ejecuta el servidor (el comando exacto puede variar según el framework que uses, como FastAPI):

    ```sh
        uvicorn main:app --reload --port 8000
    ```
    (Verifique la documentación de su servidor si el comando es diferente.)

### Paso 2: Iniciar el Servidor de Desarrollo del Frontend

    1. Abra la segunda terminal y navegue al directorio del frontend ( frontend/frontend-ia/).
    2. Ejecuta el comando de desarrollo de React (usando Vite o Create React App):

    ```sh
        npm run dev
    ```
    3. Acceder a la Aplicación:
    La aplicación React estará disponible en tu navegador, generalmente en: http://localhost:5173/(o el puerto que indica tu terminal).

## 📁 Estructura del Proyecto

La aplicación sigue una arquitectura limpia para la fácil escalabilidad:

| Directorio/Archivo               | Descripción                                                             |
|----------------------------------|-------------------------------------------------------------------------|
| 📂 `backend-id/`                 | Servidor API, lógica de IA y modelos                                    |
| 📂 `frontend-id/`                | Aplicación React                                                        |
| 📄 `frontend-id/src/App.jsx`     | Componente principal - contenedor de diseño                             |
| 📂 `frontend-id/src/hooks/`      | Custom Hooks (`useChatLogic.js`)                                        |
| 📂 `frontend-id/src/components/` | Componentes UI (`Mensaje.jsx`, `ChatInput.jsx`, etc.)                   |
| 🎨 `frontend-id/src/App.css`     | Estilos globales y variables CSS                                        |


├── 📂 backend-id/           # Servidor API, lógica IA y modelos
├── 📂 frontend-id/          # Aplicación React
│   ├── 📄 src/App.jsx       # Componente principal
│   ├── 📂 src/hooks/        # Custom Hooks
│   ├── 📂 src/components/   # Componentes UI
│   └── 🎨 src/App.css       # Estilos globales

## 🎨 Características adicionales

    Diseño Oscuro (Dark Mode): Interfaz optimizada para ambientes de poca luz.

    Diseño Modular: Componentes separados para alta mantenibilidad.

    Scroll Automático: La conversación se desplaza automáticamente al recibir una nueva respuesta.

    Manejo de Carga: Indicadores de "Cargando..." y manejo de errores de conexión.

