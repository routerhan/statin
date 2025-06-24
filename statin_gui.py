import tkinter as tk
from tkinter import messagebox

ULN = 200  # Example upper limit of normal CK (U/L)

def manage_statin():
    try:
        ck_value = float(entry_ck.get())
        muscle_symptoms = var_symptoms.get()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid CK value (U/L).")
        return

    result = ""

    if ck_value > 10 * ULN or (muscle_symptoms and ck_value > 10 * ULN):
        result = "Withdraw statin. Provide hydration and monitor renal function."
    elif 3 * ULN < ck_value <= 10 * ULN:
        result = "Withdraw statin. Consider nonstatin-related causes and modify risk factors."
    elif ck_value <= 3 * ULN:
        if muscle_symptoms:
            result = (
                "Withdraw statin. Consider nonstatin-related causes and modify risk factors.\n"
                "- If symptoms resolve and CK returns to normal: reinitiate statin at a reduced dose or switch to an alternative statin.\n"
                "- If CK remains elevated (>3x ULN) or symptoms persist: consult a specialist or consider muscle biopsy."
            )
        else:
            result = (
                "Continue statin therapy. Recheck CK in 2 to 4 weeks.\n"
                "Consider nonstatin-related causes and modify risk factors."
            )

    text_result.config(state=tk.NORMAL)
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, result)
    text_result.config(state=tk.DISABLED)

def reset_fields():
    entry_ck.delete(0, tk.END)
    var_symptoms.set(False)
    text_result.config(state=tk.NORMAL)
    text_result.delete(1.0, tk.END)
    text_result.config(state=tk.DISABLED)

# GUI Layout
root = tk.Tk()
root.title("Statin Myopathy Management Tool")

tk.Label(root, text="Enter CK value (U/L):").grid(row=0, column=0, padx=10, pady=5)
entry_ck = tk.Entry(root, font=("Arial", 14))
entry_ck.grid(row=0, column=1, padx=10, pady=5)

var_symptoms = tk.BooleanVar()
tk.Checkbutton(root, text="Muscle symptoms present", variable=var_symptoms, font=("Arial", 12)).grid(row=1, column=0, columnspan=2, pady=5)

frame_buttons = tk.Frame(root)
frame_buttons.grid(row=2, column=0, columnspan=2, pady=10)

tk.Button(frame_buttons, text="Evaluate", command=manage_statin, font=("Arial", 12)).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="Reset", command=reset_fields, font=("Arial", 12)).grid(row=0, column=1, padx=10)

text_result = tk.Text(root, height=12, width=70, wrap=tk.WORD, state=tk.DISABLED, font=("Times New Roman", 20))
text_result.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
