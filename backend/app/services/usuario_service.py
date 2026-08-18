from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.services.auth_service import gerar_hash_senha, verificar_senha


def buscar_usuario_por_email(
    db: Session,
    email: str,
) -> Usuario | None:
    return db.scalar(select(Usuario).where(Usuario.email == email.lower()))


def criar_usuario(
    db: Session,
    dados: UsuarioCreate,
) -> Usuario:
    usuario = Usuario(
        nome=dados.nome,
        email=str(dados.email).lower(),
        senha_hash=gerar_hash_senha(dados.senha),
        empresa_id=dados.empresa_id,
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def autenticar_usuario(
    db: Session,
    email: str,
    senha: str,
) -> Usuario | None:
    usuario = buscar_usuario_por_email(db, email)

    if not usuario or not usuario.ativo:
        return None

    if not verificar_senha(senha, usuario.senha_hash):
        return None

    return usuario
