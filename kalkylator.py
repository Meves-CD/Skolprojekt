# logic/calculator.py

# Swedish tax constants (2024)

STATE_TAX_RATE = 0.20
STATE_TAX_THRESHOLD = 613900
SELF_EMPLOYED_FEE_RATE = 0.2897 # Egenavgifter

def calculate_grundavdrag(income: float) -> float:
	"""
	Calculate grundavdrag (basic deduction) based on income.
	Simplified version of Skatteveket's sliding scale.
	"""
	if income <= 14000:
		return income
	elif income <= 91000:
		return 14000 + (income - 14000) * 0.31
	elif income <= 12300:
		return 37870
	elif income <= 370000:
		return 37870 - (income - 12300) * 0.1
	elif income <= 507900:
		return 13170
	else:
		return 13900