# Handoff técnico

## Produto e arquitetura

Núcleo AI é uma plataforma SaaS multiempresa para consulta de documentos internos, respostas de IA com fontes e automações comerciais. O frontend oficial é `frontend-web` (Next.js). O backend está em `backend` (FastAPI, SQLAlchemy e Alembic). `frontend-nucleo` é apenas uma referência histórica preservada.

O navegador acessa APIs internas do Next.js. A camada BFF guarda o JWT em cookie `HttpOnly` e encaminha o token ao FastAPI como Bearer. O backend sempre deriva `empresa_id` do usuário autenticado; nunca aceite um tenant fornecido pelo navegador para consultas de negócio.

## Estado atual

- Deploy alvo: Render.
- Frontend público: `https://nucleo-ai-frontend.onrender.com`.
- Backend público: `https://nucleo-ai-api.onrender.com`.
- O Dockerfile do frontend respeita a porta dinâmica do provedor.
- O backend aplica migrations antes de iniciar e expõe `/health` e `/ready`.
- Testes locais cobrem backend, utilitários frontend e rotas públicas/protegidas no navegador.
- A primeira conta administrativa é criada por `python -m app.scripts.create_admin`; omita `--senha` para usar entrada protegida.

## Segurança

Nunca leia, imprima ou versione `.env`, chaves, senhas, tokens ou documentos enviados. Não registre tokens de convite ou redefinição. Mantenha `CORS_ORIGINS` explícito e use variáveis secretas do provedor.

## Próximos passos operacionais

1. Verifique o estado do Git e preserve mudanças existentes.
2. Execute lint, testes, migrations e builds antes de publicar.
3. Confirme o deploy do frontend e teste login, cookie, dashboard e logout.
4. Configure SMTP e armazenamento persistente antes de uso real por equipes.
