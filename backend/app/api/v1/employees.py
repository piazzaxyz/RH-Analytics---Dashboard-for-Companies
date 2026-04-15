from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Body
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role, get_current_user
from app.schemas.employee import EmployeeResponse
from app.schemas.payroll import PayrollResponse
from app.schemas.evaluation import EvaluationResponse
from app.models.employee import Employee, EmployeeStatus
from app.models.department import Department
from app.models.position import Position
from app.models.user import User
from app.models.document import Document, DocumentType
from app.models.payroll import Payroll
from app.models.evaluation import Evaluation
from app.builders.employee_builder import EmployeeBuilder
from app.services.audit_service import log_audit
from app.core.config import Settings
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/employees", tags=["employees"])
settings = Settings()

@router.get("/", response_model=List[EmployeeResponse])
def list_employees(
	status: Optional[str] = None,
	department_id: Optional[int] = None,
	search: Optional[str] = None,
	skip: int = 0,
	limit: int = 20,
	db: Session = Depends(get_db),
	user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))
):
	query = db.query(Employee)
	if status:
		status_enum = EmployeeStatus.ativo if status.lower() == "ativo" else EmployeeStatus.inativo
		query = query.filter(Employee.status == status_enum)
	if department_id:
		query = query.filter(Employee.department_id == department_id)
	if search:
		query = query.filter(Employee.full_name.ilike(f"%{search}%"))
	employees = query.offset(skip).limit(limit).all()
	return [_employee_to_response(e, db) for e in employees]

@router.post("/", response_model=EmployeeResponse)
def create_employee(
	data: dict = Body(...),
	db: Session = Depends(get_db),
	user: User = Depends(require_role("admin", "rh"))
):
	try:
		builder = EmployeeBuilder()
		builder.set_personal_data(**data)
		builder.set_work_data(**data)
		builder.set_bank_data(**data)
		builder.set_photo(data.get("photo_blob"))
		employee = builder.build()
	except ValueError as e:
		raise HTTPException(status_code=400, detail=str(e))
	dept_id = data.get("department_id")
	pos_id = data.get("position_id")
	if dept_id and not db.query(Department).filter(Department.id == dept_id).first():
		raise HTTPException(status_code=400, detail="Departamento não encontrado")
	if pos_id and not db.query(Position).filter(Position.id == pos_id).first():
		raise HTTPException(status_code=400, detail="Cargo não encontrado")
	db.add(employee)
	try:
		db.commit()
		db.refresh(employee)
	except Exception as e:
		db.rollback()
		raise HTTPException(status_code=400, detail=str(e))
	log_audit(db, user.id, "create", "employee", employee.id, None, data, "127.0.0.1")
	return _employee_to_response(employee, db)


def _employee_to_response(e, db: Session) -> EmployeeResponse:
	department = db.query(Department).filter(Department.id == e.department_id).first()
	position = db.query(Position).filter(Position.id == e.position_id).first()
	supervisor = db.query(Employee).filter(Employee.id == e.supervisor_id).first() if e.supervisor_id else None
	return EmployeeResponse(
		id=e.id, full_name=e.full_name, cpf=e.cpf, rg=e.rg, birth_date=e.birth_date,
		address=e.address, phone=e.phone, email=e.email, work_card_number=e.work_card_number,
		work_card_series=e.work_card_series, admission_date=e.admission_date, dismissal_date=e.dismissal_date,
		status=e.status.value, department_id=e.department_id, department_name=department.name if department else "",
		position_id=e.position_id, position_title=position.title if position else "",
		supervisor_id=e.supervisor_id, supervisor_name=supervisor.full_name if supervisor else None,
		bank_name=e.bank_name, bank_agency=e.bank_agency, bank_account=e.bank_account,
		bank_account_type=e.bank_account_type, photo_url=f"/api/v1/employees/{e.id}/photo" if e.photo_blob else None,
		salary=e.salary, pis_pasep=e.pis_pasep, created_at=e.created_at, updated_at=e.updated_at
	)


