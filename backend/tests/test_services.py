import logging
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.config import Settings
from app.models.usuario import PerfilUsuario
from app.routers.convites import criar_convite
from app.schemas.convite import ConviteAceitar, ConviteCreate
from app.schemas.redefinicao_senha import ConfirmarRedefinicao
from app.scripts.create_admin import normalizar_email, validar_nome
from app.services.auth_service import criar_token_acesso
from app.services.documento_service import validar_arquivo
from app.services.email_service import enviar_convite


def test_token_jwt_e_criado() -> None:
    assert isinstance(criar_token_acesso("00000000-0000-0000-0000-000000000001"), str)


def test_pdf_invalido_e_rejeitado() -> None:
    with pytest.raises(ValueError, match="inválido"):
        validar_arquivo("arquivo.pdf", "application/pdf", b"nao e pdf")


def test_novas_senhas_exigem_doze_caracteres() -> None:
    with pytest.raises(ValidationError):
        ConviteAceitar(token="t" * 48, nome="Pessoa Teste", senha="curta123")
    with pytest.raises(ValidationError):
        ConfirmarRedefinicao(token="t" * 48, nova_senha="curta123")


def test_cors_com_credenciais_rejeita_curinga() -> None:
    with pytest.raises(ValidationError, match="origens explícitas"):
        Settings(
            _env_file=None,
            DATABASE_URL="postgresql+psycopg://postgres@localhost/nucleo_test",
            JWT_SECRET_KEY="s" * 48,
            CORS_ORIGINS="*",
        )


def test_modo_console_nao_registra_token_de_convite(caplog: pytest.LogCaptureFixture) -> None:
    token = "token-ultrassecreto-de-convite"
    with caplog.at_level(logging.INFO):
        enviar_convite("pessoa@example.com", token)
    assert token not in caplog.text


def test_cli_admin_valida_dados_antes_de_gravar() -> None:
    assert normalizar_email(" ADMIN@EXAMPLE.COM ") == "admin@example.com"
    assert validar_nome(" Empresa Teste ", "Empresa") == "Empresa Teste"
    with pytest.raises(ValueError, match="e-mail válido"):
        normalizar_email("admin@example.invalid")
    with pytest.raises(ValueError, match="entre 2 e 150"):
        validar_nome(" ", "Empresa")


def test_gestor_nao_pode_convidar_administrador() -> None:
    gestor = SimpleNamespace(perfil=PerfilUsuario.GESTOR)
    dados = ConviteCreate(email="novo-admin@example.com", perfil=PerfilUsuario.ADMIN)
    with pytest.raises(HTTPException) as exc_info:
        criar_convite(dados, usuario=gestor, db=SimpleNamespace())  # type: ignore[arg-type]
    assert exc_info.value.status_code == 403
