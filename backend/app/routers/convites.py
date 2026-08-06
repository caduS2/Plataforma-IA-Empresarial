from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import token_urlsafe

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db
from app.models.convite import Convite
from app.models.usuario import Usuario
from app.schemas.convite import ConviteAceitar, ConviteCreate, ConviteResponse
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.security import get_current_user, require_manager
from app.services import email_service, usuario_service


router = APIRouter(prefix="/convites", tags=["Convites"])


@router.get("/", response_model=list[ConviteResponse])
def listar_convites(usuario: Usuario = Depends(require_manager), db: Session = Depends(get_db)) -> list[Convite]:
    return list(db.scalars(select(Convite).where(Convite.empresa_id == usuario.empresa_id).order_by(Convite.criado_em.desc())))


@router.post("/", response_model=ConviteResponse, status_code=status.HTTP_201_CREATED)
def criar_convite(dados: ConviteCreate, usuario: Usuario = Depends(require_manager), db: Session = Depends(get_db)) -> Convite:
    email = str(dados.email).lower()
    if usuario_service.buscar_usuario_por_email(db, email):
        raise HTTPException(status_code=409, detail="Este e-mail ja possui acesso.")
    agora = datetime.now(timezone.utc)
    db.execute(update(Convite).where(Convite.empresa_id == usuario.empresa_id, Convite.email == email, Convite.status == "pendente").values(status="cancelado"))
    token = token_urlsafe(48)
    convite = Convite(empresa_id=usuario.empresa_id, email=email, perfil=dados.perfil, token_hash=sha256(token.encode()).hexdigest(), expira_em=agora + timedelta(days=settings.INVITE_EXPIRE_DAYS))
    db.add(convite); db.commit(); db.refresh(convite)
    email_service.enviar_convite(email, token)
    return convite


@router.post("/{convite_id}/cancelar", response_model=ConviteResponse)
def cancelar_convite(convite_id: str, usuario: Usuario = Depends(require_manager), db: Session = Depends(get_db)) -> Convite:
    convite = db.scalar(select(Convite).where(Convite.id == convite_id, Convite.empresa_id == usuario.empresa_id))
    if not convite or convite.status != "pendente":
        raise HTTPException(status_code=404, detail="Convite pendente não encontrado.")
    convite.status = "cancelado"; db.commit(); db.refresh(convite)
    return convite


@router.post("/{convite_id}/reenviar", response_model=ConviteResponse)
def reenviar_convite(convite_id: str, usuario: Usuario = Depends(require_manager), db: Session = Depends(get_db)) -> Convite:
    convite = db.scalar(select(Convite).where(Convite.id == convite_id, Convite.empresa_id == usuario.empresa_id, Convite.status == "pendente"))
    if not convite:
        raise HTTPException(status_code=404, detail="Convite pendente não encontrado.")
    token = token_urlsafe(48)
    convite.token_hash = sha256(token.encode()).hexdigest()
    convite.expira_em = datetime.now(timezone.utc) + timedelta(days=settings.INVITE_EXPIRE_DAYS)
    db.commit(); db.refresh(convite)
    email_service.enviar_convite(convite.email, token)
    return convite


@router.post("/aceitar", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def aceitar_convite(dados: ConviteAceitar, db: Session = Depends(get_db)) -> Usuario:
    convite = db.scalar(select(Convite).where(Convite.token_hash == sha256(dados.token.encode()).hexdigest(), Convite.status == "pendente"))
    if not convite or convite.expira_em < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Convite invalido ou expirado.")
    if usuario_service.buscar_usuario_por_email(db, convite.email):
        raise HTTPException(status_code=409, detail="Este e-mail ja possui acesso.")
    novo_usuario = usuario_service.criar_usuario(db, UsuarioCreate(nome=dados.nome, email=convite.email, senha=dados.senha, empresa_id=convite.empresa_id))
    novo_usuario.perfil = convite.perfil
    convite.status = "aceito"
    db.commit(); db.refresh(novo_usuario)
    return novo_usuario
