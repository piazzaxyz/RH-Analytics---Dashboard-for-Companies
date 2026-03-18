from datetime import datetime
from typing import Literal

from pydantic import BaseModel


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
    processed_at: datetime | None
    created_at: datetime
    updated_at: datetime
