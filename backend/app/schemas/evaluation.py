from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class EvaluationResponse(BaseModel):
	id: int
	employee_id: int
	employee_name: str
	evaluator_id: Optional[int]
	evaluator_name: str
	evaluation_type: Optional[str] = None
	reference_month: str
	score: int
	technical_score: int
	behavioral_score: int
	notes: Optional[str]
	action_plan: Optional[str]
	status: Literal["pendente", "concluido"]
	created_at: datetime
	updated_at: datetime
