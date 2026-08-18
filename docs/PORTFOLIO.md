# Núcleo AI — material para portfólio

## Resumo para currículo

**Núcleo AI — Plataforma SaaS Full Stack (projeto pessoal)**  
Desenvolvimento de uma plataforma multiempresa com Next.js, TypeScript, FastAPI e PostgreSQL. Implementei autenticação JWT com cookies HttpOnly, RBAC, isolamento de dados por tenant, uploads validados, respostas de IA com fontes, migrations Alembic, testes automatizados, Docker, CI com GitHub Actions e deploy no Render.

## Descrição para LinkedIn

Desenvolvi o Núcleo AI, um projeto pessoal full stack voltado à organização e consulta de conhecimento empresarial. A aplicação combina um frontend Next.js com uma API FastAPI e PostgreSQL, usando uma camada BFF para manter o JWT fora do JavaScript do navegador. O projeto inclui isolamento multiempresa, perfis de acesso, documentos, convites, recuperação de senha, automações com fontes internas, integrações de dados públicos, migrations, testes unitários e E2E, Docker e integração contínua.

Um dos principais desafios foi tornar o mesmo produto consistente entre desenvolvimento local e produção: corrigi o startup do Next.js para respeitar a porta dinâmica do Render, validei cookies atrás de proxy HTTPS, alinhei schema SQLAlchemy/Alembic e automatizei verificações de backend, frontend e navegador.

## Apresentação para Workana

Projeto demonstrativo de uma plataforma web completa construída com React/Next.js no frontend e Python/FastAPI no backend. A solução possui autenticação segura, banco PostgreSQL, separação de dados por empresa, upload e processamento de documentos, painel responsivo, APIs REST, containers Docker e testes automatizados. O projeto evidencia capacidade para desenvolver, integrar, testar e publicar aplicações full stack, sem representar trabalho realizado para cliente comercial.

## Pitch para entrevista

“O Núcleo AI é meu projeto pessoal de portfólio para demonstrar uma entrega full stack de ponta a ponta. Eu construí o frontend em Next.js, o backend em FastAPI e a persistência em PostgreSQL. A autenticação usa JWT em cookie HttpOnly por uma camada BFF, e todas as consultas de negócio derivam a empresa do usuário autenticado para evitar vazamento entre tenants. Também implementei migrations, testes unitários e E2E, CI e Docker. Na publicação, diagnostiquei um timeout real do frontend e corrigi o processo para escutar a porta dinâmica do Render.”

## Pontos técnicos para destacar

- BFF no Next.js para proteger o token de sessão.
- Autorização por perfil e isolamento multiempresa no backend.
- Tokens de convite e redefinição persistidos como hash.
- Uploads com limite, nomes aleatórios e validação de assinatura/formato.
- Respostas de IA ligadas às fontes internas utilizadas.
- Alembic como fonte de evolução do schema PostgreSQL.
- Pytest, Vitest e Playwright cobrindo camadas diferentes.
- GitHub Actions, Docker multi-stage e healthchecks.
- Diagnóstico de produção baseado em tempo até o primeiro byte, porta e binding do processo.

## Stack

Next.js, React, TypeScript, Tailwind CSS, Zod, FastAPI, Python, Pydantic, SQLAlchemy, Alembic, PostgreSQL, JWT, Argon2, Docker, Docker Compose, Pytest, Vitest, Playwright, Ruff, ESLint, GitHub Actions e Render.