@router.post("/{id}/photo", response_model=EmployeeResponse)
def upload_photo(id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	e = db.query(Employee).filter(Employee.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Colaborador não encontrado")
	blob = file.file.read()
	e.photo_blob = blob.hex()
	db.commit()
	db.refresh(e)
	log_audit(db, user.id, "upload_photo", "employee", e.id, None, {"photo_blob": "uploaded"}, "127.0.0.1")
	return _employee_to_response(e, db)


@router.get("/{id}/photo")
def get_photo(id: int, db: Session = Depends(get_db)):
	e = db.query(Employee).filter(Employee.id == id).first()
	if not e or not e.photo_blob:
		raise HTTPException(status_code=404, detail="Foto não encontrada")
	return Response(content=bytes.fromhex(e.photo_blob), media_type="image/jpeg")


@router.post("/{id}/documents")
def upload_document(id: int, file: UploadFile = File(...), type: str = "outro", db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	e = db.query(Employee).filter(Employee.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Colaborador não encontrado")
	try:
		doc_type = DocumentType(type)
	except ValueError:
		doc_type = DocumentType.outro
	blob = file.file.read()
	doc = Document(employee_id=id, type=doc_type, filename=file.filename or "file", file_blob=blob.hex(), uploaded_by=user.id)
	db.add(doc)
	db.commit()
	db.refresh(doc)
	log_audit(db, user.id, "upload_document", "employee", e.id, None, {"document": file.filename}, "127.0.0.1")
	return {"id": doc.id, "filename": doc.filename, "type": doc.type.value}


@router.get("/{id}/documents")
def list_documents(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	docs = db.query(Document).filter(Document.employee_id == id).all()
	return [{"id": d.id, "filename": d.filename, "type": d.type.value, "uploaded_at": d.uploaded_at} for d in docs]


@router.get("/{id}/payrolls", response_model=List[PayrollResponse])
def list_payrolls(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	payrolls = db.query(Payroll).filter(Payroll.employee_id == id).all()
	emp = db.query(Employee).filter(Employee.id == id).first()
	emp_name = emp.full_name if emp else ""
	return [PayrollResponse(id=p.id, employee_id=p.employee_id, employee_name=emp_name, reference_month=p.reference_month,
		base_salary=p.base_salary, overtime_50_value=p.overtime_50_value, overtime_100_value=p.overtime_100_value,
		night_additional_value=p.night_additional_value, dsr_value=p.dsr_value, bonus_value=p.bonus_value,
		hazard_pay=p.hazard_pay, unhealthy_pay=p.unhealthy_pay, gross_salary=p.gross_salary, inss_value=p.inss_value,
		irrf_value=p.irrf_value, vt_discount=p.vt_discount, vr_discount=p.vr_discount,
		health_plan_discount=p.health_plan_discount, loan_discount=p.loan_discount, absence_discount=p.absence_discount,
		alimony_discount=p.alimony_discount, other_discounts=p.other_discounts, net_salary=p.net_salary,
		status=p.status.value, processed_at=p.processed_at, created_at=p.created_at, updated_at=p.updated_at) for p in payrolls]


@router.get("/{id}/evaluations", response_model=List[EvaluationResponse])
def list_evaluations(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	evals = db.query(Evaluation).filter(Evaluation.employee_id == id).all()
	emp = db.query(Employee).filter(Employee.id == id).first()
	emp_name = emp.full_name if emp else ""
	evaluator_ids = list(set(e.evaluator_id for e in evals if e.evaluator_id))
	evaluator_names = {u.id: u.username for u in db.query(User).filter(User.id.in_(evaluator_ids)).all()} if evaluator_ids else {}
	return [EvaluationResponse(id=e.id, employee_id=e.employee_id, employee_name=emp_name, evaluator_id=e.evaluator_id,
		evaluator_name=evaluator_names.get(e.evaluator_id, ""), reference_month=e.reference_month, score=e.score,
		technical_score=e.technical_score, behavioral_score=e.behavioral_score, notes=e.notes,
		action_plan=e.action_plan, status=e.status.value,
		created_at=e.created_at, updated_at=e.updated_at) for e in evals]


@router.get("/{id}", response_model=EmployeeResponse)
def get_employee(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	e = db.query(Employee).filter(Employee.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Colaborador não encontrado")
	return _employee_to_response(e, db)

def _parse_date(val):
	if val is None or val == "":
		return None
	if hasattr(val, "year"):
		return val
	try:
		from datetime import datetime
		return datetime.strptime(str(val)[:10], "%Y-%m-%d").date()
	except (ValueError, TypeError):
		return None

@router.put("/{id}", response_model=EmployeeResponse)
def update_employee(id: int, data: dict = Body(...), db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	e = db.query(Employee).filter(Employee.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Colaborador não encontrado")
	old_data = {c.name: getattr(e, c.name) for c in e.__table__.columns}
	date_fields = {"birth_date", "admission_date", "dismissal_date"}
	valid_cols = {c.name for c in e.__table__.columns}
	for key, value in data.items():
		if key not in valid_cols or key == "id":
			continue
		if key in date_fields and value is not None:
			parsed = _parse_date(value)
			if parsed is not None:
				setattr(e, key, parsed)
		else:
			setattr(e, key, value)
	db.commit()
	db.refresh(e)
	log_audit(db, user.id, "update", "employee", e.id, old_data, data, "127.0.0.1")
	return _employee_to_response(e, db)

@router.delete("/{id}", response_model=EmployeeResponse)
def delete_employee(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	e = db.query(Employee).filter(Employee.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Colaborador não encontrado")
	old_data = {c.name: getattr(e, c.name) for c in e.__table__.columns}
	e.status = EmployeeStatus.inativo
	db.commit()
	db.refresh(e)
	log_audit(db, user.id, "delete", "employee", e.id, old_data, {"status": "inativo"}, "127.0.0.1")
	return _employee_to_response(e, db)
