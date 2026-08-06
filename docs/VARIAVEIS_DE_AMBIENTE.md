# Variáveis de ambiente

Use `backend/.env.example` como referência. Mantenha valores privados apenas em `backend/.env` no desenvolvimento e no gerenciador de segredos da hospedagem.

Principais grupos: banco (`DATABASE_URL`), sessão (`JWT_SECRET_KEY`), origem pública (`FRONTEND_URL`, `CORS_ORIGINS`), e-mail (`EMAIL_*`, `SMTP_*`), IA (`GEMINI_*`) e integrações financeiras (`SEC_USER_AGENT`).

O front-end usa `NEXT_PUBLIC_API_URL`. Essa variável é pública e nunca pode conter segredo.
