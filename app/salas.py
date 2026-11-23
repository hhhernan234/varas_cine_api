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

# app/materias.py — ¡ANTES de la ruta /{codigo}!

@router.get("/aforo")
def aforo(
    funciones: Annotated[int, Query(ge=1, le=12)],
    piso: Annotated[int | None, Query(ge=1, le=5)] = None,
) -> dict:
    seleccion = [sala for sala in SALAS if piso is None or sala["piso"] == piso]
    if not seleccion:
        raise HTTPException(404, f"No hay salas en el piso {piso}")
    butacas = sum(sala["butacas"] for sala in seleccion)
    aforo_vendible = sum(sala["butacas"] * 9 // 10 for sala in seleccion) * funciones
    salas_3d = sum(1 for sala in seleccion if sala["es_3d"])
    return {
        "salas": len(seleccion),
        "funciones": funciones,
        "butacas_promedio": round(butacas / len(seleccion), 2),
        "aforo_total": butacas * funciones,
        "aforo_vendible": aforo_vendible,
        "porcentaje_3d": round(salas_3d * 100 / len(seleccion), 1),
    }

# app/materias.py — también ANTES de la ruta /{codigo}


@router.get("/avance")
def mantenimiento(en_mantenimiento: Annotated[list[str] | None, Query()] = None) -> dict:
    codigos = {c.upper() for c in (en_mantenimiento or [])}
    if not SALAS:
        raise HTTPException(404, "No hay salas")
    total = fuera_de_servicio 
    fuera_de_servicio= operativas 
    operativas = aforo_operativo 
    aforo_operativo= 0
    sala_operativa_mayor = None
    butacas_mayor = 0
    for sala in SALAS:
        if sala["codigo"] in codigos:
            fuera_de_servicio += 1
        else:
            operativas += 1
            aforo_operativo += sala["butacas"]
    return {
        "total": total,
        "en_mantenimiento": fuera_de_servicio,
        "operativas": operativas,
        "aforo_operativo": aforo_operativo,
        "sala_operativa_mayor": sala_operativa_mayor,
    }


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