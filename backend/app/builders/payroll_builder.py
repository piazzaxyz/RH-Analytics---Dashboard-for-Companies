from app.builders.base_builder import AbstractBuilder
from app.models.payroll import Payroll
from typing import Optional

class PayrollBuilder(AbstractBuilder[Payroll]):
	def reset(self):
		self._data = {}
		self._errors = []

	def set_employee(self, employee_id: int) -> 'PayrollBuilder':
		self._data["employee_id"] = employee_id
		return self

	def set_reference_month(self, month: str) -> 'PayrollBuilder':
		self._data["reference_month"] = month
		return self

	def set_values(self, **kwargs) -> 'PayrollBuilder':
		for field in [
			"base_salary", "overtime_50_value", "overtime_100_value", "night_additional_value",
			"dsr_value", "bonus_value", "hazard_pay", "unhealthy_pay", "gross_salary",
			"inss_value", "irrf_value", "vt_discount", "vr_discount", "health_plan_discount",
			"loan_discount", "absence_discount", "alimony_discount", "other_discounts", "net_salary"
		]:
			self._data[field] = kwargs.get(field, 0)
		return self

	def set_status(self, status: str) -> 'PayrollBuilder':
		self._data["status"] = status
		return self

	def set_processed_at(self, processed_at: Optional[str]) -> 'PayrollBuilder':
		self._data["processed_at"] = processed_at
		return self

	def build(self) -> Payroll:
		if not self._data.get("employee_id") or not self._data.get("reference_month"):
			self._errors.append("employee_id e reference_month são obrigatórios")
		if self._errors:
			raise ValueError(f"Erros de validação: {self._errors}")
		payroll = Payroll(**self._data)
		self.reset()
		return payroll
