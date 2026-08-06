from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class EmpresaBase(BaseModel):
    nome: str = Field(
        min_length=2,
        max_length=150,
        examples=["Empresa Exemplo Ltda."],
    )
    cnpj: str | None = Field(
        default=None,
        min_length=14,
        max_length=14,
        examples=["12345678000199"],
    )


class EmpresaCreate(EmpresaBase):
    pass


class EmpresaUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )
    cnpj: str | None = Field(
        default=None,
        min_length=14,
        max_length=14,
    )
    ativa: bool | None = None


class EmpresaResponse(EmpresaBase):
    id: UUID
    ativa: bool
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)