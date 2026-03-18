from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(enum.Enum):
	admin = "admin"
	gestor = "gestor"
	rh = "rh"
	visualizador = "visualizador"

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, autoincrement=True)
	username = Column(String(50), unique=True, nullable=False)
	email = Column(String(120), unique=True, nullable=False)
	hashed_password = Column(String(128), nullable=False)
	role = Column(Enum(UserRole), nullable=False)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
	updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)
