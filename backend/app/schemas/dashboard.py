from pydantic import BaseModel


class DashboardOverviewResponse(BaseModel):
    headcount: int
    turnover_rate: float
    absenteeism_rate: float
    total_payroll: float


class PayrollEvolutionResponse(BaseModel):
    months: list[str]
    values: list[float]


class HeadcountByDepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    headcount: int


class OvertimeByDepartmentResponse(BaseModel):
    department_id: int
    department_name: str
    overtime_hours: float
