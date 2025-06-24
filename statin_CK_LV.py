import tkinter as tk
from tkinter import messagebox

ULN_CK = 200  # Example CK ULN (U/L)
ULN_ALT = 40  # Example ALT/AST ULN (U/L)
BILIRUBIN_THRESHOLD = 2.0  # mg/dL

def evaluate_ck_and_liver():
    try:
        ck_value = float(entry_ck.get())
        transaminase = float(entry_alt.get())
        bilirubin = float(entry_bilirubin.get())
        muscle_symptoms = var_symptoms.get()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
        return

    result = ""

    # CK and myopathy assessment
    if ck_value > 10 * ULN_CK or (muscle_symptoms and ck_value > 10 * ULN_CK):
        result += "CK: Withdraw statin, hydrate, and monitor renal function.\n\n"
    elif 3 * ULN_CK < ck_value <= 10 * ULN_CK:
        result += "CK: Withdraw statin. Consider nonstatin-related causes and modify risk factors.\n\n"
    elif ck_value <= 3 * ULN_CK:
        if muscle_symptoms:
            result += (
                "CK: Withdraw statin. Consider nonstatin-related causes and modify risk factors.\n"
                "- If symptoms resolve and CK returns to normal: reinitiate statin at a reduced dose or switch to an alternative statin.\n"
                "- If CK remains elevated or symptoms persist: consult a specialist or consider muscle biopsy.\n\n"
            )
        else:
            result += (
                "CK: Continue statin. Follow up CK in 2–4 weeks. Consider nonstatin-related causes and modify risk factors.\n\n"
            )

    # Liver function assessment
    if transaminase <= ULN_ALT:
        result += "Liver: Start statin. Follow-up liver function test in 12 weeks.\n"
    elif ULN_ALT < transaminase <= 3 * ULN_ALT:
        if bilirubin <= BILIRUBIN_THRESHOLD:
            result += (
                "Liver: Consider starting statin. Reassess liver function and bilirubin in 2–4 weeks.\n"
            )
        else:
            result += "Liver: Do not start statin. Bilirubin > 2 mg/dL. Consult hepatic experts.\n"
    else:  # transaminase > 3x ULN
        result += "Liver: Do not start statin. Transaminase > 3× ULN. Consult hepatic experts.\n"

    text_result.config(state=tk.NORMAL)
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, result)
    text_result.config(state=tk.DISABLED)

def reset_fields():
    entry_ck.delete(0, tk.END)
    entry_alt.delete(0, tk.END)
    entry_bilirubin.delete(0, tk.END)
    var_symptoms.set(False)
    text_result.config(state=tk.NORMAL)
    text_result.delete(1.0, tk.END)
    text_result.config(state=tk.DISABLED)

# GUI Layout
root = tk.Tk()
root.title("Statin Safety Management Tool (CK + Liver Function)")

tk.Label(root, text="CK value (U/L):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_ck = tk.Entry(root, font=("Arial", 14))
entry_ck.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Transaminase (ALT/AST) (U/L):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_alt = tk.Entry(root, font=("Arial", 14))
entry_alt.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Total Bilirubin (mg/dL):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_bilirubin = tk.Entry(root, font=("Arial", 14))
entry_bilirubin.grid(row=2, column=1, padx=10, pady=5)

var_symptoms = tk.BooleanVar()
tk.Checkbutton(root, text="Muscle symptoms present", variable=var_symptoms, font=("Arial", 12)).grid(row=3, column=0, columnspan=2, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(frame_buttons, text="Evaluate", command=evaluate_ck_and_liver, font=("Arial", 12)).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Reset", command=reset_fields, font=("Arial", 12)).grid(row=0, column=1, padx=10)

text_result = tk.Text(root, height=15, width=80, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 14))
text_result.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
