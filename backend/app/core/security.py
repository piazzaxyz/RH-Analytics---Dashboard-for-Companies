from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import Settings
from app.core.database import get_db
from app.models.user import User, UserRole
from sqlalchemy.orm import Session

settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_password_hash(password: str) -> str:
	return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def create_access_token(data: dict, expires_delta: timedelta = None):
	to_encode = data.copy()
	expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
	to_encode.update({"exp": expire})
	return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str):
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
		return payload
	except JWTError:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
	payload = verify_token(token)
	user_id = payload.get("sub")
	if not user_id:
		raise HTTPException(status_code=401, detail="Token inválido")
	user = db.query(User).filter(User.id == int(user_id)).first()
	if not user or not user.is_active:
		raise HTTPException(status_code=401, detail="Usuário não encontrado ou inativo")
	return user

def require_role(*roles):
	def dependency(user: User = Depends(get_current_user)):
		if user.role.value not in roles:
			raise HTTPException(status_code=403, detail="Permissão negada")
		return user
	return dependency
