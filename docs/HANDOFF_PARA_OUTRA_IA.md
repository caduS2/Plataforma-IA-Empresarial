# Handoff para outra IA

## Produto e arquitetura

Núcleo AI é uma plataforma para equipes comerciais consultarem documentos internos e gerarem respostas com fontes. O front-end está em `frontend-nucleo` e usa Vinext/React. O back-end está em `backend`, usa FastAPI, SQLAlchemy, Alembic e PostgreSQL.

O front-end chama a API por uma variável pública de URL. O back-end resolve o usuário pela sessão JWT e sempre deriva a empresa a partir desse usuário; não aceite empresa enviada pelo navegador para consultar documentos, membros, convites ou Copilot.

## Funcionalidades implementadas

- Cadastro, login, JWT e papéis `admin`, `gestor` e `usuario`.
- Recuperação de senha com token de uso único armazenado como hash.
- Convites com hash, expiração, cancelamento, reenvio e invalidação de pendentes anteriores.
- Documentos isolados por empresa, upload com validação de formato e extração de texto.
- Copilot com fontes internas e integração configurável com Gemini.
- Banco Central, CVM e SEC em modo dependente de configuração.
- Endpoints de saúde e prontidão do banco.
- CORS configurável, cabeçalhos de proteção e limite local básico de requisições.

## Pontos pendentes

- OCR local completo para imagens e PDFs escaneados; hoje esses arquivos ficam em `aguardando_ocr` e podem ser usados pela visão do provedor de IA quando configurada.
- Interface completa para convite, papéis e reprocessamento de documentos.
- Auditoria persistente, rate limiting distribuído, backup automatizado e observabilidade externa.
- SMTP real, SEC com identificador e dados de mercado licenciados.
- Publicação: requer chave JWT forte, banco gerenciado, domínio e provedor escolhido.

## Segurança

Nunca leia, imprima ou versione `.env`, chaves, senhas, tokens ou documentos enviados. Revise o valor de `JWT_SECRET_KEY` antes de produção; trocar a chave invalida sessões existentes. `backend/.env.example` contém somente nomes e exemplos seguros.

## Como continuar

1. Leia os arquivos relevantes antes de editar e confira o status do Git.
2. Preserve alterações existentes e faça mudanças pequenas.
3. Execute migrações, compilação do back-end, build e testes do front-end após cada conjunto de alterações.
4. Atualize este arquivo e `docs/STATUS_DO_PROJETO.md` ao concluir uma etapa.

## Auditoria mais recente

Em 6 de agosto de 2026, o Alembic estava no cabeçalho `a3c9e4f106d2`; a prontidão do PostgreSQL respondeu corretamente; a compilação Python e o build Vinext passaram; e os dois testes de renderização do front-end passaram. Não há suíte automatizada de testes de back-end versionada no projeto. OCR local completo, envio SMTP real, monitoramento, backup automatizado e publicação não foram validados.

## Prompt para continuar em outra IA

> Leia primeiro `docs/HANDOFF_PARA_OUTRA_IA.md`, inspecione o estado real dos arquivos e o Git, preserve mudanças existentes e não invente o estado do projeto. Execute os testes disponíveis antes e depois de alterar apenas o necessário. Nunca exponha conteúdo de `.env`, chaves, senhas, tokens ou dados privados. Atualize este handoff ao final.
