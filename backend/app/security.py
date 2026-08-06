from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database.session import get_db
from app.models.usuario import PerfilUsuario, Usuario


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Usuario:
    """Resolve the active user from a valid Bearer token."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = UUID(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessao invalida ou expirada.",
        ) from exc

    user = db.get(Usuario, user_id)
    if not user or not user.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessao invalida ou expirada.",
        )
    return user


def require_manager(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.perfil not in {PerfilUsuario.ADMIN, PerfilUsuario.GESTOR}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissao de gestor necessaria.")
    return user


def require_admin(user: Usuario = Depends(get_current_user)) -> Usuario:
    if user.perfil is not PerfilUsuario.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão de administrador necessária.")
    return user
