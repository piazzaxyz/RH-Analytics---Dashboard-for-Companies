import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class LoanInstallmentStatus(enum.Enum):
    pendente = "pendente"
    descontado = "descontado"
    atrasado = "atrasado"


class LoanInstallment(Base):
    __tablename__ = "loan_installments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False)
    installment_number = Column(Integer, nullable=False)
    due_month = Column(String(7), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(LoanInstallmentStatus), nullable=False, default=LoanInstallmentStatus.pendente)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False
    )

    loan = relationship("Loan")
