from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.convite import Convite
from app.models.documento import Documento
from app.models.usuario import Usuario
from app.schemas.dashboard import DashboardResumo
from app.security import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/resumo", response_model=DashboardResumo)
def obter_resumo(
    usuario: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DashboardResumo:
    empresa_id = usuario.empresa_id
    usuarios = db.scalar(select(func.count()).select_from(Usuario).where(Usuario.empresa_id == empresa_id)) or 0
    documentos = db.scalar(select(func.count()).select_from(Documento).where(Documento.empresa_id == empresa_id)) or 0
    indexados = (
        db.scalar(
            select(func.count())
            .select_from(Documento)
            .where(
                Documento.empresa_id == empresa_id,
                Documento.status == "indexado",
            )
        )
        or 0
    )
    convites = (
        db.scalar(
            select(func.count())
            .select_from(Convite)
            .where(
                Convite.empresa_id == empresa_id,
                Convite.status == "pendente",
            )
        )
        or 0
    )
    return DashboardResumo(
        empresas=1,
        usuarios=usuarios,
        documentos=documentos,
        documentos_indexados=indexados,
        convites_pendentes=convites,
    )
