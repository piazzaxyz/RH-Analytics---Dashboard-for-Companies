IRRF_TABLE = [
	(2259.20,   0.0,    0.0),
	(2826.65,   0.075,  169.44),
	(3751.05,   0.15,   381.44),
	(4664.68,   0.225,  662.77),
	(float('inf'), 0.275, 896.00),
]
IRRF_DEDUCAO_DEPENDENTE = 189.59

def calculate_irrf(base: float, dependents: int = 0) -> float:
	"""
	Calcula o desconto de IRRF progressivo conforme tabela 2024.
	base = salário bruto - INSS - dedução dependentes
	"""
	base -= IRRF_DEDUCAO_DEPENDENTE * dependents
	for limit, rate, deduction in IRRF_TABLE:
		if base <= limit:
			return max((base * rate) - deduction, 0)
	return 0.0
