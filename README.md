# Núcleo AI

Plataforma de conhecimento comercial com FastAPI, PostgreSQL e front-end Vinext/React.

## Executar localmente

Em um terminal, entre em `backend`, ative o ambiente virtual e inicie a API com Uvicorn. Em outro, entre em `frontend-nucleo` e execute o servidor de desenvolvimento. Mantenha os dois terminais abertos.

As configurações locais ficam em `backend/.env` e `frontend-nucleo/.env.local`. Nunca envie esses arquivos para o Git.

## Verificações

- Back-end: compilação Python e `alembic current`.
- Front-end: `npm run build` e `npm test`.

Consulte `docs/STATUS_DO_PROJETO.md` e `docs/HANDOFF_PARA_OUTRA_IA.md` para o estado técnico detalhado.
