from collections.abc import Generator

from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.database.connection import engine


class Base(DeclarativeBase):
    """Classe base para todos os modelos do banco de dados."""


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """
    Fornece uma sessão do banco para cada requisição
    e garante seu fechamento ao final.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
