from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.schemas.loan import LoanResponse, LoanInstallmentResponse
from app.models.loan import Loan, LoanStatus
from app.models.loan_installment import LoanInstallment, LoanInstallmentStatus
from app.services.audit_service import log_audit
from app.core.config import Settings
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/loans", tags=["loans"])
settings = Settings()

@router.get("/", response_model=List[LoanResponse])
def list_loans(
	employee_id: Optional[int] = None,
	status: Optional[str] = None,
	db: Session = Depends(get_db),
	user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))
):
	from app.models.loan import LoanStatus
	query = db.query(Loan)
	if employee_id:
		query = query.filter(Loan.employee_id == employee_id)
	if status:
		query = query.filter(Loan.status == LoanStatus(status))
	loans = query.all()
	return [LoanResponse(
		id=l.id,
		employee_id=l.employee_id,
		employee_name="",
		total_amount=l.total_amount,
		installments_count=l.installments_count,
		monthly_discount=l.monthly_discount,
		start_month=l.start_month,
		reason=l.reason,
		status=l.status.value,
		created_at=l.created_at,
		updated_at=l.updated_at
	) for l in loans]

@router.post("/", response_model=LoanResponse)
def create_loan(data: dict = Body(...), db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	loan = Loan(**data)
	db.add(loan)
	db.commit()
	db.refresh(loan)
	log_audit(db, user.id, "create_loan", "loan", loan.id, None, data, "127.0.0.1")
	return LoanResponse(
		id=loan.id,
		employee_id=loan.employee_id,
		employee_name="",
		total_amount=loan.total_amount,
		installments_count=loan.installments_count,
		monthly_discount=loan.monthly_discount,
		start_month=loan.start_month,
		reason=loan.reason,
		status=loan.status.value,
		created_at=loan.created_at,
		updated_at=loan.updated_at
	)

@router.get("/{id}", response_model=LoanResponse)
def get_loan(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	loan = db.query(Loan).filter(Loan.id == id).first()
	if not loan:
		raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
	return LoanResponse(
		id=loan.id,
		employee_id=loan.employee_id,
		employee_name="",
		total_amount=loan.total_amount,
		installments_count=loan.installments_count,
		monthly_discount=loan.monthly_discount,
		start_month=loan.start_month,
		reason=loan.reason,
		status=loan.status.value,
		created_at=loan.created_at,
		updated_at=loan.updated_at
	)

@router.put("/{id}", response_model=LoanResponse)
def update_loan(id: int, data: dict, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	loan = db.query(Loan).filter(Loan.id == id).first()
	if not loan:
		raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
	old_data = {c.name: getattr(loan, c.name) for c in loan.__table__.columns}
	for key, value in data.items():
		setattr(loan, key, value)
	db.commit()
	db.refresh(loan)
	log_audit(db, user.id, "update_loan", "loan", loan.id, old_data, data, "127.0.0.1")
	return LoanResponse(
		id=loan.id,
		employee_id=loan.employee_id,
		employee_name="",
		total_amount=loan.total_amount,
		installments_count=loan.installments_count,
		monthly_discount=loan.monthly_discount,
		start_month=loan.start_month,
		reason=loan.reason,
		status=loan.status.value,
		created_at=loan.created_at,
		updated_at=loan.updated_at
	)

@router.get("/{id}/installments", response_model=List[LoanInstallmentResponse])
def list_installments(id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
	loan = db.query(Loan).filter(Loan.id == id).first()
	if not loan:
		raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
	installments = db.query(LoanInstallment).filter(LoanInstallment.loan_id == id).all()
	return [LoanInstallmentResponse(
		id=i.id,
		loan_id=i.loan_id,
		employee_id=loan.employee_id,
		employee_name="",
		installment_number=i.installment_number,
		due_month=i.due_month,
		amount=i.amount,
		status=i.status.value,
		created_at=i.created_at,
		updated_at=i.updated_at
	) for i in installments]
