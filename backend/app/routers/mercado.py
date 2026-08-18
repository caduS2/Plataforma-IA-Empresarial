from __future__ import annotations

import csv
import io
import json
import urllib.parse
import urllib.request
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query

from app.config import settings
from app.models.usuario import Usuario
from app.schemas.mercado import EmpresaCvm, EmpresaUsa, FonteExterna, IndicadorMacro, PontoIndicador
from app.security import get_current_user

router = APIRouter(prefix="/mercado", tags=["Dados de mercado"])
INDICADORES = {
    "selic": ("432", "Taxa Selic"),
    "ipca": ("433", "IPCA - variacao mensal"),
    "cambio": ("1", "Cambio - dolar americano"),
}


def carregar_json(url: str, headers: dict[str, str] | None = None) -> object:
    request = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read())


@router.get("/fontes", response_model=list[FonteExterna])
def listar_fontes(_: Usuario = Depends(get_current_user)) -> list[FonteExterna]:
    return [
        FonteExterna(
            nome="Banco Central do Brasil",
            tipo="Indicadores macroeconomicos",
            url="https://www.bcb.gov.br/estatisticas",
            atualizacao="Conforme a serie",
        ),
        FonteExterna(
            nome="CVM Dados Abertos",
            tipo="Companhias abertas e fundos",
            url="https://dados.cvm.gov.br/",
            atualizacao="Diaria ou periodica",
        ),
        FonteExterna(
            nome="SEC EDGAR",
            tipo="Empresas listadas nos EUA",
            url="https://www.sec.gov/edgar",
            atualizacao="Conforme novos filings",
        ),
    ]


@router.get("/indicadores/{indicador}", response_model=IndicadorMacro)
def consultar_indicador(
    indicador: str,
    limite: int = Query(default=30, ge=1, le=365),
    _: Usuario = Depends(get_current_user),
) -> IndicadorMacro:
    if indicador not in INDICADORES:
        raise HTTPException(status_code=404, detail="Indicador nao suportado.")
    codigo, nome = INDICADORES[indicador]
    try:
        dados = carregar_json(
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados/ultimos/{limite}?formato=json"
        )
        pontos = [
            PontoIndicador(
                data=datetime.strptime(item["data"], "%d/%m/%Y").date(), valor=float(item["valor"].replace(",", "."))
            )
            for item in dados
        ]
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Nao foi possivel consultar o Banco Central agora.") from exc
    return IndicadorMacro(
        codigo=codigo,
        nome=nome,
        fonte="Banco Central do Brasil (SGS)",
        atualizado_em=pontos[-1].data if pontos else None,
        pontos=pontos,
    )


@router.get("/cvm/empresas", response_model=list[EmpresaCvm])
def buscar_empresa_cvm(
    consulta: str = Query(min_length=2, max_length=100),
    _: Usuario = Depends(get_current_user),
) -> list[EmpresaCvm]:
    try:
        catalogo = carregar_json("https://dados.cvm.gov.br/api/3/action/package_show?id=cia_aberta-cad")
        recursos = catalogo["result"]["resources"]
        csv_url = next(recurso["url"] for recurso in recursos if recurso["url"].endswith(".csv"))
        with urllib.request.urlopen(csv_url, timeout=30) as response:
            conteudo = response.read().decode("latin-1")
        termo = consulta.lower()
        encontrados = []
        for linha in csv.DictReader(io.StringIO(conteudo), delimiter=";"):
            nome = linha.get("DENOM_SOCIAL", "")
            cnpj = linha.get("CNPJ_CIA", "")
            if termo in nome.lower() or termo in cnpj.replace(".", "").replace("/", "").replace("-", ""):
                encontrados.append(EmpresaCvm(cnpj=cnpj, nome=nome, situacao=linha.get("SIT")))
            if len(encontrados) == 10:
                break
        return encontrados
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Nao foi possivel consultar a CVM agora.") from exc


@router.get("/sec/empresa/{cik}", response_model=EmpresaUsa)
def consultar_empresa_sec(cik: str, _: Usuario = Depends(get_current_user)) -> EmpresaUsa:
    if not settings.SEC_USER_AGENT:
        raise HTTPException(
            status_code=503, detail="A fonte SEC precisa de um identificador de contato configurado antes do uso."
        )
    codigo = cik.zfill(10)
    try:
        dados = carregar_json(
            f"https://data.sec.gov/submissions/CIK{codigo}.json",
            headers={"User-Agent": settings.SEC_USER_AGENT, "Accept-Encoding": "gzip, deflate"},
        )
        return EmpresaUsa(
            cik=codigo,
            nome=dados["name"],
            ticker=(dados.get("tickers") or [None])[0],
            descricao=dados.get("sicDescription"),
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Nao foi possivel consultar a SEC agora.") from exc
