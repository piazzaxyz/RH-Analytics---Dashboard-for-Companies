from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
	get_password_hash, verify_password, create_access_token, verify_token, get_current_user, require_role
)
from app.schemas.auth import UserResponse, AuthTokenResponse
from app.models.user import User
from app.core.config import Settings
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
settings = Settings()

@router.post("/login", response_model=AuthTokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	username = form_data.username
	password = form_data.password
	user = db.query(User).filter(User.username == username).first()
	if not user or not verify_password(password, user.hashed_password):
		raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
	access_token = create_access_token({"sub": str(user.id)}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	return AuthTokenResponse(
		access_token=access_token,
		token_type="bearer",
		user=UserResponse(
			id=user.id,
			username=user.username,
			email=user.email,
			role=user.role.value,
			is_active=user.is_active,
			created_at=user.created_at,
			updated_at=user.updated_at
		)
	)

@router.post("/refresh", response_model=AuthTokenResponse)
def refresh(token: str, db: Session = Depends(get_db)):
	payload = verify_token(token)
	user_id = payload.get("sub")
	user = db.query(User).filter(User.id == int(user_id)).first()
	if not user:
		raise HTTPException(status_code=401, detail="Usuário não encontrado")
	access_token = create_access_token({"sub": str(user.id)}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	return AuthTokenResponse(
		access_token=access_token,
		token_type="bearer",
		user=UserResponse(
			id=user.id,
			username=user.username,
			email=user.email,
			role=user.role.value,
			is_active=user.is_active,
			created_at=user.created_at,
			updated_at=user.updated_at
		)
	)

@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
	return UserResponse(
		id=user.id,
		username=user.username,
		email=user.email,
		role=user.role.value,
		is_active=user.is_active,
		created_at=user.created_at,
		updated_at=user.updated_at
	)
