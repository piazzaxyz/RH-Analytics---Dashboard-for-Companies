import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class DocumentType(enum.Enum):
    rg = "rg"
    cpf = "cpf"
    diploma = "diploma"
    certificado = "certificado"
    outro = "outro"


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    type = Column(Enum(DocumentType), nullable=False)
    filename = Column(String(255), nullable=False)
    file_blob = Column(String, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    employee = relationship("Employee")
    user = relationship("User")
