# RH Analytics - Dashboard para Empresas

Sistema de gestão de RH com dashboard analítico, controle de colaboradores, ponto, folha de pagamento, avaliações, empréstimos e cargos por alas.

## Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** React 18, TypeScript, Vite

---

## Pré-requisitos

- **Python 3.10+**
- **Node.js 18+** e npm
- **Git**

---

## Configuração do Projeto

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd Dashboard-RH
```

### 2. Variáveis de ambiente

Copie os arquivos de exemplo e ajuste conforme necessário:

```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

**Backend (.env):**
- `SECRET_KEY` – Chave para JWT (em produção use uma chave forte de 32+ caracteres)
- `DATABASE_URL` – URL do banco (padrão: SQLite em `./database.db`)
- `CORS_ORIGINS` – Origens permitidas (ex.: `http://localhost:5173`)

**Frontend (.env):**
- `VITE_API_URL` – URL da API (padrão: `http://localhost:8000/api/v1`)

---

## Backend – Setup do zero

### 1. Entre na pasta do backend

```bash
cd backend
```

### 2. Crie o ambiente virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o .env

```bash
# Copie o exemplo (se ainda não fez)
copy .env.example .env   # Windows
cp .env.example .env      # Linux/macOS

# Edite o .env conforme necessário
```

### 5. Crie o banco de dados do zero

**Opção A – Banco zerado (recomendado na primeira vez):**

```bash
# Certifique-se de estar em backend/ com o venv ativado
python -m seeds.reset_data
```

Isso remove o banco existente (se houver), recria as tabelas e insere usuários, departamentos, alas e cargos iniciais.

**Opção B – Apenas subir o servidor:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Na primeira execução, as tabelas são criadas automaticamente e as alas/cargos padrão são inseridos se a tabela de alas estiver vazia.

### 6. Inicie o servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend ficará em **http://localhost:8000**
Documentação da API: **http://localhost:8000/docs**

---

## Frontend – Setup do zero

### 1. Entre na pasta do frontend

```bash
cd frontend
```

### 2. Instale as dependências

```bash
npm install
```

### 3. Configure o .env

```bash
# Copie o exemplo (se ainda não fez)
copy .env.example .env   # Windows
cp .env.example .env      # Linux/macOS

# Garanta que VITE_API_URL aponte para o backend (ex.: http://localhost:8000/api/v1)
```

### 4. Inicie o servidor de desenvolvimento

```bash
npm run dev
```

O frontend ficará em **http://localhost:5173**

---

## Acesso inicial

Após o setup:

- **URL:** http://localhost:5173
- **Login:** `admin@rh.com`
- **Senha:** `admin123`

Outros usuários de teste (após `reset_data`):
- `rh@rh.com` / `rh123`
- `gestor@rh.com` / `gestor123`
- `visualizador@rh.com` / `vis123`

---

## Banco de dados

### SQLite (padrão)

O banco é criado em `backend/database.db` (ou conforme `DATABASE_URL` no `.env`).

### Zerar o banco e recriar

```bash
cd backend
python -m seeds.reset_data
```

**Importante:** Pare o servidor antes de rodar o reset, ou o script tentará limpar as tabelas com DELETE.

### Estrutura principal

- **Usuários** – Autenticação e roles (admin, rh, gestor, visualizador)
- **Departamentos** – Áreas da empresa
- **Alas** – Grupos de cargos (DEV, DS, RH, Marketing, etc.)
- **Cargos** – Vinculados a alas e níveis
- **Colaboradores** – Dados cadastrais e vínculo com departamento/cargo
- **Ponto** – Registros de jornada e horas extras
- **Folha de pagamento** – Cálculo e processamento
- **Avaliações** – Avaliações de desempenho
- **Empréstimos** – Empréstimos consignados

---

## Scripts úteis

### Backend

| Comando | Descrição |
|--------|-----------|
| `uvicorn app.main:app --reload --port 8000` | Inicia o servidor em modo desenvolvimento |
| `python -m seeds.reset_data` | Zera o banco e executa seed mínimo |
| `python -m seeds.seed_data` | Seed completo (colaboradores, ponto, folha) |

### Frontend

| Comando | Descrição |
|--------|-----------|
| `npm run dev` | Servidor de desenvolvimento |
| `npm run build` | Build para produção |
| `npm run preview` | Preview do build |
| `npm run lint` | Verifica código com Biome |
| `npm run lint:fix` | Corrige automaticamente com Biome |
| `npm run format` | Formata código com Biome |

---

## Pre-commit e qualidade de código

### Setup (após clonar)

```bash
# 1. Instalar dependências do root (husky + lint-staged) - configura os hooks
npm install

# 2. Instalar dependências do backend (inclui pre-commit)
cd backend
pip install -r requirements.txt

# 3. Instalar dependências do frontend (inclui Biome)
cd ../frontend
npm install
```

O `npm install` na raiz executa o script `prepare` que configura o Husky. O hook `pre-commit` roda `pre-commit run` (backend) e `lint-staged` (frontend).

**Importante:** O comando `pre-commit` precisa estar no PATH. Após instalar as dependências do backend (`pip install -r requirements.txt`), ative o venv antes de commitar, ou instale globalmente: `pip install pre-commit`.

### O que roda no commit

- **Backend:** Ruff (lint + format), Bandit (segurança), pre-commit-hooks (trailing whitespace, etc.)
- **Frontend:** Biome (lint + format) via Husky + lint-staged

### Comandos manuais

```bash
# Rodar todos os hooks em todos os arquivos
pre-commit run --all-files

# Rodar apenas Ruff no backend
cd backend && ruff check . && ruff format .
```

### Conflito "Stashed changes conflicted with hook auto-fixes"

Quando há alterações **não staged** nos mesmos arquivos que os hooks modificam, o pre-commit pode falhar ao restaurar o stash. Para evitar:

1. **Opção A:** Faça `git add -A` antes de commitar (stage tudo)
2. **Opção B:** Rode `pre-commit run --all-files` primeiro, depois `git add` os arquivos corrigidos e commite novamente

### Corrigir erros do Ruff antes de commitar

Se o Ruff falhar (ex.: tabs em vez de espaços), corrija manualmente:

```bash
cd backend
ruff check . --fix
ruff format .
git add .
```

---

## Estrutura do projeto

```
Dashboard-RH/
├── backend/
│   ├── app/
│   │   ├── api/v1/      # Endpoints da API
│   │   ├── core/        # Config, database, security
│   │   ├── models/      # Modelos SQLAlchemy
│   │   ├── schemas/     # Schemas Pydantic
│   │   └── services/    # Lógica de negócio
│   ├── seeds/           # Scripts de seed
│   ├── .env.example
│   ├── .env             # (não versionado)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   ├── .env.example
│   └── .env             # (não versionado)
└── README.md
```

---

## Troubleshooting

### Erro ao rodar `reset_data` (banco em uso)

Pare o servidor backend e execute novamente. Se o arquivo estiver bloqueado, o script tentará limpar as tabelas com DELETE.

### CORS bloqueando requisições

Confira se `CORS_ORIGINS` no `.env` do backend inclui a URL do frontend (ex.: `http://localhost:5173`).

### Frontend não conecta na API

Verifique se `VITE_API_URL` no `.env` do frontend aponta para o backend (ex.: `http://localhost:8000/api/v1`).

### Módulo não encontrado (Python)

Ative o ambiente virtual e reinstale as dependências:

```bash
cd backend
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```
