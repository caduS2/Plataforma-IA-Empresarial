# Variáveis de ambiente

Use `backend/.env.example` como referência. Mantenha valores privados apenas em `backend/.env` no desenvolvimento e no gerenciador de segredos da hospedagem.

Principais grupos: banco (`DATABASE_URL`), sessão (`JWT_SECRET_KEY`), origem pública (`FRONTEND_URL`, `CORS_ORIGINS`), e-mail (`EMAIL_*`, `SMTP_*`), IA (`GEMINI_*`) e integrações financeiras (`SEC_USER_AGENT`).

O frontend oficial usa `BACKEND_URL` apenas no runtime do servidor Next.js. Ela deve apontar para a URL interna ou pública do FastAPI e nunca deve conter segredo. O navegador chama somente as rotas `/api/*` da camada BFF.
