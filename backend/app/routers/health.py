from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.database.connection import engine

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "mensagem": "API funcionando corretamente!"}


@router.get("/ready")
def readiness_check() -> dict:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível.") from exc
    return {"status": "ready"}
