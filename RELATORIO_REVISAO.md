# Relatório de Revisão — Sistema RH PWA

## Problemas Encontrados e Corrigidos

| Arquivo | Problema | Correção Aplicada |
|---------|----------|-------------------|
| `backend/app/main.py` | Imports duplicados, falta lifespan, routers não registrados corretamente | Adicionado lifespan para criar tabelas, imports de models, CORS via settings |
| `backend/app/core/database.py` | Falta função `get_db` para injeção de dependência | Criada função `get_db()` com yield |
| `backend/app/core/config.py` | Config obrigatório sem fallback, Pydantic v1 Config | Valores default para dev, migrado para `model_config` (Pydantic v2) |
| `backend/app/core/security.py` | `Depends()` sem callable, passlib incompatível com bcrypt 5.x | Uso de `Depends(get_db)`, troca para bcrypt direto |
| `backend/app/core/security.py` | `require_role` comparava enum com string | Uso de `user.role.value not in roles` |
| `backend/app/api/__init__.py` | Arquivo não existia | Criado agregando todos os routers v1 |
| `backend/app/api/v1/auth.py` | Login não usava OAuth2PasswordRequestForm | Form data para compatibilidade OAuth2 |
| `backend/app/api/v1/auth.py` | `db: Session = Depends()` sem get_db | `Depends(get_db)` |
| `backend/app/api/v1/employees.py` | Código malformado (rotas dentro de return) | Reestruturado, rotas extraídas |
| `backend/app/api/v1/employees.py` | `create_employee` com sintaxe quebrada | Corrigido return e rotas aninhadas |
| `backend/app/api/v1/employees.py` | Falta get_db em todos os endpoints | Adicionado `Depends(get_db)` |
| `backend/app/api/v1/employees.py` | Document type string vs enum | Conversão com try/except para DocumentType |
| `backend/app/api/v1/employees.py` | get_photo retornava bytes sem Response | Uso de `Response(content=..., media_type="image/jpeg")` |
| `backend/app/api/v1/dashboard.py` | `user: get_current_user` typo | `user: User = Depends(require_role(...))` |
| `backend/app/api/v1/dashboard.py` | Payroll.status == "processado" (string) | `PayrollStatus.processado` |
| `backend/app/api/v1/dashboard.py` | Falta get_db | Adicionado em todos os endpoints |
| `backend/app/api/v1/timesheets.py` | file_parser recebia path, não file-like | Ajustado parse_csv/json/pdf para aceitar file-like |
| `backend/app/api/v1/timesheets.py` | Timesheet(**rec) com keys incompatíveis | Lógica de import com mapeamento explícito |
| `backend/app/api/v1/payroll.py` | status enum vs string em PayrollResponse | Uso de `payroll.status.value` |
| `backend/app/api/v1/loans.py` | Loan.status filter com string | `LoanStatus(status)` |
| `backend/app/api/v1/loans.py` | LoanInstallment sem employee_id | Uso de `loan.employee_id` |
| `backend/app/builders/employee_builder.py` | status/department_id/position_id como string | Conversão para enum e int |
| `backend/app/schemas/employee.py` | department_id/position_id obrigatórios | `Optional[int]` |
| `backend/app/schemas/employee.py` | Falta model_config Pydantic v2 | `model_config = {"from_attributes": True}` |
| `backend/app/services/file_parser.py` | parse_csv usava pandas (build falha) | Substituído por csv.DictReader |
| `backend/app/services/file_parser.py` | parse_json/parse_pdf esperavam path | Suporte a file-like objects |
| `backend/seeds/seed_data.py` | Apenas placeholder | Implementado seed completo com 15 colaboradores |
| `backend/requirements.txt` | pandas causava erro de build | Removido, csv nativo |
| `backend/requirements.txt` | passlib incompatível | Removido, bcrypt direto |
| `frontend/src/services/api.ts` | baseURL incorreto, sem interceptor 401 | baseURL `/api/v1`, interceptor para logout em 401 |
| `frontend/src/services/auth.ts` | Login com JSON em vez de form | URLSearchParams + Content-Type form-urlencoded |
| `frontend/src/services/dashboard.ts` | Paths com /api duplicado | `/dashboard/overview` etc. |
| `frontend/src/services/employee.ts` | Paths incorretos | `/employees` |
| `frontend/src/services/timesheet.ts` | Paths incorretos | `/timesheets`, `/timesheets/import` |
| `frontend/src/services/payroll.ts` | Path e método process incorretos | `/payroll`, `calculate-batch/{month}` |
| `frontend/src/pages/EmployeesPage.tsx` | emp.name, emp.position_name | full_name, position_title |
| `frontend/src/components/EmployeeForm.tsx` | Formulário incompleto | Formulário completo com todos os campos |
| `frontend/src/components/Header.tsx` | Logout com localStorage direto | Uso de removeToken() |
| `frontend/vite.config.ts` | Porta 3000 | Porta 5173 |
| `frontend/App.tsx` | Header na tela de login | Header oculto em /login |
| `frontend/index.html` | Em public/, sem script | Movido para root com script main.tsx |

## Arquivos Criados (que estavam faltando)

- `backend/app/api/__init__.py` — Agregação dos routers
- `backend/app/api/v1/departments.py` — Endpoint listar departamentos
- `backend/app/api/v1/positions.py` — Endpoint listar cargos
- `frontend/src/services/departments.ts` — Serviço de departamentos
- `frontend/src/services/positions.ts` — Serviço de cargos
- `frontend/index.html` — Entry point do Vite
- `backend/.env` — Configuração de ambiente
- `frontend/.env` — VITE_API_URL

## Status Final

- **Backend**: ✅ Rodando em http://localhost:8000
- **Frontend**: ✅ Rodando em http://localhost:5173
- **Seed**: ✅ 4 usuários, 5 departamentos, 5 cargos, 15 colaboradores, 200 registros de ponto, 5 folhas

## Credenciais de Teste

| Usuário           | Senha     | Role       |
|-------------------|-----------|------------|
| admin@rh.com      | admin123  | Admin      |
| rh@rh.com         | rh123     | RH         |
| gestor@rh.com     | gestor123 | Gestor     |
| visualizador@rh.com | vis123  | Visualizador |

## Como Executar

```bash
# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
python seeds/seed_data.py
uvicorn app.main:app --reload --port 8000

# Frontend (outro terminal)
cd frontend
npm install
npm run dev
```

Acesse http://localhost:5173 e faça login com admin@rh.com / admin123.
