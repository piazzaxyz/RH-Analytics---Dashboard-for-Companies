INSS_TABLE = [
	(1412.00,   0.075),
	(2666.68,   0.09),
	(4000.03,   0.12),
	(7786.02,   0.14),
]
INSS_TETO = 908.85

def calculate_inss(salary: float) -> float:
	"""
	Calcula o desconto de INSS progressivo conforme tabela 2024.
	"""
	base = salary
	total = 0.0
	prev_limit = 0.0
	for limit, rate in INSS_TABLE:
		if base > limit:
			total += (limit - prev_limit) * rate
			prev_limit = limit
		else:
			total += (base - prev_limit) * rate
			break
	return min(total, INSS_TETO)
