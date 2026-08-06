from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.empresa import EmpresaCreate, EmpresaResponse, EmpresaUpdate
from app.models.usuario import Usuario
from app.security import require_admin
from app.services import empresa_service


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"],
)


@router.post(
    "/",
    response_model=EmpresaResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_empresa(
    dados: EmpresaCreate,
    db: Session = Depends(get_db),
) -> EmpresaResponse:
    if dados.cnpj and empresa_service.buscar_empresa_por_cnpj(db, dados.cnpj):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma empresa cadastrada com este CNPJ.",
        )

    return empresa_service.criar_empresa(db, dados)


@router.get(
    "/",
    response_model=list[EmpresaResponse],
)
def listar_empresas(
    db: Session = Depends(get_db),
) -> list[EmpresaResponse]:
    return empresa_service.listar_empresas(db)


@router.get(
    "/{empresa_id}",
    response_model=EmpresaResponse,
)
def buscar_empresa(
    empresa_id: UUID,
    db: Session = Depends(get_db),
) -> EmpresaResponse:
    empresa = empresa_service.buscar_empresa_por_id(db, empresa_id)

    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    return empresa


@router.put(
    "/{empresa_id}",
    response_model=EmpresaResponse,
)
def atualizar_empresa(
    empresa_id: UUID,
    dados: EmpresaUpdate,
    usuario_atual: Usuario = Depends(require_admin),
    db: Session = Depends(get_db),
) -> EmpresaResponse:
    if empresa_id != usuario_atual.empresa_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado para esta empresa.")
    empresa = empresa_service.buscar_empresa_por_id(db, empresa_id)

    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    if dados.cnpj and dados.cnpj != empresa.cnpj:
        empresa_com_mesmo_cnpj = empresa_service.buscar_empresa_por_cnpj(
            db,
            dados.cnpj,
        )

        if empresa_com_mesmo_cnpj:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe uma empresa cadastrada com este CNPJ.",
            )

    return empresa_service.atualizar_empresa(db, empresa, dados)


@router.delete(
    "/{empresa_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def excluir_empresa(
    empresa_id: UUID,
    usuario_atual: Usuario = Depends(require_admin),
    db: Session = Depends(get_db),
) -> None:
    if empresa_id != usuario_atual.empresa_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado para esta empresa.")
    empresa = empresa_service.buscar_empresa_por_id(db, empresa_id)

    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada.",
        )

    empresa_service.excluir_empresa(db, empresa)
