from app.builders.base_builder import AbstractBuilder
from app.models.timesheet import Timesheet
from typing import Optional

class TimesheetBuilder(AbstractBuilder[Timesheet]):
	def reset(self):
		self._data = {}
		self._errors = []

	def set_employee(self, employee_id: int) -> 'TimesheetBuilder':
		self._data["employee_id"] = employee_id
		return self

	def set_date(self, date: str) -> 'TimesheetBuilder':
		self._data["date"] = date
		return self

	def set_times(self, clock_in: Optional[str], clock_out: Optional[str], clock_in_2: Optional[str], clock_out_2: Optional[str]) -> 'TimesheetBuilder':
		self._data["clock_in"] = clock_in
		self._data["clock_out"] = clock_out
		self._data["clock_in_2"] = clock_in_2
		self._data["clock_out_2"] = clock_out_2
		return self

	def set_minutes(self, total: int, overtime_50: int, overtime_100: int, night_shift: int) -> 'TimesheetBuilder':
		self._data["total_minutes"] = total
		self._data["overtime_50_minutes"] = overtime_50
		self._data["overtime_100_minutes"] = overtime_100
		self._data["night_shift_minutes"] = night_shift
		return self

	def set_justification(self, justification: Optional[str]) -> 'TimesheetBuilder':
		self._data["justification"] = justification
		return self

	def set_status(self, status: str) -> 'TimesheetBuilder':
		self._data["status"] = status
		return self

	def build(self) -> Timesheet:
		if not self._data.get("employee_id") or not self._data.get("date"):
			self._errors.append("employee_id e date são obrigatórios")
		if self._errors:
			raise ValueError(f"Erros de validação: {self._errors}")
		timesheet = Timesheet(**self._data)
		self.reset()
		return timesheet
