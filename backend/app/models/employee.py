from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class EmployeeStatus(enum.Enum):
	ativo = "ativo"
	inativo = "inativo"

class Employee(Base):
	__tablename__ = "employees"

	id = Column(Integer, primary_key=True, autoincrement=True)
	full_name = Column(String(120), nullable=False)
	cpf = Column(String(14), unique=True, nullable=False)
	rg = Column(String(20), nullable=False)
	birth_date = Column(Date, nullable=False)
	address = Column(String(255), nullable=False)
	phone = Column(String(20), nullable=False)
	email = Column(String(120), nullable=False)
	work_card_number = Column(String(20), nullable=False)
	work_card_series = Column(String(10), nullable=False)
	admission_date = Column(Date, nullable=False)
	dismissal_date = Column(Date, nullable=True)
	status = Column(Enum(EmployeeStatus), nullable=False, default=EmployeeStatus.ativo)
	department_id = Column(Integer, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
	position_id = Column(Integer, ForeignKey("positions.id", ondelete="SET NULL"), nullable=True)
	supervisor_id = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"), nullable=True)
	bank_name = Column(String(50), nullable=False)
	bank_agency = Column(String(20), nullable=False)
	bank_account = Column(String(20), nullable=False)
	bank_account_type = Column(String(20), nullable=False)
	photo_blob = Column(String, nullable=True)
	salary = Column(Float, nullable=False)
	pis_pasep = Column(String(20), nullable=False)
	created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
	updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

	department = relationship("Department", back_populates="employees")
	position = relationship("Position", back_populates="employees")
	supervisor = relationship("Employee", remote_side=[id])
