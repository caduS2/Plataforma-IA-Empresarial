from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.usuario import PerfilUsuario


class UsuarioCreate(BaseModel):
    nome: str = Field(
        min_length=2,
        max_length=150,
        examples=["Maria Silva"],
    )
    email: EmailStr = Field(
        examples=["maria@empresa.com"],
    )
    senha: str = Field(
        min_length=8,
        max_length=128,
        examples=["SenhaSegura123!"],
    )
    empresa_id: UUID


class UsuarioResponse(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    perfil: PerfilUsuario
    ativo: bool
    empresa_id: UUID
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(
        min_length=8,
        max_length=128,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"