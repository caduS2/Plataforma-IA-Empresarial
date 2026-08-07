# Núcleo — Plataforma de IA Empresarial

Plataforma SaaS multiempresa desenvolvida como projeto autoral para aplicar, na prática, conceitos de desenvolvimento backend, APIs REST, autenticação, bancos de dados, segurança, integrações e inteligência artificial.

> Projeto pessoal em evolução para beta técnico.

---

## Sobre o projeto

O **Núcleo** foi desenvolvido com o objetivo de simular uma plataforma empresarial real, permitindo que diferentes empresas utilizem o mesmo sistema mantendo seus usuários, documentos e informações isolados.

O projeto é utilizado como ambiente prático de desenvolvimento e evolução de conhecimentos em engenharia de software.

---

## Principais funcionalidades

- Autenticação de usuários
- Autenticação baseada em JWT
- Hash seguro de senhas com Argon2
- Gerenciamento de empresas
- Gerenciamento de usuários e equipes
- Papéis de administrador, gestor e usuário
- Sistema de convites
- Recuperação de senha
- Isolamento de dados entre empresas
- Upload e processamento de documentos
- Uso de documentos como fontes para respostas de IA
- Integrações com serviços externos
- Integrações com Banco Central e CVM
- Endpoints de saúde e prontidão da aplicação
- Migrations de banco de dados
- Documentação de backup e restauração

---

## Tecnologias

### Backend

- Python
- FastAPI
- PostgreSQL
- SQL
- SQLAlchemy
- Alembic
- APIs REST

### Segurança

- JWT
- Argon2
- Controle de acesso por papéis
- Variáveis de ambiente
- CORS

### Inteligência Artificial e integrações

- Gemini
- Processamento de documentos
- Banco Central
- CVM

### Frontend

- React
- JavaScript
- HTML5
- CSS3

### Ferramentas

- Git
- GitHub
- Docker
- Swagger / OpenAPI

---

## Arquitetura geral

O projeto é dividido principalmente entre:

```text
Plataforma-IA-Empresarial/
│
├── backend/
│   ├── app/
│   ├── migrations/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend-nucleo/
│
├── docs/
│
├── README.md
└── .gitignore
