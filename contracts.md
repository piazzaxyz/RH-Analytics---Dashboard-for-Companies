# Contratos de dados para RH Sistema

## Schemas Pydantic (Backend) + Types TypeScript (Frontend)

---

### Users

#### Pydantic

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Literal["admin", "gestor", "rh", "visualizador"]
    is_active: bool
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface User {
  id: number
  username: string
  email: string
  role: 'admin' | 'gestor' | 'rh' | 'visualizador'
  is_active: boolean
  created_at: string // ISO datetime
  updated_at: string // ISO datetime
}

---

### Departments

#### Pydantic

class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str
    manager_id: int
    manager_name: str
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Department {
  id: number
  name: string
  description: string
  manager_id: number
  manager_name: string
  created_at: string
  updated_at: string
}

---

### Positions

#### Pydantic

class PositionResponse(BaseModel):
    id: int
    title: str
    description: str
    base_salary: float
    department_id: int
    department_name: str
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Position {
  id: number
  title: string
  description: string
  base_salary: number
  department_id: number
  department_name: string
  created_at: string
  updated_at: string
}

---

### Employees

#### Pydantic

class EmployeeResponse(BaseModel):
    id: int
    full_name: str
    cpf: str
    rg: str
    birth_date: date
    address: str
    phone: str
    email: str
    work_card_number: str
    work_card_series: str
    admission_date: date
    dismissal_date: Optional[date]
    status: Literal["ativo", "inativo"]
    department_id: int
    department_name: str
    position_id: int
    position_title: str
    supervisor_id: Optional[int]
    supervisor_name: Optional[str]
    bank_name: str
    bank_agency: str
    bank_account: str
    bank_account_type: str
    photo_url: Optional[str]
    salary: float
    pis_pasep: str
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Employee {
  id: number
  full_name: string
  cpf: string
  rg: string
  birth_date: string
  address: string
  phone: string
  email: string
  work_card_number: string
  work_card_series: string
  admission_date: string
  dismissal_date: string | null
  status: 'ativo' | 'inativo'
  department_id: number
  department_name: string
  position_id: number
  position_title: string
  supervisor_id: number | null
  supervisor_name: string | null
  bank_name: string
  bank_agency: string
  bank_account: string
  bank_account_type: string
  photo_url: string | null
  salary: number
  pis_pasep: string
  created_at: string
  updated_at: string
}

---

### Positions History

#### Pydantic

class PositionHistoryResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    position_id: int
    position_title: str
    department_id: int
    department_name: str
    start_date: date
    end_date: Optional[date]
    reason: str
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface PositionHistory {
  id: number
  employee_id: number
  employee_name: string
  position_id: number
  position_title: string
  department_id: number
  department_name: string
  start_date: string
  end_date: string | null
  reason: string
  created_at: string
  updated_at: string
}

---

### Timesheets

#### Pydantic

class TimesheetResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    date: date
    clock_in: Optional[time]
    clock_out: Optional[time]
    clock_in_2: Optional[time]
    clock_out_2: Optional[time]
    total_minutes: int
    overtime_50_minutes: int
    overtime_100_minutes: int
    night_shift_minutes: int
    justification: Optional[str]
    status: Literal["ok", "inconsistente", "justificado"]
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Timesheet {
  id: number
  employee_id: number
  employee_name: string
  date: string
  clock_in: string | null
  clock_out: string | null
  clock_in_2: string | null
  clock_out_2: string | null
  total_minutes: number
  overtime_50_minutes: number
  overtime_100_minutes: number
  night_shift_minutes: number
  justification: string | null
  status: 'ok' | 'inconsistente' | 'justificado'
  created_at: string
  updated_at: string
}

---

### Timesheet Imports

#### Pydantic

class TimesheetImportResponse(BaseModel):
    id: int
    imported_by: int
    imported_by_name: str
    filename: str
    format: Literal["csv", "json", "pdf"]
    records_imported: int
    records_failed: int
    imported_at: datetime

#### TypeScript

export interface TimesheetImport {
  id: number
  imported_by: number
  imported_by_name: string
  filename: string
  format: 'csv' | 'json' | 'pdf'
  records_imported: number
  records_failed: number
  imported_at: string
}

---

### Payrolls

#### Pydantic

class PayrollResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    reference_month: str
    base_salary: float
    overtime_50_value: float
    overtime_100_value: float
    night_additional_value: float
    dsr_value: float
    bonus_value: float
    hazard_pay: float
    unhealthy_pay: float
    gross_salary: float
    inss_value: float
    irrf_value: float
    vt_discount: float
    vr_discount: float
    health_plan_discount: float
    loan_discount: float
    absence_discount: float
    alimony_discount: float
    other_discounts: float
    net_salary: float
    status: Literal["rascunho", "processado", "pago"]
    processed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Payroll {
  id: number
  employee_id: number
  employee_name: string
  reference_month: string
  base_salary: number
  overtime_50_value: number
  overtime_100_value: number
  night_additional_value: number
  dsr_value: number
  bonus_value: number
  hazard_pay: number
  unhealthy_pay: number
  gross_salary: number
  inss_value: number
  irrf_value: number
  vt_discount: number
  vr_discount: number
  health_plan_discount: number
  loan_discount: number
  absence_discount: number
  alimony_discount: number
  other_discounts: number
  net_salary: number
  status: 'rascunho' | 'processado' | 'pago'
  processed_at: string | null
  created_at: string
  updated_at: string
}

---

### Evaluations

#### Pydantic

class EvaluationResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    evaluator_id: int
    evaluator_name: str
    reference_month: str
    score: int
    technical_score: int
    behavioral_score: int
    notes: Optional[str]
    action_plan: Optional[str]
    status: Literal["pendente", "concluido"]
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Evaluation {
  id: number
  employee_id: number
  employee_name: string
  evaluator_id: number
  evaluator_name: string
  reference_month: string
  score: number
  technical_score: number
  behavioral_score: number
  notes: string | null
  action_plan: string | null
  status: 'pendente' | 'concluido'
  created_at: string
  updated_at: string
}

---

### Courses

#### Pydantic

class CourseResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    title: str
    institution: str
    hours: int
    completion_date: date
    certificate_url: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Course {
  id: number
  employee_id: number
  employee_name: string
  title: string
  institution: string
  hours: number
  completion_date: string
  certificate_url: string | null
  description: string | null
  created_at: string
  updated_at: string
}

---

### Loans

#### Pydantic

class LoanResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    total_amount: float
    installments_count: int
    monthly_discount: float
    start_month: str
    reason: str
    status: Literal["ativo", "quitado", "cancelado"]
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface Loan {
  id: number
  employee_id: number
  employee_name: string
  total_amount: number
  installments_count: number
  monthly_discount: number
  start_month: string
  reason: string
  status: 'ativo' | 'quitado' | 'cancelado'
  created_at: string
  updated_at: string
}

---

### Loan Installments

#### Pydantic

class LoanInstallmentResponse(BaseModel):
    id: int
    loan_id: int
    employee_id: int
    employee_name: str
    installment_number: int
    due_month: str
    amount: float
    status: Literal["pendente", "descontado", "atrasado"]
    created_at: datetime
    updated_at: datetime

#### TypeScript

export interface LoanInstallment {
  id: number
  loan_id: number
  employee_id: number
  employee_name: string
  installment_number: number
  due_month: string
  amount: number
  status: 'pendente' | 'descontado' | 'atrasado'
  created_at: string
  updated_at: string
}

---

### Documents

#### Pydantic

class DocumentResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    type: Literal["rg", "cpf", "diploma", "certificado", "outro"]
    filename: str
    file_url: str
    uploaded_at: datetime
    uploaded_by: int
    uploaded_by_name: str

#### TypeScript

export interface Document {
  id: number
  employee_id: number
  employee_name: string
  type: 'rg' | 'cpf' | 'diploma' | 'certificado' | 'outro'
  filename: string
  file_url: string
  uploaded_at: string
  uploaded_by: number
  uploaded_by_name: string
}

---

### Audit Logs

#### Pydantic

class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    action: str
    entity: str
    entity_id: int
    old_value: Optional[dict]
    new_value: Optional[dict]
    ip_address: str
    occurred_at: datetime

#### TypeScript

export interface AuditLog {
  id: number
  user_id: number
  user_name: string
  action: string
  entity: string
  entity_id: number
  old_value: Record<string, any> | null
  new_value: Record<string, any> | null
  ip_address: string
  occurred_at: string
}
