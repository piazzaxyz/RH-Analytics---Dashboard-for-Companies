from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "desenvolvimento-local-chave-secreta-32chars-minimo"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    DATABASE_URL: str = "sqlite:///./database.db"
    ENCRYPTION_KEY: str = ""
    CORS_ORIGINS: str = "http://localhost:5173"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
