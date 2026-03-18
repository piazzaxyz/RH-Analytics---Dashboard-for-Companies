from datetime import date
from app.builders.base_builder import AbstractBuilder
from app.models.employee import Employee, EmployeeStatus
from typing import Optional

def _parse_date(val) -> Optional[date]:
	if val is None or val == "":
		return None
	if isinstance(val, date):
		return val
	s = str(val).strip()
	if not s:
		return None
	try:
		return date.fromisoformat(s[:10])
	except (ValueError, TypeError):
		return None

class EmployeeBuilder(AbstractBuilder[Employee]):
	def reset(self):
		self._data = {}
		self._documents = []
		self._errors = []

	def set_personal_data(self, **kwargs) -> 'EmployeeBuilder':
		required = ["full_name", "cpf", "rg", "birth_date", "address", "phone", "email"]
		for field in required:
			value = kwargs.get(field)
			if value is None or value == "":
				self._errors.append(f"Campo obrigatório: {field}")
			else:
				if field == "birth_date":
					d = _parse_date(value)
					if d is None:
						self._errors.append("Data de nascimento inválida")
					else:
						self._data[field] = d
				else:
					self._data[field] = value
		return self

	def set_work_data(self, **kwargs) -> 'EmployeeBuilder':
		required = ["work_card_number", "work_card_series", "admission_date", "status", "department_id", "position_id", "salary", "pis_pasep"]
		for field in required:
			value = kwargs.get(field)
			if value is None or value == "":
				self._errors.append(f"Campo obrigatório: {field}")
			else:
				if field == "status":
					self._data[field] = EmployeeStatus.ativo if str(value).lower() == "ativo" else EmployeeStatus.inativo
				elif field == "admission_date":
					d = _parse_date(value)
					if d is None:
						self._errors.append("Data de admissão inválida")
					else:
						self._data[field] = d
				elif field in ("department_id", "position_id", "salary"):
					self._data[field] = int(value) if field != "salary" else float(value)
				else:
					self._data[field] = value
		self._data["dismissal_date"] = _parse_date(kwargs.get("dismissal_date"))
		sv = kwargs.get("supervisor_id")
		try:
			self._data["supervisor_id"] = int(sv) if sv not in (None, "") else None
		except (ValueError, TypeError):
			self._data["supervisor_id"] = None
		return self

	def set_bank_data(self, **kwargs) -> 'EmployeeBuilder':
		required = ["bank_name", "bank_agency", "bank_account", "bank_account_type"]
		for field in required:
			value = kwargs.get(field)
			if value is None or value == "":
				self._errors.append(f"Campo obrigatório: {field}")
			else:
				self._data[field] = value
		return self

	def set_photo(self, photo_blob: Optional[str]) -> 'EmployeeBuilder':
		self._data["photo_blob"] = photo_blob
		return self

	def build(self) -> Employee:
		if self._errors:
			raise ValueError(f"Erros de validação: {self._errors}")
		employee = Employee(**self._data)
		self.reset()
		return employee
