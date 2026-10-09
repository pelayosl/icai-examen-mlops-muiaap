from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator
import pandas as pd

class Entrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_paquete: str = Field(min_length=1)
    peso_kg: float = Field(gt=0, le=30)
    distancia_km: float = Field(ge=0, le=200)

    @field_validator("id_paquete", mode="before")
    @classmethod
    def check_id(cls, value: object) -> object:
        if value is None or pd.isna(value):
            raise ValueError("El ID del paquete no puede ser nulo")
        if not isinstance(value, str):
            return value

        value = value.strip()
        if not value:
            raise ValueError("El ID del paquete no puede estar vacío")
        return value

class Salida(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id_paquete: str = Field(min_length=1)
    categoria: Literal["normal", "urgente"]
    confianza: float = Field(ge=0, le=1)

    @field_validator("id_paquete", mode="before")
    @classmethod
    def check_id(cls, value: object) -> object:
        if value is None or pd.isna(value):
            raise ValueError("El ID del paquete no puede ser nulo")
        if not isinstance(value, str):
            return value

        value = value.strip()
        if not value:
            raise ValueError("El ID del paquete no puede estar vacío")
        return value
