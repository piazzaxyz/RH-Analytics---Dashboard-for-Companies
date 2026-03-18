from datetime import date, datetime, time
from typing import Literal

from pydantic import BaseModel


class TimesheetResponse(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    date: date
    clock_in: time | None
    clock_out: time | None
    clock_in_2: time | None
    clock_out_2: time | None
    total_minutes: int
    overtime_50_minutes: int
    overtime_100_minutes: int
    night_shift_minutes: int
    overtime_disposition: str | None = None
    overtime_parecer: str | None = None
    overtime_used: int | None = None
    justification: str | None = None
    status: Literal["ok", "inconsistente", "justificado"]
    created_at: datetime
    updated_at: datetime


class TimesheetImportResponse(BaseModel):
    id: int
    imported_by: int
    imported_by_name: str
    filename: str
    format: Literal["csv", "json", "pdf"]
    records_imported: int
    records_failed: int
    imported_at: datetime
