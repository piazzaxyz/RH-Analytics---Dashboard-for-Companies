from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class LoanStatus(enum.Enum):
	ativo = "ativo"
	quitado = "quitado"
	cancelado = "cancelado"

class Loan(Base):
	__tablename__ = "loans"

	id = Column(Integer, primary_key=True, autoincrement=True)
	employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
	total_amount = Column(Float, nullable=False)
	installments_count = Column(Integer, nullable=False)
	monthly_discount = Column(Float, nullable=False)
	start_month = Column(String(7), nullable=False)
	reason = Column(String(255), nullable=False)
	status = Column(Enum(LoanStatus), nullable=False, default=LoanStatus.ativo)
	created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
	updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

	employee = relationship("Employee")
