from uuid import UUID

from pydantic import BaseModel, Field


class PerguntaAssistente(BaseModel):
    pergunta: str = Field(min_length=3, max_length=8_000)


class FonteResposta(BaseModel):
    documento_id: UUID
    nome: str
    trecho: str
    relevancia: float


class RespostaAssistente(BaseModel):
    resposta: str
    fontes: list[FonteResposta]
    modo: str
