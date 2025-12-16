from typing import List, Optional  # 🔑 Añadimos Optional para 'framework'

from pydantic import BaseModel, Field


# Esquema del input
class ChatRequest(BaseModel):
    """Estructura para la solicitud de chat del usuario."""

    prompt: str = Field(description="La pregunta o requerimiento técnico del usuario.")


# MODELO DE SALIDA ESTRUCTURADA
class CodeSnippet(BaseModel):
    """Estructura para representar un único fragmento de código."""

    lenguaje: str = Field(
        description="Lenguaje de programación o tipo de archivo (ej: 'python', 'javascript', 'sql', 'yaml')."
    )
    nombre_archivo: str = Field(
        description="Nombre propuesto para el archivo que contiene este código (ej: 'main.py', 'user_model.ts')."
    )
    codigo: str = Field(
        description="El fragmento de código completo, limpio y listo para usar."
    )


class SoftwareSolution(BaseModel):
    """Estructura completa para la solución de software generada por la IA, ajustada para el frontend."""

    nombre: str = Field(
        description="Nombre descriptivo o título breve para el proyecto/solución (ej: 'Calculadora CLI')."
    )
    lenguaje: str = Field(
        description="Lenguaje de programación principal de la solución (ej: 'Python')."
    )
    framework: Optional[str] = Field(
        None,
        description="Framework o librería principal utilizada (ej: 'FastAPI', 'React', si aplica).",
    )

    explicacion: str = Field(
        description="Explicación detallada de la solución, la lógica de diseño y los principios utilizados."
    )

    codigo: str = Field(
        description="El código fuente del archivo principal, para mostrar en el SyntaxHighlighter."
    )

    archivos: List[str] = Field(
        description="Lista de los NOMBRES de los archivos que componen la solución (ej: ['main.py', 'settings.py', 'router.py'])."
    )

    dependencias: List[str] = Field(
        description="Lista de dependencias, librerías o paquetes externos que deben instalarse."
    )
    comando_ejecucion: str = Field(
        description="Comando de ejemplo para ejecutar o probar la solución (ej: 'python main.py' o 'npm run start')."
    )
