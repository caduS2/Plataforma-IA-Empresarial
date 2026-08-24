"""Serviço de demonstração (Recruiter Demo Mode).

Cria (de forma idempotente) um tenant e um usuário de demonstração isolados,
sem expor nenhuma conta administrativa real. O usuário demo tem perfil
limitado (``usuario``) e pertence a uma empresa própria ("Núcleo Demo"),
portanto nunca enxerga dados de outras empresas.
"""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.empresa import Empresa
from app.models.usuario import PerfilUsuario, Usuario
from app.services.auth_service import criar_token_acesso, gerar_hash_senha

DEMO_EMPRESA_NOME = "Núcleo Demo"
DEMO_USUARIO_EMAIL = "demo@nucleo.ai"
DEMO_USUARIO_NOME = "Visitante Demo"
# Senha usada apenas para o seed interno do tenant demo. Não é secret de
# produção; o acesso demo ocorre via endpoint dedicado, não pela tela de login.
DEMO_USUARIO_SENHA = "NucleoDemo@2026"


def _garantir_demo(db: Session) -> Usuario:
    """Cria o tenant/usuário demo caso ainda não existam (idempotente)."""
    usuario = db.scalar(select(Usuario).where(Usuario.email == DEMO_USUARIO_EMAIL))
    if usuario:
        return usuario

    empresa = db.scalar(
        select(Empresa)
        .where(func.lower(Empresa.nome) == DEMO_EMPRESA_NOME.lower())
        .order_by(Empresa.criado_em)
        .limit(1)
    )
    if not empresa:
        empresa = Empresa(nome=DEMO_EMPRESA_NOME)
        db.add(empresa)
        db.flush()

    usuario = Usuario(
        nome=DEMO_USUARIO_NOME,
        email=DEMO_USUARIO_EMAIL,
        senha_hash=gerar_hash_senha(DEMO_USUARIO_SENHA),
        empresa_id=empresa.id,
        perfil=PerfilUsuario.USUARIO,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def entrar_demo(db: Session) -> str:
    """Garante o acesso demo e retorna um token de acesso JWT."""
    usuario = _garantir_demo(db)
    return criar_token_acesso(assunto=str(usuario.id))
