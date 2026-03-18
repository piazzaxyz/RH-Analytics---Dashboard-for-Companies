from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.core.database import Base, engine
import app.models.employee
import app.models.department
import app.models.position
import app.models.user
import app.models.audit
import app.models.course
import app.models.document
import app.models.evaluation
import app.models.loan
import app.models.loan_installment
import app.models.payroll
import app.models.position_history
import app.models.timesheet
import app.models.timesheet_import

settings = Settings()

CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173", "http://[::1]:5173"]
if settings.CORS_ORIGINS:
    CORS_ORIGINS = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE evaluations ADD COLUMN evaluation_type VARCHAR(50)"))
            conn.commit()
    except Exception:
        pass
    yield


app = FastAPI(title="Dashboard RH", lifespan=lifespan, redirect_slash=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

from app.api import router as api_router
app.include_router(api_router)
