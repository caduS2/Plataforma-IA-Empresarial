from pydantic import BaseModel, EmailStr, Field


class SolicitarRedefinicao(BaseModel):
    email: EmailStr


class ConfirmarRedefinicao(BaseModel):
    token: str = Field(min_length=20, max_length=96)
    nova_senha: str = Field(min_length=8, max_length=128)


class MensagemRedefinicao(BaseModel):
    mensagem: str
