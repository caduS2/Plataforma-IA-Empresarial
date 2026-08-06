from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse
from app.security import get_current_user


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(
    usuario_atual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Usuario]:
    return list(
        db.scalars(
            select(Usuario)
            .where(Usuario.empresa_id == usuario_atual.empresa_id)
            .order_by(Usuario.nome)
        )
    )
