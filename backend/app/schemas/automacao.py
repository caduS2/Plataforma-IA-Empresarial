from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.assistente import FonteResposta


class GerarAutomacao(BaseModel):
    tipo: Literal["email", "followup", "proposta"]
    contexto: str = Field(min_length=3, max_length=8_000)


class AutomacaoGerada(BaseModel):
    tipo: str
    conteudo: str
    fontes: list[FonteResposta]
    modo: str
