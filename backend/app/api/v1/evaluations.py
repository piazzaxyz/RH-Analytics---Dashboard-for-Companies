from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.schemas.evaluation import EvaluationResponse
from app.models.evaluation import Evaluation, EvaluationStatus
from app.models.user import User
from app.models.employee import Employee
from app.services.audit_service import log_audit
from app.core.config import Settings
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/evaluations", tags=["evaluations"])
settings = Settings()

@router.get("/", response_model=List[EvaluationResponse])
def list_evaluations(
	employee_id: Optional[int] = None,
	month: Optional[str] = None,
	db: Session = Depends(get_db),
	user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))
):
	query = db.query(Evaluation)
	if employee_id:
		query = query.filter(Evaluation.employee_id == employee_id)
	if month:
		query = query.filter(Evaluation.reference_month == month)
	evals = query.all()
	emp_names = {e.id: e.full_name for e in db.query(Employee).filter(Employee.id.in_([x.employee_id for x in evals])).all()} if evals else {}
	return [EvaluationResponse(
		id=e.id,
		employee_id=e.employee_id,
		employee_name=emp_names.get(e.employee_id, ""),
		evaluator_id=e.evaluator_id,
		evaluator_name="",
		evaluation_type=getattr(e, "evaluation_type", None),
		reference_month=e.reference_month,
		score=e.score,
		technical_score=e.technical_score,
		behavioral_score=e.behavioral_score,
		notes=e.notes,
		action_plan=e.action_plan,
		status=e.status.value,
		created_at=e.created_at,
		updated_at=e.updated_at
	) for e in evals]

@router.post("/", response_model=EvaluationResponse)
def create_evaluation(data: dict = Body(...), db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	data = dict(data)
	data.setdefault("evaluator_id", user.id)
	data.setdefault("status", "pendente")
	e = Evaluation(**data)
	db.add(e)
	db.commit()
	db.refresh(e)
	log_audit(db, user.id, "create_evaluation", "evaluation", e.id, None, data, "127.0.0.1")
	return EvaluationResponse(
		id=e.id,
		employee_id=e.employee_id,
		employee_name="",
		evaluator_id=e.evaluator_id,
		evaluator_name="",
		evaluation_type=getattr(e, "evaluation_type", None),
		reference_month=e.reference_month,
		score=e.score,
		technical_score=e.technical_score,
		behavioral_score=e.behavioral_score,
		notes=e.notes,
		action_plan=e.action_plan,
		status=e.status.value,
		created_at=e.created_at,
		updated_at=e.updated_at
	)

@router.get("/{id}", response_model=EvaluationResponse)
def get_evaluation(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	e = db.query(Evaluation).filter(Evaluation.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Avaliação não encontrada")
	return EvaluationResponse(
		id=e.id,
		employee_id=e.employee_id,
		employee_name="",
		evaluator_id=e.evaluator_id,
		evaluator_name="",
		evaluation_type=getattr(e, "evaluation_type", None),
		reference_month=e.reference_month,
		score=e.score,
		technical_score=e.technical_score,
		behavioral_score=e.behavioral_score,
		notes=e.notes,
		action_plan=e.action_plan,
		status=e.status.value,
		created_at=e.created_at,
		updated_at=e.updated_at
	)

@router.put("/{id}", response_model=EvaluationResponse)
def update_evaluation(id: int, data: dict, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	e = db.query(Evaluation).filter(Evaluation.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Avaliação não encontrada")
	old_data = {c.name: getattr(e, c.name) for c in e.__table__.columns}
	for key, value in data.items():
		setattr(e, key, value)
	db.commit()
	db.refresh(e)
	log_audit(db, user.id, "update_evaluation", "evaluation", e.id, old_data, data, "127.0.0.1")
	return EvaluationResponse(
		id=e.id,
		employee_id=e.employee_id,
		employee_name="",
		evaluator_id=e.evaluator_id,
		evaluator_name="",
		evaluation_type=getattr(e, "evaluation_type", None),
		reference_month=e.reference_month,
		score=e.score,
		technical_score=e.technical_score,
		behavioral_score=e.behavioral_score,
		notes=e.notes,
		action_plan=e.action_plan,
		status=e.status.value,
		created_at=e.created_at,
		updated_at=e.updated_at
	)

@router.post("/{id}/conclude", response_model=EvaluationResponse)
def conclude_evaluation(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	e = db.query(Evaluation).filter(Evaluation.id == id).first()
	if not e:
		raise HTTPException(status_code=404, detail="Avaliação não encontrada")
	e.status = EvaluationStatus.concluido
	db.commit()
	db.refresh(e)
	log_audit(db, user.id, "conclude_evaluation", "evaluation", e.id, None, {"status": "concluido"}, "127.0.0.1")
	return EvaluationResponse(
		id=e.id,
		employee_id=e.employee_id,
		employee_name="",
		evaluator_id=e.evaluator_id,
		evaluator_name="",
		evaluation_type=getattr(e, "evaluation_type", None),
		reference_month=e.reference_month,
		score=e.score,
		technical_score=e.technical_score,
		behavioral_score=e.behavioral_score,
		notes=e.notes,
		action_plan=e.action_plan,
		status=e.status.value,
		created_at=e.created_at,
		updated_at=e.updated_at
	)
