from enum import Enum
from pydantic import BaseModel, Field, field_validator


class Criticidad(str, Enum):
    BAJA = "baja"
    MEDIA = "media"
    ALTA = "alta"


class ExtraccionTecnica(BaseModel):
    tecnologias: list[str] = Field(description="Tecnologías mencionadas en el texto")
    nivel_de_criticidad: Criticidad = Field(description="Criticidad: baja, media o alta")
    resumen_tecnico: str = Field(description="Resumen técnico breve en español")

    @field_validator("tecnologias")
    @classmethod
    def validar_tecnologias(cls, value: list[str]) -> list[str]:
        if not value or any(not item.strip() for item in value):
            raise ValueError("Debe existir al menos una tecnología identificable")
        return value

    @field_validator("resumen_tecnico")
    @classmethod
    def validar_resumen(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El resumen no puede estar vacío")
        return value
