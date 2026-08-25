from sqlalchemy import select

from app.database.session import SessionLocal
from app.models.empresa import Empresa
from app.models.usuario import PerfilUsuario, Usuario
from app.services.auth_service import gerar_hash_senha

E2E_EMPRESA_NOME = "Nucleo AI E2E"
E2E_EMAIL = "admin@demo.com"
E2E_SENHA = "DemoSenha@123"


def seed_e2e() -> None:
    db = SessionLocal()

    try:
        empresa = db.scalar(select(Empresa).where(Empresa.nome == E2E_EMPRESA_NOME))

        if empresa is None:
            empresa = Empresa(
                nome=E2E_EMPRESA_NOME,
                ativa=True,
            )
            db.add(empresa)
            db.flush()

        usuario = db.scalar(select(Usuario).where(Usuario.email == E2E_EMAIL))

        if usuario is None:
            usuario = Usuario(
                nome="Administrador E2E",
                email=E2E_EMAIL,
                senha_hash=gerar_hash_senha(E2E_SENHA),
                perfil=PerfilUsuario.ADMIN,
                ativo=True,
                empresa_id=empresa.id,
            )
            db.add(usuario)
        else:
            usuario.nome = "Administrador E2E"
            usuario.senha_hash = gerar_hash_senha(E2E_SENHA)
            usuario.perfil = PerfilUsuario.ADMIN
            usuario.ativo = True
            usuario.empresa_id = empresa.id

        db.commit()

        print(f"Usuario E2E pronto: {E2E_EMAIL}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_e2e()
