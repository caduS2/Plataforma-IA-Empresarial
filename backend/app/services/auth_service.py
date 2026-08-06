from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash

from app.config import settings


password_hash = PasswordHash.recommended()


def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(
    senha: str,
    senha_hash: str,
) -> bool:
    return password_hash.verify(senha, senha_hash)


def criar_token_acesso(
    assunto: str,
    expires_delta: timedelta | None = None,
) -> str:
    expiracao = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: dict[str, Any] = {
        "sub": assunto,
        "exp": expiracao,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )