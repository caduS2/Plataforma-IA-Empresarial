from datetime import date

from pydantic import BaseModel


class PontoIndicador(BaseModel):
    data: date
    valor: float


class IndicadorMacro(BaseModel):
    codigo: str
    nome: str
    fonte: str
    atualizado_em: date | None
    pontos: list[PontoIndicador]


class FonteExterna(BaseModel):
    nome: str
    tipo: str
    url: str
    atualizacao: str


class EmpresaCvm(BaseModel):
    cnpj: str
    nome: str
    situacao: str | None = None


class EmpresaUsa(BaseModel):
    cik: str
    nome: str
    ticker: str | None = None
    descricao: str | None = None
