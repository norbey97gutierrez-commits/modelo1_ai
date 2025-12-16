from typing import List, Optional  # 🔑 Añadimos Optional para 'framework'

from pydantic import BaseModel, Field

# ===============================================
# 1. ESQUEMA DE ENTRADA (Input Model)
# ===============================================


class ChatRequest(BaseModel):
    """Estructura para la solicitud de chat del usuario."""

    prompt: str = Field(description="La pregunta o requerimiento técnico del usuario.")


# ===============================================
# 2. MODELO DE SALIDA ESTRUCTURADA (Output Model)
# ===============================================


# ⚠️ La clase CodeSnippet ya no es necesaria si solo reportamos
# el código principal en el campo 'codigo' y los nombres en 'archivos'.
# Si la IA necesita generar múltiples archivos complejos, la mantenemos,
# pero simplificaremos 'SoftwareSolution' para el frontend.
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

    # 🔑 CAMPOS NUEVOS/RENOMBRADOS REQUERIDOS POR EL FRONTEND:
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

    # 🔑 RENOMBRADO: 'explicacion_tecnica' -> 'explicacion'
    explicacion: str = Field(
        description="Explicación detallada de la solución, la lógica de diseño y los principios utilizados."
    )

    # 🔑 NUEVO CAMPO PARA EL CÓDIGO PRINCIPAL:
    codigo: str = Field(
        description="El código fuente del archivo principal, para mostrar en el SyntaxHighlighter."
    )

    # 🔑 AJUSTADO: 'archivos_codigo' -> 'archivos' (para coincidir con solucion.archivos?.length)
    # Ya que el código principal va en 'codigo', esta lista contendrá los nombres de los archivos secundarios.
    archivos: List[str] = Field(
        description="Lista de los NOMBRES de los archivos que componen la solución (ej: ['main.py', 'settings.py', 'router.py'])."
    )

    # CAMPOS ORIGINALES:
    dependencias: List[str] = Field(
        description="Lista de dependencias, librerías o paquetes externos que deben instalarse."
    )
    comando_ejecucion: str = Field(
        description="Comando de ejemplo para ejecutar o probar la solución (ej: 'python main.py' o 'npm run start')."
    )
