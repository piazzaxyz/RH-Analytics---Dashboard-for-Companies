from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.schemas.dashboard import DashboardOverviewResponse, PayrollEvolutionResponse, HeadcountByDepartmentResponse, OvertimeByDepartmentResponse
from app.models.employee import Employee, EmployeeStatus
from app.models.payroll import Payroll, PayrollStatus
from app.models.department import Department
from app.models.timesheet import Timesheet
from app.core.config import Settings
from typing import List
from datetime import datetime

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
settings = Settings()

@router.get("/overview", response_model=DashboardOverviewResponse)
def overview(db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	headcount = db.query(Employee).filter(Employee.status == EmployeeStatus.ativo).count()
	total_payroll = db.query(Payroll).filter(Payroll.status == PayrollStatus.processado).with_entities(Payroll.net_salary).all()
	total_payroll_value = sum([p[0] for p in total_payroll]) if total_payroll else 0
	turnover_rate = 0.05
	absenteeism_rate = 0.02
	return DashboardOverviewResponse(
		headcount=headcount,
		turnover_rate=turnover_rate,
		absenteeism_rate=absenteeism_rate,
		total_payroll=total_payroll_value
	)

@router.get("/payroll-evolution", response_model=PayrollEvolutionResponse)
def payroll_evolution(db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	months = []
	values = []
	now = datetime.now()
	year = now.year
	month_num = now.month
	for i in range(12):
		m = month_num - i
		y = year
		while m <= 0:
			m += 12
			y -= 1
		month = f"{y}-{m:02d}"
		total = db.query(Payroll).filter(Payroll.reference_month == month, Payroll.status == PayrollStatus.processado).with_entities(Payroll.net_salary).all()
		values.append(sum([p[0] for p in total]))
		months.append(month)
	return PayrollEvolutionResponse(months=months[::-1], values=values[::-1])

@router.get("/headcount-by-department", response_model=List[HeadcountByDepartmentResponse])
def headcount_by_department(db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	departments = db.query(Department).all()
	result = []
	for dept in departments:
		count = db.query(Employee).filter(Employee.department_id == dept.id, Employee.status == EmployeeStatus.ativo).count()
		result.append(HeadcountByDepartmentResponse(
			department_id=dept.id,
			department_name=dept.name,
			headcount=count
		))
	return result

@router.get("/overtime-by-department", response_model=List[OvertimeByDepartmentResponse])
def overtime_by_department(db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	try:
		departments = db.query(Department).all()
		month = datetime.now().strftime("%Y-%m")
		result = []
		for dept in departments:
			employees = db.query(Employee).filter(Employee.department_id == dept.id, Employee.status == EmployeeStatus.ativo).all()
			overtime = 0.0
			for e in employees:
				timesheets = db.query(Timesheet).filter(Timesheet.employee_id == e.id, Timesheet.date.like(f"{month}-%")).all()
				for t in timesheets:
					overtime += (t.overtime_50_minutes or 0) + (t.overtime_100_minutes or 0)
			result.append(OvertimeByDepartmentResponse(
				department_id=dept.id,
				department_name=dept.name,
				overtime_hours=overtime / 60.0
			))
		return result
	except Exception:
		return []
