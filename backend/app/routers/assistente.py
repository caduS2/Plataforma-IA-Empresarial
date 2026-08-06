from __future__ import annotations

import json
import re
import urllib.request
import base64
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db
from app.models.documento import Documento
from app.models.usuario import Usuario
from app.schemas.assistente import FonteResposta, PerguntaAssistente, RespostaAssistente
from app.security import get_current_user


router = APIRouter(prefix="/assistente", tags=["Assistente"])
STOPWORDS = {"a", "ao", "as", "com", "da", "das", "de", "do", "dos", "e", "em", "na", "no", "nos", "o", "os", "para", "por", "que", "um", "uma"}


def termos(texto: str) -> set[str]:
    return {termo for termo in re.findall(r"[\wÀ-ÿ]{3,}", texto.lower()) if termo not in STOPWORDS}


def trecho_relevante(texto: str, palavras: set[str]) -> str:
    frases = re.split(r"(?<=[.!?])\s+|\n+", texto)
    melhor = max(frases, key=lambda frase: len(termos(frase) & palavras), default=texto)
    return melhor.strip()[:500]


def consultar_gemini(pergunta: str, fontes: list[FonteResposta], arquivos: list[Documento] | None = None) -> str | None:
    if not settings.GEMINI_API_KEY:
        return None
    contexto = "\n\n".join(f"[{indice + 1}] {fonte.nome}: {fonte.trecho}" for indice, fonte in enumerate(fontes))
    prompt = (
        "Responda em portugues do Brasil somente com base nas fontes internas abaixo. "
        "Se nao houver evidencia suficiente, diga isso claramente. Nao invente numeros, fatos ou citacoes.\n\n"
        f"Pergunta: {pergunta}\n\nFontes:\n{contexto}"
    )
    partes: list[dict[str, object]] = [{"text": prompt}]
    for documento in (arquivos or [])[:3]:
        caminho = Path(documento.caminho_arquivo)
        if not caminho.exists() or caminho.stat().st_size > 15 * 1024 * 1024:
            continue
        if documento.tipo_mime.startswith("image/") or documento.tipo_mime == "application/pdf":
            partes.append({"inlineData": {"mimeType": documento.tipo_mime, "data": base64.b64encode(caminho.read_bytes()).decode("ascii")}})
    payload = json.dumps({"contents": [{"parts": partes}]}).encode("utf-8")
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read())
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        return None


@router.post("/perguntar", response_model=RespostaAssistente)
def perguntar(
    dados: PerguntaAssistente,
    usuario_atual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> RespostaAssistente:
    palavras = termos(dados.pergunta)
    documentos = list(db.scalars(select(Documento).where(
        Documento.empresa_id == usuario_atual.empresa_id,
        Documento.conteudo_texto.is_not(None),
    )))
    classificados = []
    visuais: list[Documento] = []
    for documento in documentos:
        texto = documento.conteudo_texto or ""
        pontuacao = len(termos(texto) & palavras)
        if pontuacao:
            classificados.append((pontuacao, documento))
        elif documento.tipo_mime.startswith("image/") or documento.tipo_mime == "application/pdf":
            visuais.append(documento)
    classificados.sort(key=lambda item: item[0], reverse=True)
    fontes = [
        FonteResposta(
            documento_id=documento.id,
            nome=documento.nome_original,
            trecho=trecho_relevante(documento.conteudo_texto or "", palavras),
            relevancia=round(pontuacao / max(len(palavras), 1), 2),
        )
        for pontuacao, documento in classificados[:4]
    ]
    if not fontes:
        fontes = [
            FonteResposta(documento_id=documento.id, nome=documento.nome_original, trecho="Arquivo visual ou PDF escaneado analisado pela IA.", relevancia=0.1)
            for documento in visuais[:3]
        ]
    if not fontes:
        return RespostaAssistente(
            resposta="Nao encontrei evidencia suficiente nos documentos desta empresa para responder com seguranca.",
            fontes=[],
            modo="fontes-internas",
        )

    resposta_ia = consultar_gemini(dados.pergunta, fontes, visuais)
    if resposta_ia:
        return RespostaAssistente(resposta=resposta_ia, fontes=fontes, modo="gemini-com-fontes")

    resumo = " ".join(fonte.trecho for fonte in fontes[:2])
    return RespostaAssistente(
        resposta=f"Encontrei estas evidencias nos documentos da empresa: {resumo}",
        fontes=fontes,
        modo="fontes-internas",
    )
