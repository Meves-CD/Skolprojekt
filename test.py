from logic.calculator import calculate_tax

result = calculate_tax(
	income=500000,
	municipal_rate=0.32,
	is_self_employed=False
)

for key, value in result.items():
	print(f"{key}: {value:,.0f} kr")