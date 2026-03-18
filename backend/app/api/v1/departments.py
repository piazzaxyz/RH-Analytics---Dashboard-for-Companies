from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.department import Department
from app.models.user import User
from typing import List

router = APIRouter(prefix="/departments", tags=["departments"])

@router.get("/")
def list_departments(db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
    return [{"id": d.id, "name": d.name, "description": d.description} for d in db.query(Department).all()]
