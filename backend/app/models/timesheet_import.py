from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class TimesheetImportFormat(enum.Enum):
    csv = "csv"
    json = "json"
    pdf = "pdf"

class TimesheetImport(Base):
    __tablename__ = "timesheet_imports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    imported_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    filename = Column(String(255), nullable=False)
    format = Column(Enum(TimesheetImportFormat), nullable=False)
    records_imported = Column(Integer, nullable=False, default=0)
    records_failed = Column(Integer, nullable=False, default=0)
    imported_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)

    user = relationship("User")
