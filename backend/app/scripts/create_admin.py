"""Cria a primeira empresa e o primeiro administrador de forma explícita."""

import argparse
from getpass import getpass

from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.empresa import Empresa
from app.models.usuario import PerfilUsuario, Usuario
from app.services.auth_service import gerar_hash_senha


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

    with SessionLocal() as db:
        email = args.email.strip().lower()
        if db.scalar(select(Usuario).where(Usuario.email == email)):
            parser.error("Já existe um usuário com este e-mail.")
        empresa = Empresa(nome=args.empresa.strip())
        db.add(empresa)
        db.flush()
        db.add(
            Usuario(
                nome=args.nome.strip(),
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
