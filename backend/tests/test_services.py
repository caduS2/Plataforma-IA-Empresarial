import pytest

from app.services.auth_service import criar_token_acesso
from app.services.documento_service import validar_arquivo


def test_token_jwt_e_criado() -> None:
    assert isinstance(criar_token_acesso("00000000-0000-0000-0000-000000000001"), str)


def test_pdf_invalido_e_rejeitado() -> None:
    with pytest.raises(ValueError, match="inválido"):
        validar_arquivo("arquivo.pdf", "application/pdf", b"nao e pdf")
