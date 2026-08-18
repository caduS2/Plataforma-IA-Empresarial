from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PORT: int = 8000
    DEBUG: bool = False
    APP_NAME: str = "Nucleo AI API"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30
    INVITE_EXPIRE_DAYS: int = 7
    FRONTEND_URL: str = "http://localhost:3000"
    EMAIL_MODE: str = "console"
    EMAIL_FROM: str = "noreply@localhost"
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_STARTTLS: bool = True
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    UPLOAD_DIR: str = "uploads"
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-3.5-flash"
    SEC_USER_AGENT: str | None = None
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    RATE_LIMIT_WINDOW_SECONDS: int = 60
    RATE_LIMIT_AUTH_REQUESTS: int = 10
    RATE_LIMIT_AI_REQUESTS: int = 20

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validar_chave_jwt(cls, value: str) -> str:
        if len(value) < 32 or value.startswith("GERAR_"):
            raise ValueError("JWT_SECRET_KEY deve ser uma chave aleatoria com pelo menos 32 caracteres.")
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
