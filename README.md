# Núcleo AI — Plataforma Empresarial Full Stack

SaaS multiempresa para transformar conhecimento interno em respostas com fontes, automações comerciais e inteligência operacional. O projeto demonstra uma arquitetura completa com frontend moderno, backend REST, autenticação segura, PostgreSQL, testes, containers e integração contínua.

## Aplicação publicada

- Frontend: [nucleo-ai-frontend.onrender.com](https://nucleo-ai-frontend.onrender.com)
- API: [nucleo-ai-api.onrender.com](https://nucleo-ai-api.onrender.com)
- Documentação OpenAPI: [nucleo-ai-api.onrender.com/docs](https://nucleo-ai-api.onrender.com/docs)
- Prontidão do banco: [nucleo-ai-api.onrender.com/ready](https://nucleo-ai-api.onrender.com/ready)

O frontend e o backend são Web Services independentes no Render. Contas não são abertas por cadastro público: o primeiro administrador é provisionado no ambiente controlado e os demais usuários entram por convite.

## O que está pronto

- Login com JWT armazenado em cookie `HttpOnly` por uma camada BFF no Next.js
- Recuperação e redefinição de senha com token temporário armazenado apenas como hash
- Isolamento de usuários, documentos, convites e métricas por empresa
- Controle de acesso com perfis `admin`, `gestor` e `usuario`
- Upload validado de PDF, DOCX, XLSX, texto, CSV e imagens até 50 MB
- Extração de texto e respostas da IA acompanhadas das fontes internas
- Geração de e-mail, follow-up e proposta com contexto empresarial
- Convites seguros para novos membros
- Indicadores oficiais do Banco Central e conectores para CVM e SEC
- Dashboard responsivo com dados reais, estados de erro, carregamento e vazio
- Migrações Alembic, testes Pytest/Vitest/Playwright, Ruff, ESLint e CI
- Execução completa com Docker Compose

## Arquitetura

```text
Navegador
   │ cookie HttpOnly
   ▼
Next.js 16 (frontend-web / BFF)
   │ Authorization: Bearer
   ▼
FastAPI (backend)
   │ SQLAlchemy + Alembic
   ▼
PostgreSQL 17
```

O diretório `frontend-nucleo` é a interface original preservada como referência. O produto principal e oficial é `frontend-web`.

## Stack

| Camada | Tecnologias |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS, Zod, Lucide |
| Backend | Python 3.12, FastAPI, Pydantic, SQLAlchemy, Alembic |
| Dados | PostgreSQL 17, armazenamento persistente de uploads |
| Segurança | JWT, Argon2, cookie HttpOnly, RBAC, rate limiting, isolamento por tenant |
| Qualidade | Pytest, Ruff, Vitest, Testing Library, Playwright, ESLint |
| Operação | Docker, Docker Compose, GitHub Actions |

## Início rápido com Docker

Pré-requisitos: Git e Docker Desktop.

1. Crie a configuração local do Docker e substitua o placeholder por uma senha aleatória longa para o PostgreSQL:

```powershell
Copy-Item .env.example .env
```

2. Crie a configuração local do backend:

```powershell
Copy-Item backend/.env.example backend/.env
```

3. Gere uma chave JWT e coloque o resultado em `JWT_SECRET_KEY` dentro de `backend/.env`:

```powershell
py -3.12 -c "import secrets; print(secrets.token_urlsafe(64))"
```

4. Suba a aplicação:

```powershell
docker compose up --build -d
```

5. Crie o primeiro administrador:

```powershell
docker compose exec backend python -m app.scripts.create_admin --empresa "Empresa Demo" --nome "Administrador" --email "admin@empresa.com"
```

A senha é solicitada e confirmada sem aparecer no terminal.

6. Acesse:

- Aplicação: http://localhost:3000
- Documentação da API: http://localhost:8000/docs
- Saúde da API: http://localhost:8000/health

Para acompanhar os serviços, use `docker compose logs -f`. Para encerrar sem apagar os dados, use `docker compose down`.

## Desenvolvimento local

### Backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
# configure JWT_SECRET_KEY e mantenha o PostgreSQL disponível
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Frontend

Em outro terminal:

```powershell
cd frontend-web
corepack enable
pnpm install
pnpm dev
```

O frontend acessa `http://127.0.0.1:8000` por padrão. Para outro endereço, copie `.env.example` para `.env.local` e altere `BACKEND_URL`.

## Verificações de qualidade

```powershell
# backend
cd backend
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m pytest --cov=app

# frontend
cd ..\frontend-web
pnpm lint
pnpm typecheck
pnpm test
pnpm test:e2e
pnpm build
```

O workflow em `.github/workflows/ci.yml` repete lint, tipos, testes, migrations e build em cada push e pull request.

## Configuração e segredos

Nunca versione `backend/.env` ou `frontend-web/.env.local`. As chaves documentadas ficam em:

- `backend/.env.example`
- `frontend-web/.env.example`
- `docs/VARIAVEIS_DE_AMBIENTE.md`

Em produção, use PostgreSQL gerenciado, HTTPS, SMTP real, uma chave JWT exclusiva, armazenamento de objetos para uploads e segredos fornecidos pela plataforma de deploy.

## Deploy no Render

O deploy utiliza os Dockerfiles versionados. O frontend oficial deve ser configurado como Web Service com:

- Root Directory: `frontend-web`
- Dockerfile Path: `./Dockerfile`
- `BACKEND_URL=https://nucleo-ai-api.onrender.com`
- Health Check Path: `/login`

O processo Next.js escuta `0.0.0.0` e respeita a variável dinâmica `PORT` fornecida pelo Render. O backend executa `alembic upgrade head` antes de iniciar o FastAPI e expõe `/health` e `/ready`.

## Decisões de segurança importantes

- Não existe cadastro público: novos usuários entram por convite.
- A primeira conta administrativa é criada por comando no ambiente controlado.
- O token de sessão não fica acessível ao JavaScript do navegador.
- Consultas e métricas usam sempre o `empresa_id` do usuário autenticado.
- Tokens de convite e redefinição são persistidos como SHA-256, nunca em texto puro.
- O backend aplica cabeçalhos de segurança e limites nos endpoints sensíveis.

## Estrutura principal

```text
backend/          API, domínio, migrations e testes Python
frontend-web/     aplicação Next.js oficial, BFF e testes web
frontend-nucleo/  interface original preservada como referência
docs/             operação, ambiente, backup e histórico
.github/          integração contínua
docker-compose.yml
```

## Limitações conhecidas

- PDFs escaneados e imagens dependem da capacidade visual do provedor de IA; não há OCR local completo.
- E-mails reais exigem SMTP configurado no ambiente de produção.
- Uploads em produção devem usar armazenamento persistente ou de objetos; o filesystem efêmero não é suficiente.
- Rate limiting é local ao processo e deve ser distribuído antes de escalar horizontalmente.
- Observabilidade externa e backups automáticos dependem do provedor de infraestrutura.

## Uso profissional

Textos objetivos para currículo, LinkedIn, Workana e entrevistas estão em [`docs/PORTFOLIO.md`](docs/PORTFOLIO.md).

## Licença

Projeto autoral para portfólio. Antes de reutilizar comercialmente, adicione uma licença explícita ao repositório.
