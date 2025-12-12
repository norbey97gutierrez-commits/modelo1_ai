from typing import List

from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    prompt: str


# Esquema de Salida para DESARROLLO DE SOFTWARE UNIVERSAL
class SoftwareSolution(BaseModel):
    """
    Define el esquema para una solución de software completa.
    """

    proyecto_nombre: str = Field(
        description="Nombre breve del módulo o funcionalidad desarrollada."
    )
    lenguaje: str = Field(
        description="Lenguaje de programación utilizado (ej. Python, Rust, TypeScript)."
    )
    framework: str = Field(
        description="Framework utilizado o 'None' si es código puro."
    )
    estructura_archivos: List[str] = Field(
        description="Lista de archivos necesarios para implementar la solución."
    )
    codigo_principal: str = Field(
        description="El código fuente principal generado. Debe ser código crudo, listo para guardar."
    )
    explicacion_tecnica: str = Field(
        description="Explicación detallada de la arquitectura y lógica utilizada."
    )
    dependencias: List[str] = Field(
        description="Lista de librerías o paquetes externos necesarios (ej. npm install X, pip install Y)."
    )
