# Backup e restauração

## Backup do PostgreSQL

Use `pg_dump` apontando para a variável `DATABASE_URL` de produção e salve o resultado fora do servidor da aplicação. Inclua data no nome e teste a restauração em um banco separado.

## Arquivos enviados

Faça backup do armazenamento persistente configurado em `UPLOAD_DIR`. O banco guarda referências aos arquivos; os dois backups precisam permanecer alinhados.

## Restauração

1. Crie um banco vazio separado.
2. Restaure o dump nesse banco, nunca diretamente no banco de produção.
3. Restaure os arquivos no mesmo caminho de armazenamento ou atualize as referências de forma controlada.
4. Aponte um ambiente de teste para a cópia restaurada e execute `/ready`.

## Retenção

Defina retenção, criptografia e acesso restrito no provedor escolhido. Não versionar dumps, uploads ou `.env` no Git.
