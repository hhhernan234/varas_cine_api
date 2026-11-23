# app/main.py — agrega el import y el include_router
from fastapi import FastAPI

from app.salas import router          # ← nuevo

app = FastAPI(title="API de Salas", version="1.0.0")
app.include_router(router)               # ← nuevo


@app.get("/")
def raiz() -> dict:
    return {"api": "salas", "docs": "/docs"}