
# gui/app.py

import tkinter as tk
from tkinter import messagebox
from logic.calculator import calculate_tax


def format_sek(amount: float) -> str:
    """Format a number as Swedish kronor."""
    return f"{amount:,.0f} kr".replace(",", " ")


def run_app():
    root = tk.Tk()
    root.title("Skatteberäknare")
    root.resizable(False, False)

    # --- Input frame ---
    input_frame = tk.LabelFrame(root, text="Uppgifter", padx=10, pady=10)
    input_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")

    tk.Label(input_frame, text="Årsinkomst (kr):").grid(row=0, column=0, sticky="w")
    income_entry = tk.Entry(input_frame, width=20)
    income_entry.grid(row=0, column=1, padx=10, pady=4)

    tk.Label(input_frame, text="Kommunalskatt (%):").grid(row=1, column=0, sticky="w")
    municipal_entry = tk.Entry(input_frame, width=20)
    municipal_entry.insert(0, "32")  # Default value
    municipal_entry.grid(row=1, column=1, padx=10, pady=4)

    tk.Label(input_frame, text="Anställningsform:").grid(row=2, column=0, sticky="w")
    employment_var = tk.BooleanVar(value=False)
    tk.Radiobutton(input_frame, text="Anställd", variable=employment_var, value=False).grid(row=2, column=1, sticky="w")
    tk.Radiobutton(input_frame, text="Egenföretagare", variable=employment_var, value=True).grid(row=3, column=1, sticky="w")

    # --- Result frame ---
    result_frame = tk.LabelFrame(root, text="Resultat", padx=10, pady=10)
    result_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

    labels = {
        "grundavdrag": "Grundavdrag:",
        "self_employed_fee": "Egenavgifter:",
        "municipal_tax": "Kommunalskatt:",
        "state_tax": "Statlig skatt:",
        "total_tax": "Total skatt:",
        "net_income": "Nettoinkomst:",
    }

    result_vars = {}
    for i, (key, label_text) in enumerate(labels.items()):
        tk.Label(result_frame, text=label_text).grid(row=i, column=0, sticky="w")
        var = tk.StringVar(value="-")
        tk.Label(result_frame, textvariable=var, width=18, anchor="e").grid(row=i, column=1, padx=10)
        result_vars[key] = var

    # --- Buttons ---
    def on_calculate():
        try:
            income = float(income_entry.get().replace(" ", "").replace(",", "."))
            municipal_rate = float(municipal_entry.get().replace(",", ".")) / 100

            if income < 0 or municipal_rate < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror("Fel", "Ange giltiga värden för inkomst och kommunalskatt.")
            return

        result = calculate_tax(income, municipal_rate, employment_var.get())

        for key, var in result_vars.items():
            var.set(format_sek(result[key]))

    def on_reset():
        income_entry.delete(0, tk.END)
        municipal_entry.delete(0, tk.END)
        municipal_entry.insert(0, "32")
        employment_var.set(False)
        for var in result_vars.values():
            var.set("-")

    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, pady=10)

    tk.Button(button_frame, text="Beräkna", width=12, command=on_calculate).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Rensa", width=12, command=on_reset).grid(row=0, column=1, padx=5)

    root.mainloop()