from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

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
