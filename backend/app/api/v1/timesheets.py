from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_role
from app.models.user import User
from app.schemas.timesheet import TimesheetResponse, TimesheetImportResponse
from app.models.timesheet import Timesheet, TimesheetStatus
from app.models.timesheet_import import TimesheetImport, TimesheetImportFormat
from app.services.file_parser import parse_csv, parse_json, parse_pdf
from app.services.audit_service import log_audit
from app.core.config import Settings
from typing import List, Optional
from datetime import datetime, date

router = APIRouter(prefix="/timesheets", tags=["timesheets"])
settings = Settings()

@router.get("/", response_model=List[TimesheetResponse])
def list_timesheets(
	employee_id: Optional[int] = None,
	month: Optional[str] = None,
	db: Session = Depends(get_db),
	user: User = Depends(require_role("admin", "gestor", "rh", "visualizador"))
):
	query = db.query(Timesheet)
	if employee_id:
		query = query.filter(Timesheet.employee_id == employee_id)
	if month:
		query = query.filter(Timesheet.date.like(f"{month}-%"))
	timesheets = query.all()
	return [TimesheetResponse(
		id=t.id,
		employee_id=t.employee_id,
		employee_name="", # Preencher com join se necessário
		date=t.date,
		clock_in=t.clock_in,
		clock_out=t.clock_out,
		clock_in_2=t.clock_in_2,
		clock_out_2=t.clock_out_2,
		total_minutes=t.total_minutes,
		overtime_50_minutes=t.overtime_50_minutes,
		overtime_100_minutes=t.overtime_100_minutes,
		night_shift_minutes=t.night_shift_minutes,
		justification=t.justification,
		status=t.status.value,
		created_at=t.created_at,
		updated_at=t.updated_at
	) for t in timesheets]

@router.post("/import", response_model=TimesheetImportResponse)
def import_timesheets(
	file: UploadFile = File(...),
	format: str = "csv",
	db: Session = Depends(get_db),
	user: User = Depends(require_role("admin", "rh"))
):
	if format == "csv":
		records = parse_csv(file.file)
	elif format == "json":
		records = parse_json(file.file)
	elif format == "pdf":
		records = parse_pdf(file.file)
	else:
		raise HTTPException(status_code=400, detail="Formato inválido")
	imported = 0
	failed = 0
	for rec in records:
		try:
			if isinstance(rec, dict) and "employee_id" in rec and "date" in rec:
				d = rec["date"]
				date_val = d if isinstance(d, date) else datetime.strptime(str(d)[:10], "%Y-%m-%d").date()
				t = Timesheet(
					employee_id=int(rec["employee_id"]),
					date=date_val,
					total_minutes=int(rec.get("total_minutes", 0)),
					overtime_50_minutes=int(rec.get("overtime_50_minutes", 0)),
					overtime_100_minutes=int(rec.get("overtime_100_minutes", 0)),
					night_shift_minutes=int(rec.get("night_shift_minutes", 0))
				)
				db.add(t)
				imported += 1
		except Exception:
			failed += 1
	db.commit()
	fmt = TimesheetImportFormat.csv if format == "csv" else (TimesheetImportFormat.json if format == "json" else TimesheetImportFormat.pdf)
	imp = TimesheetImport(
		imported_by=user.id,
		filename=file.filename or "upload",
		format=fmt,
		records_imported=imported,
		records_failed=failed
	)
	db.add(imp)
	db.commit()
	db.refresh(imp)
	log_audit(db, user.id, "import_timesheets", "timesheet_import", imp.id, None, {"filename": file.filename}, "127.0.0.1")
	return TimesheetImportResponse(
		id=imp.id,
		imported_by=imp.imported_by,
		imported_by_name="",
		filename=imp.filename,
		format=imp.format.value,
		records_imported=imp.records_imported,
		records_failed=imp.records_failed,
		imported_at=imp.imported_at
	)

@router.put("/{id}", response_model=TimesheetResponse)
def edit_timesheet(id: int, data: dict, db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	t = db.query(Timesheet).filter(Timesheet.id == id).first()
	if not t:
		raise HTTPException(status_code=404, detail="Registro de ponto não encontrado")
	old_data = {c.name: getattr(t, c.name) for c in t.__table__.columns}
	for key, value in data.items():
		setattr(t, key, value)
	db.commit()
	db.refresh(t)
	log_audit(db, user.id, "edit_timesheet", "timesheet", t.id, old_data, data, "127.0.0.1")
	return TimesheetResponse(
		id=t.id,
		employee_id=t.employee_id,
		employee_name="",
		date=t.date,
		clock_in=t.clock_in,
		clock_out=t.clock_out,
		clock_in_2=t.clock_in_2,
		clock_out_2=t.clock_out_2,
		total_minutes=t.total_minutes,
		overtime_50_minutes=t.overtime_50_minutes,
		overtime_100_minutes=t.overtime_100_minutes,
		night_shift_minutes=t.night_shift_minutes,
		justification=t.justification,
		status=t.status.value,
		created_at=t.created_at,
		updated_at=t.updated_at
	)

@router.get("/inconsistencies", response_model=List[TimesheetResponse])
def list_inconsistencies(db: Session = Depends(get_db), user: User = Depends(require_role("admin", "rh"))):
	timesheets = db.query(Timesheet).filter(Timesheet.status == TimesheetStatus.inconsistente).all()
	return [TimesheetResponse(
		id=t.id,
		employee_id=t.employee_id,
		employee_name="",
		date=t.date,
		clock_in=t.clock_in,
		clock_out=t.clock_out,
		clock_in_2=t.clock_in_2,
		clock_out_2=t.clock_out_2,
		total_minutes=t.total_minutes,
		overtime_50_minutes=t.overtime_50_minutes,
		overtime_100_minutes=t.overtime_100_minutes,
		night_shift_minutes=t.night_shift_minutes,
		justification=t.justification,
		status=t.status.value,
		created_at=t.created_at,
		updated_at=t.updated_at
	) for t in timesheets]
