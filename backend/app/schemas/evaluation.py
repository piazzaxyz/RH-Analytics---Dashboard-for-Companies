from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class EvaluationResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    evaluator_id: int | None
    evaluator_name: str
    evaluation_type: str | None = None
    reference_month: str
    score: int
    technical_score: int
    behavioral_score: int
    notes: str | None
    action_plan: str | None
    status: Literal["pendente", "concluido"]
    created_at: datetime
    updated_at: datetime
