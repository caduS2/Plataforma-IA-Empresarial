from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, TokenResponse, UsuarioResponse
from app.security import get_current_user
from app.services import auth_service, usuario_service

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post("/login", response_model=TokenResponse)
def realizar_login(dados: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    usuario = usuario_service.autenticar_usuario(db, str(dados.email), dados.senha)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha invalidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(access_token=auth_service.criar_token_acesso(assunto=str(usuario.id)))


@router.get("/me", response_model=UsuarioResponse)
def usuario_atual(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    return usuario
