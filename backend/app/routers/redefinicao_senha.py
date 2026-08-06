from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import token_urlsafe

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db
from app.models.redefinicao_senha import RedefinicaoSenha
from app.schemas.redefinicao_senha import ConfirmarRedefinicao, MensagemRedefinicao, SolicitarRedefinicao
from app.services import email_service, usuario_service
from app.services.auth_service import gerar_hash_senha


router = APIRouter(prefix="/senha", tags=["Recuperacao de senha"])
MENSAGEM_PADRAO = "Se houver uma conta com este e-mail, as instrucoes de recuperacao serao enviadas."


@router.post("/solicitar-redefinicao", response_model=MensagemRedefinicao)
def solicitar_redefinicao(dados: SolicitarRedefinicao, db: Session = Depends(get_db)) -> MensagemRedefinicao:
    usuario = usuario_service.buscar_usuario_por_email(db, str(dados.email))
    if usuario and usuario.ativo:
        agora = datetime.now(timezone.utc)
        db.execute(
            update(RedefinicaoSenha)
            .where(RedefinicaoSenha.usuario_id == usuario.id, RedefinicaoSenha.usado_em.is_(None))
            .values(usado_em=agora)
        )
        token = token_urlsafe(48)
        registro = RedefinicaoSenha(
            usuario_id=usuario.id,
            token_hash=sha256(token.encode()).hexdigest(),
            expira_em=agora + timedelta(minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES),
        )
        db.add(registro)
        db.commit()
        email_service.enviar_redefinicao_senha(usuario.email, token)
    return MensagemRedefinicao(mensagem=MENSAGEM_PADRAO)


@router.post("/confirmar-redefinicao", response_model=MensagemRedefinicao)
def confirmar_redefinicao(dados: ConfirmarRedefinicao, db: Session = Depends(get_db)) -> MensagemRedefinicao:
    token_hash = sha256(dados.token.encode()).hexdigest()
    registro = db.scalar(select(RedefinicaoSenha).where(RedefinicaoSenha.token_hash == token_hash, RedefinicaoSenha.usado_em.is_(None)))
    if not registro or registro.expira_em < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Link de redefinicao invalido ou expirado.")
    usuario = db.get(__import__("app.models.usuario", fromlist=["Usuario"]).Usuario, registro.usuario_id)
    usuario.senha_hash = gerar_hash_senha(dados.nova_senha)
    registro.usado_em = datetime.now(timezone.utc)
    db.commit()
    return MensagemRedefinicao(mensagem="Senha redefinida com sucesso.")
