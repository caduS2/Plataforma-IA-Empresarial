import logging
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.config import Settings
from app.models.usuario import PerfilUsuario
from app.routers.convites import criar_convite
from app.schemas.convite import ConviteAceitar, ConviteCreate
from app.schemas.redefinicao_senha import ConfirmarRedefinicao
from app.scripts.create_admin import normalizar_email, validar_nome
from app.services import demo_service
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


def test_demo_reutiliza_usuario_existente_sem_duplicar() -> None:
    """Acesso demo é idempotente: se o usuário demo já existe, não cria outro."""
    db = MagicMock()
    usuario_existente = SimpleNamespace(id="00000000-0000-0000-0000-0000000000aa")
    db.scalar.return_value = usuario_existente

    with patch.object(demo_service, "criar_token_acesso", return_value="token-demo") as mock_token:
        token = demo_service.entrar_demo(db)

    assert token == "token-demo"
    mock_token.assert_called_once_with(assunto=str(usuario_existente.id))
    # Não deve criar empresa/usuario novos quando já existem.
    db.add.assert_not_called()
    db.commit.assert_not_called()


def test_demo_retorna_token_para_usuario_criado() -> None:
    """Quando o usuário demo não existe, o seed cria empresa+usuário e devolve token."""
    db = MagicMock()
    # Primeiro select (usuário) retorna None; segundo select (empresa) também retorna None.
    db.scalar.side_effect = [None, None]
    db.flush.return_value = None
    db.refresh.side_effect = lambda obj: None

    with (
        patch.object(demo_service, "gerar_hash_senha", return_value="hash"),
        patch.object(demo_service, "criar_token_acesso", return_value="token-demo"),
    ):
        token = demo_service.entrar_demo(db)

    assert token == "token-demo"
    # Empresa e usuário foram adicionados; commit executado.
    assert db.add.call_count == 2
    db.commit.assert_called_once()
