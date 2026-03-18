from app.builders.base_builder import AbstractBuilder
from app.models.loan import Loan
from typing import Optional

class LoanBuilder(AbstractBuilder[Loan]):
	def reset(self):
		self._data = {}
		self._errors = []

	def set_employee(self, employee_id: int) -> 'LoanBuilder':
		self._data["employee_id"] = employee_id
		return self

	def set_amount(self, total_amount: float, installments_count: int, monthly_discount: float) -> 'LoanBuilder':
		self._data["total_amount"] = total_amount
		self._data["installments_count"] = installments_count
		self._data["monthly_discount"] = monthly_discount
		return self

	def set_start_month(self, start_month: str) -> 'LoanBuilder':
		self._data["start_month"] = start_month
		return self

	def set_reason(self, reason: str) -> 'LoanBuilder':
		self._data["reason"] = reason
		return self

	def set_status(self, status: str) -> 'LoanBuilder':
		self._data["status"] = status
		return self

	def build(self) -> Loan:
		if not self._data.get("employee_id") or not self._data.get("total_amount"):
			self._errors.append("employee_id e total_amount são obrigatórios")
		if self._errors:
			raise ValueError(f"Erros de validação: {self._errors}")
		loan = Loan(**self._data)
		self.reset()
		return loan
