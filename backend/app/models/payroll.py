import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PayrollStatus(enum.Enum):
    rascunho = "rascunho"
    processado = "processado"
    pago = "pago"


class Payroll(Base):
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    reference_month = Column(String(7), nullable=False)
    base_salary = Column(Float, nullable=False)
    overtime_50_value = Column(Float, nullable=False, default=0)
    overtime_100_value = Column(Float, nullable=False, default=0)
    night_additional_value = Column(Float, nullable=False, default=0)
    dsr_value = Column(Float, nullable=False, default=0)
    bonus_value = Column(Float, nullable=False, default=0)
    hazard_pay = Column(Float, nullable=False, default=0)
    unhealthy_pay = Column(Float, nullable=False, default=0)
    gross_salary = Column(Float, nullable=False)
    inss_value = Column(Float, nullable=False)
    irrf_value = Column(Float, nullable=False)
    vt_discount = Column(Float, nullable=False, default=0)
    vr_discount = Column(Float, nullable=False, default=0)
    health_plan_discount = Column(Float, nullable=False, default=0)
    loan_discount = Column(Float, nullable=False, default=0)
    absence_discount = Column(Float, nullable=False, default=0)
    alimony_discount = Column(Float, nullable=False, default=0)
    other_discounts = Column(Float, nullable=False, default=0)
    net_salary = Column(Float, nullable=False)
    status = Column(Enum(PayrollStatus), nullable=False, default=PayrollStatus.rascunho)
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False
    )

    employee = relationship("Employee")
