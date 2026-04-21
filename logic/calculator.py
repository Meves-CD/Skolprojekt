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

def calculate_municipal_tax(taxable_income: float, municipal_rate: float) -> float:
	"""Calculate kommunalskatt on taxable income."""
	if taxable_income <= 0:
		return 0.0
	return taxable_income * municipal_rate

def calculate_state_tax(taxable_income: float) -> float:
	"""Calculate statlig inkomstskatt (20%) on income above threshold."""
	if taxable_income <= STATE_TAX_THRESHOLD:
		return 0.0
	return (taxable_income - STATE_TAX_THRESHOLD) * STATE_TAX_RATE

def calculate_self_employed_fee(income: float) -> float:
	"""Calculate egenavgifter for self-employed individuals."""
	return income * SELF_EMPLOYED_FEE_RATE

def calculate_tax(income: float, municipal_rate: float, is_self_employed: bool) -> dict:
	"""
	Main calculator function. Returns a breakdown of all tax components.

	Args:
		income: Gross yearly income in SEK
		municipal_rate: Local tax rate as a decimal (e.g. 0.32)
		is_self_employed: True if person runs their own business

	Returns:
		Dictionary with tax breakdown and net income
	"""
	result = {
		"gross_income": income,
		"self_employed_fee": 0.0,
		"taxable_income": 0.0,
		"grundavdrag": 0.0,
		"municipal_tax": 0.0,
		"state_tax": 0.0,
		"total_tax": 0.0,
		"net_income": 0.0,
	}

	if is_self_employed:
		fee = calculate_self_employed_fee(income)
		result["self_employed_fee"] = fee
		adjusted_income = income - fee * 0.5 # Schablonavdag: half the fee is deductible
	else:
		adjusted_income = income

	grundavdrag = calculate_grundavdrag(adjusted_income)
	taxable_income = max(0.0, adjusted_income - grundavdrag)

	municipal_tax = calculate_municipal_tax(taxable_income, municipal_rate)
	state_tax = calculate_state_tax(taxable_income)

	result["grundavdrag"] = grundavdrag
	result["taxable_income"] = taxable_income
	result["municipal_tax"] = municipal_tax
	result["state_tax"] = state_tax
	result["total_tax"] = municipal_tax + state_tax + result["self_employed_fee"]
	result["net_income"] = income - result["total_tax"]

	return result