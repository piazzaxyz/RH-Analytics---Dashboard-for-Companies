from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.position import Position
from app.models.user import User
from typing import List

router = APIRouter(prefix="/positions", tags=["positions"])

@router.get("/")
def list_positions(db: Session = Depends(get_db), user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))):
    return [{"id": p.id, "title": p.title, "description": p.description, "base_salary": p.base_salary, "department_id": p.department_id} for p in db.query(Position).all()]
