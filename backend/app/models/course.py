from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(120), nullable=False)
    institution = Column(String(120), nullable=False)
    hours = Column(Integer, nullable=False)
    completion_date = Column(Date, nullable=False)
    certificate_blob = Column(String, nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False
    )

    employee = relationship("Employee")
