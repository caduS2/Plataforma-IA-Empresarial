from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.schemas.empresa import EmpresaCreate, EmpresaUpdate


def listar_empresas(db: Session) -> list[Empresa]:
    resultado = db.scalars(
        select(Empresa).order_by(Empresa.nome)
    )
    return list(resultado)


def buscar_empresa_por_id(
    db: Session,
    empresa_id: UUID,
) -> Empresa | None:
    return db.get(Empresa, empresa_id)


def buscar_empresa_por_cnpj(
    db: Session,
    cnpj: str,
) -> Empresa | None:
    return db.scalar(
        select(Empresa).where(Empresa.cnpj == cnpj)
    )


def criar_empresa(
    db: Session,
    dados: EmpresaCreate,
) -> Empresa:
    empresa = Empresa(**dados.model_dump())

    db.add(empresa)
    db.commit()
    db.refresh(empresa)

    return empresa


def atualizar_empresa(
    db: Session,
    empresa: Empresa,
    dados: EmpresaUpdate,
) -> Empresa:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(empresa, campo, valor)

    db.commit()
    db.refresh(empresa)

    return empresa


def excluir_empresa(
    db: Session,
    empresa: Empresa,
) -> None:
    db.delete(empresa)
    db.commit()