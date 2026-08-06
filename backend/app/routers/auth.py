from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import LoginRequest, TokenResponse, UsuarioCreate, UsuarioResponse
from app.security import get_current_user
from app.services import auth_service, empresa_service, usuario_service


router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post("/cadastro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)) -> UsuarioResponse:
    empresa = empresa_service.buscar_empresa_por_id(db, dados.empresa_id)
    if not empresa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empresa nao encontrada.")

    if usuario_service.buscar_usuario_por_email(db, str(dados.email)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ja existe um usuario cadastrado com este e-mail.")
    return usuario_service.criar_usuario(db, dados)


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
