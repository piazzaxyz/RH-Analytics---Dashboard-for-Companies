from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class EvaluationStatus(enum.Enum):
	pendente = "pendente"
	concluido = "concluido"

class Evaluation(Base):
	__tablename__ = "evaluations"

	id = Column(Integer, primary_key=True, autoincrement=True)
	employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
	evaluator_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
	evaluation_type = Column(String(50), nullable=True)
	reference_month = Column(String(7), nullable=False)
	score = Column(Integer, nullable=False)
	technical_score = Column(Integer, nullable=False)
	behavioral_score = Column(Integer, nullable=False)
	notes = Column(String(255), nullable=True)
	action_plan = Column(String(255), nullable=True)
	status = Column(Enum(EvaluationStatus), nullable=False, default=EvaluationStatus.pendente)
	created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
	updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

	employee = relationship("Employee")
	evaluator = relationship("User")
