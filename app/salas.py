# app/salas.py — primera parte
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.datos import SALAS
from app.esquemas import Sala, SalaActualizar, SalaCrear

router = APIRouter(prefix="/salas", tags=["salas"])


def obtener_sala(codigo: str) -> dict:
    """Devuelve el diccionario de la sala o lanza 404."""
    for sala in SALAS:
        if sala["codigo"] == codigo.upper():
            return sala
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe la sala '{codigo}'",
    )


SalaEncontrada = Annotated[dict, Depends(obtener_sala)]

# app/salas.py — segunda parte: el CRUD


@router.get("", response_model=list[Sala])
def listar_salas(
    piso: Annotated[int | None, Query(ge=1, le=5)] = None,
    solo_es_3d: bool = False,
) -> list[dict]:
    resultado = SALAS
    if piso is not None:
        resultado = [m for m in resultado if m["piso"] == piso]
    if solo_es_3d:
        resultado = [m for m in resultado if m["es_3d"]]
    return resultado


@router.post("", response_model=Sala, status_code=status.HTTP_201_CREATED)
def crear_sala(nueva: SalaCrear) -> dict:
    if any(m["codigo"] == nueva.codigo for m in SALAS):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La sala '{nueva.codigo}' ya existe",
        )
    SALAS.append(nueva.model_dump())
    return SALAS[-1]


@router.get("/{codigo}", response_model=Sala)
def ver_sala(sala: SalaEncontrada) -> dict:
    return sala


@router.put("/{codigo}", response_model=Sala)
def actualizar_sala(cambios: SalaActualizar, sala: SalaEncontrada) -> dict:
    sala.update(cambios.model_dump(exclude_unset=True))
    return sala


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sala(sala: SalaEncontrada) -> None:
    SALAS.remove(sala)