import os
from secrets import token_urlsafe

os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://postgres@localhost:5432/nucleo_ai_test")
os.environ.setdefault("JWT_SECRET_KEY", token_urlsafe(48))
