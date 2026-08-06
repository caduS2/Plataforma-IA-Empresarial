from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db
from app.models.documento import Documento
from app.models.usuario import Usuario
from app.schemas.documento import DocumentoResponse
from app.security import get_current_user
from app.services.documento_service import extrair_texto, validar_arquivo

router = APIRouter(prefix="/documentos", tags=["Documentos"])
MAX_FILE_SIZE = 50 * 1024 * 1024


@router.get("/", response_model=list[DocumentoResponse])
def listar_documentos(
    usuario_atual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Documento]:
    return list(db.scalars(select(Documento).where(Documento.empresa_id == usuario_atual.empresa_id).order_by(Documento.criado_em.desc())))


@router.post("/upload", response_model=DocumentoResponse, status_code=status.HTTP_201_CREATED)
async def enviar_documento(
    arquivo: UploadFile = File(...),
    usuario_atual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Documento:
    content = await arquivo.read()
    if not content:
        raise HTTPException(status_code=400, detail="O arquivo está vazio.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="O arquivo excede 50 MB.")
    nome_original = Path(arquivo.filename or "arquivo").name[:255]
    try:
        suffix = validar_arquivo(nome_original, arquivo.content_type, content)
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    texto_extraido = extrair_texto(nome_original, content)
    safe_name = f"{uuid4()}{suffix}"
    directory = Path(settings.UPLOAD_DIR) / str(usuario_atual.empresa_id)
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / safe_name
    destination.write_bytes(content)
    status_processamento = "indexado" if texto_extraido else "aguardando_ocr"
    documento = Documento(empresa_id=usuario_atual.empresa_id, usuario_id=usuario_atual.id, nome_original=nome_original, caminho_arquivo=str(destination), tipo_mime=arquivo.content_type or "application/octet-stream", tamanho_bytes=len(content), status=status_processamento, conteudo_texto=texto_extraido)
    db.add(documento)
    db.commit()
    db.refresh(documento)
    return documento
