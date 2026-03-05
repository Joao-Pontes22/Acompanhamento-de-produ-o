# 📊 Sistema de Acompanhamento de Produção

API backend desenvolvida para **controle e acompanhamento de processos produtivos**, permitindo registrar, consultar e gerenciar informações relacionadas à produção, componentes, estoque, movimentações e fornecedores.

O objetivo do projeto é criar uma **API organizada, escalável e de fácil manutenção**, aplicando boas práticas de arquitetura backend.

⚠️ **Status do projeto:**  
A estrutura principal da aplicação foi finalizada. O projeto encontra-se **em desenvolvimento**, com ajustes finais de regras de negócio, melhorias e testes sendo implementados.

---

# 🚀 Tecnologias Utilizadas
```
- Python
- FastAPI
- SQLAlchemy
- SQLite (ambiente de desenvolvimento)
- Alembic (migração de banco de dados)
- Pydantic
- JWT Authentication
```
Essas tecnologias permitem construir uma **API performática, tipada e com documentação automática**.

---

# 🧠 Arquitetura do Projeto

A aplicação foi estruturada seguindo conceitos inspirados em **Clean Architecture e Domain-Oriented Design**, separando responsabilidades e organizando o sistema por **domínios de negócio**.

Essa abordagem melhora:

- organização do código
- escalabilidade do sistema
- manutenção
- clareza das regras de negócio
- isolamento entre camadas

A estrutura principal do projeto está organizada da seguinte forma:
```
app
 ├── core
 │   ├── Settings
 │   ├── Dependencies
 │   ├── Repositories_dependencies
 │   └── Services_dependencies
 │
 ├── domain
 │   ├── Assembly_Production
 │   ├── Clients
 │   ├── Components
 │   ├── Employers
 │   ├── Entities
 │   ├── Login
 │   ├── Machine
 │   ├── Machining_Production
 │   ├── Movimentation
 │   ├── Parts
 │   ├── Parts_And_Components
 │   ├── Relation
 │   ├── Sectors
 │   ├── Setup
 │   ├── Stock
 │   ├── Suppliers
 │   └── Value_objects
 │
 ├── models
 ├── repositories
 ├── Routes
 ├── Schemas
 └── Services
```
Cada **domínio** representa uma parte específica do sistema produtivo, mantendo suas próprias regras e responsabilidades.

---

# 🔐 Autenticação

A API possui **autenticação baseada em JWT (JSON Web Token)**.

Fluxo básico:

1. usuário realiza login
2. recebe um token JWT
3. o token é utilizado nas requisições protegidas da API

Isso permite **controle de acesso e segurança nas operações do sistema**.

---

# 📦 Principais Módulos do Sistema

O sistema possui diversos módulos voltados ao controle produtivo.
```
Produção
- Assembly Production
- Machining Production
- Setup

Estrutura de Produto
- Parts
- Components
- Parts and Components
- Relations

Operacional
- Machines
- Sectors
- Employers

Logística
- Stock
- Movimentation
- Suppliers

Gestão
- Clients
```
---

# 📡 Funcionalidades da API

Entre as funcionalidades já implementadas estão:
```
- registro de produção
- controle de peças e componentes
- movimentação de estoque
- controle de máquinas
- gestão de fornecedores
- gestão de setores
- autenticação de usuários
- filtros e consultas de dados
- integração entre diferentes entidades do sistema produtivo
```
---

# ⚙️ Como Rodar o Projeto

1️⃣ Clonar o repositório
```
git clone https://github.com/seu-usuario/seu-repositorio.git
```
---

2️⃣ Criar ambiente virtual
```
python -m venv venv
```
---

3️⃣ Ativar ambiente virtual
```
Windows

venv\Scripts\activate

Linux ou Mac

source venv/bin/activate
```
---

4️⃣ Instalar dependências
```
pip install -r requirements.txt
```
---

5️⃣ Rodar a aplicação
```
uvicorn main:app --reload
```
---

6️⃣ Acessar documentação automática da API

FastAPI gera documentação automaticamente.

Swagger
```
http://localhost:8000/docs
```
ReDoc
```
http://localhost:8000/redoc
```
---

# 🔄 Migração de Banco de Dados

O projeto utiliza **Alembic** para versionamento do banco.

Criar nova migração
```
alembic revision --autogenerate -m "descricao"
```
Aplicar migrações
```
alembic upgrade head
```
---

# 📈 Roadmap do Projeto

Próximas melhorias planejadas:

- finalização de regras de negócio
- melhoria de tratamento de exceções
- criação de testes automatizados
- otimização de consultas ao banco
- melhoria da documentação da API
- possível migração para PostgreSQL

---

# 🎯 Objetivo do Projeto

Este projeto foi desenvolvido com foco em:

- prática de **arquitetura backend**
- organização de sistemas complexos
- aplicação de **boas práticas de engenharia de software**
- construção de APIs escaláveis
- simulação de um sistema real de controle produtivo

---

# 👨‍💻 Autor

João Oliveira

Projeto desenvolvido como estudo e evolução prática em **arquitetura backend, organização de código e desenvolvimento de APIs com FastAPI**.
