# RH Analytics - Dashboard for Companies

Sistema de gestão de RH com dashboard analítico para empresas.

## Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite
- **Frontend:** React 18, TypeScript, Vite

## Setup

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m seeds.reset_data  # Seed inicial
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acesse: http://localhost:5173

**Login:** admin@rh.com / admin123
