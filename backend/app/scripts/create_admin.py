"""Cria a primeira empresa e o primeiro administrador de forma explícita."""

import argparse
from getpass import getpass

from pydantic import EmailStr, TypeAdapter, ValidationError
from sqlalchemy import func, select

from app.database.session import SessionLocal
from app.models.empresa import Empresa
from app.models.usuario import PerfilUsuario, Usuario
from app.services.auth_service import gerar_hash_senha

email_adapter = TypeAdapter(EmailStr)


def normalizar_email(value: str) -> str:
    try:
        return str(email_adapter.validate_python(value.strip())).lower()
    except ValidationError as exc:
        raise ValueError("Informe um e-mail válido.") from exc


def validar_nome(value: str, campo: str) -> str:
    value = value.strip()
    if not 2 <= len(value) <= 150:
        raise ValueError(f"{campo} precisa ter entre 2 e 150 caracteres.")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Criar administrador inicial")
    parser.add_argument("--empresa", required=True)
    parser.add_argument("--nome", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--senha", help="Opcional; se omitida, será solicitada sem exibição no terminal.")
    args = parser.parse_args()
    senha = args.senha or getpass("Senha do administrador: ")
    if not args.senha and senha != getpass("Confirme a senha: "):
        parser.error("As senhas não coincidem.")
    if len(senha) < 12:
        parser.error("A senha precisa ter pelo menos 12 caracteres.")
    try:
        email = normalizar_email(args.email)
        nome = validar_nome(args.nome, "O nome")
        empresa_nome = validar_nome(args.empresa, "O nome da empresa")
    except ValueError as exc:
        parser.error(str(exc))

    with SessionLocal() as db:
        if db.scalar(select(Usuario).where(Usuario.email == email)):
            parser.error("Já existe um usuário com este e-mail.")
        empresa = db.scalar(
            select(Empresa).where(func.lower(Empresa.nome) == empresa_nome.lower()).order_by(Empresa.criado_em).limit(1)
        )
        if not empresa:
            empresa = Empresa(nome=empresa_nome)
            db.add(empresa)
            db.flush()
        db.add(
            Usuario(
                nome=nome,
                email=email,
                senha_hash=gerar_hash_senha(senha),
                empresa_id=empresa.id,
                perfil=PerfilUsuario.ADMIN,
            )
        )
        db.commit()
        print(f"Administrador {email} criado para {empresa.nome}.")


if __name__ == "__main__":
    main()
