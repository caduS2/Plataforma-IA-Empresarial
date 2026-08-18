from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.usuario import PerfilUsuario


class ConviteCreate(BaseModel):
    email: EmailStr
    perfil: PerfilUsuario = PerfilUsuario.USUARIO


class ConviteAceitar(BaseModel):
    token: str = Field(min_length=20, max_length=96)
    nome: str = Field(min_length=2, max_length=150)
    senha: str = Field(min_length=12, max_length=128)


class ConviteResponse(BaseModel):
    id: UUID
    email: EmailStr
    perfil: PerfilUsuario
    status: str
    expira_em: datetime

    model_config = {"from_attributes": True}
