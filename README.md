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
```

O backend concentra as APIs, regras de negócio, autenticação, acesso ao banco de dados e integrações.

O frontend fornece a interface utilizada pelos usuários.

A pasta `docs` contém a documentação técnica complementar do projeto.

---

## Segurança e dados sensíveis

Credenciais, senhas, chaves de API e configurações privadas não são armazenadas no repositório público.

Os principais arquivos locais são:

```text
backend/.env
frontend-nucleo/.env.local
```

Esses arquivos são ignorados pelo Git e devem permanecer apenas no ambiente local.

O arquivo `backend/.env.example` serve como referência para configurar as variáveis necessárias sem expor informações privadas.

---

## Executando localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/caduS2/Plataforma-IA-Empresarial.git
```

Entre na pasta:

```bash
cd Plataforma-IA-Empresarial
```

---

### 2. Configurar o backend

Entre na pasta do backend:

```bash
cd backend
```

Crie um ambiente virtual Python:

```bash
python -m venv .venv
```

No Windows PowerShell, ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Crie o arquivo local de configuração usando o exemplo existente:

```powershell
Copy-Item .env.example .env
```

Depois configure no arquivo `.env` os dados necessários, principalmente a conexão com PostgreSQL e a chave JWT.

Com o PostgreSQL configurado, aplique as migrations:

```bash
alembic upgrade head
```

Inicie a API:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

---

### 3. Verificar o backend

Com a API executando, acesse:

```text
http://127.0.0.1:8000/health
```

O projeto também possui um endpoint de prontidão que verifica a comunicação com o banco:

```text
http://127.0.0.1:8000/ready
```

---

### 4. Configurar o frontend

Mantenha o terminal do backend aberto.

Abra um **segundo terminal** e entre na pasta:

```bash
cd frontend-nucleo
```

Instale as dependências:

```bash
npm install
```

Crie o arquivo:

```text
.env.local
```

Adicione:

```text
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Depois inicie o frontend:

```bash
npm run dev
```

O endereço para abrir a interface será informado no terminal.

Backend e frontend devem permanecer executando simultaneamente durante o desenvolvimento local.

---

## Documentação da API

Com o backend funcionando, a documentação interativa gerada pelo FastAPI pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

Através do Swagger/OpenAPI é possível visualizar e testar os endpoints da aplicação.

---

## Documentação técnica

A pasta:

```text
docs/
```

contém documentação complementar relacionada a:

- estado atual do projeto;
- variáveis de ambiente;
- backup e restauração;
- continuidade do desenvolvimento;
- handoff técnico.

Essa documentação facilita a manutenção, compreensão e evolução do sistema.

---

## O que este projeto demonstra

O desenvolvimento do Núcleo coloca em prática conhecimentos relacionados a:

- Python e FastAPI;
- desenvolvimento de APIs REST;
- PostgreSQL;
- SQLAlchemy;
- migrations com Alembic;
- autenticação e autorização;
- JWT e Argon2;
- gerenciamento de usuários e empresas;
- controle de papéis e permissões;
- arquitetura multiempresa;
- isolamento de dados entre empresas;
- upload e processamento de documentos;
- integração entre backend e frontend;
- integrações com serviços externos;
- inteligência artificial aplicada a software;
- segurança de aplicações;
- Docker;
- Git e GitHub;
- documentação técnica.

---

## Status do projeto

🚧 **Em desenvolvimento**

O Núcleo é um projeto pessoal em evolução para beta técnico.

A aplicação possui funcionalidades já desenvolvidas e validadas localmente, enquanto outras partes continuam sendo aprimoradas antes de uma futura utilização em produção.

O desenvolvimento atual prioriza evolução da arquitetura, segurança, testes, integrações e qualidade técnica.

---

## Autor

**Carlos Eduardo Martini de Britto**

Desenvolvedor Backend Python Júnior  
Estudante de Análise e Desenvolvimento de Sistemas — UNIP

### Principais tecnologias

`Python` • `FastAPI` • `PostgreSQL` • `SQL` • `APIs REST` • `Docker` • `Git`

---

## Objetivo profissional

Este projeto faz parte do meu portfólio e demonstra conhecimentos adquiridos através do desenvolvimento prático de uma aplicação completa.

Atualmente busco oportunidades como:

- Desenvolvedor Backend Python Júnior
- Desenvolvedor de Software Júnior
- Desenvolvedor Full Stack Júnior
- Trainee em Desenvolvimento de Software
