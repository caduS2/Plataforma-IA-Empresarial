# Status do projeto

## Estado validado

- Frontend oficial em `frontend-web`, desenvolvido com Next.js, React e TypeScript.
- Backend FastAPI conectado ao PostgreSQL com SQLAlchemy e migrations Alembic.
- Autenticação JWT mediada por BFF, com cookie `HttpOnly`, `Secure` em HTTPS e `SameSite=Lax`.
- Isolamento multiempresa aplicado a usuários, documentos, convites, dashboard e respostas com fontes.
- Recuperação de senha e convites com tokens persistidos somente como hash.
- Ruff, Pytest, ESLint, TypeScript, Vitest, Playwright e builds Docker validados.
- CI versionada em `.github/workflows/ci.yml`.
- Backend público com `/health` e `/ready` funcionais no Render.
- Frontend configurado para respeitar `0.0.0.0:$PORT` no Render.

## Operação externa necessária

- Confirmar o deploy do commit mais recente no serviço `nucleo-ai-frontend`.
- Provisionar o primeiro administrador pelo shell privado do backend, caso ainda não exista.
- Configurar SMTP para entrega real de convites e recuperação de senha.
- Configurar armazenamento persistente para uploads antes de uso contínuo em produção.

## Limitações transparentes

- OCR local completo, rate limiting distribuído, observabilidade externa e backup automatizado não fazem parte desta versão.
- Gemini e SEC ficam indisponíveis enquanto suas variáveis opcionais não estiverem configuradas.
