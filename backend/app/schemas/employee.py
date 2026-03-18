from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime, date

class EmployeeResponse(BaseModel):
	model_config = {"from_attributes": True}

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
	department_id: Optional[int]
	department_name: str
	position_id: Optional[int]
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
