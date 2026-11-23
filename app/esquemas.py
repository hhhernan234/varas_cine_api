# app/esquemas.py
from pydantic import BaseModel, Field


class SalaBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=60)
    butacas: int = Field(ge=20, le=500)
    piso: int = Field(ge=1, le=5)
    es_3d: bool = False


class SalaCrear(SalaBase):
    # Tres letras mayúsculas + tres dígitos: MAT101, PRG201...
    codigo: str = Field(pattern=r"^[A-Z]{3}\d{3}$")


class SalaActualizar(BaseModel):
    # Todos opcionales: en un PUT parcial, lo que no se envía no se toca.
    nombre: str | None = Field(default=None, min_length=3, max_length=60)
    butacas: int | None = Field(default=None, ge=20, le=500)
    piso: int | None = Field(default=None, ge=1, le=5)
    es_3d: bool | None = None


class Sala(SalaCrear):
    """Lo que la API devuelve: los cinco campos completos."""