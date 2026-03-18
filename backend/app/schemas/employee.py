from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


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
    dismissal_date: date | None
    status: Literal["ativo", "inativo"]
    department_id: int | None
    department_name: str
    position_id: int | None
    position_title: str
    supervisor_id: int | None
    supervisor_name: str | None
    bank_name: str
    bank_agency: str
    bank_account: str
    bank_account_type: str
    photo_url: str | None
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
    end_date: date | None
    reason: str
    created_at: datetime
    updated_at: datetime
