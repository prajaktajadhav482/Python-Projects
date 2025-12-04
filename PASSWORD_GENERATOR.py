#!/usr/bin/env python3
"""
Tkinter-based Password Generator GUI
- Choose length (slider)
- Checkboxes for char types
- Avoid ambiguous characters
- Generate, Copy, Save
No external packages required.
"""

import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>/?"
AMBIGUOUS = "Il1O0"

def build_charset(use_lower, use_upper, use_digits, use_symbols, avoid_ambiguous):
    charset = ""
    if use_lower: charset += LOWER
    if use_upper: charset += UPPER
    if use_digits: charset += DIGITS
    if use_symbols: charset += SYMBOLS
    if avoid_ambiguous:
        charset = "".join(ch for ch in charset if ch not in AMBIGUOUS)
    return charset

def generate_password(length, charset):
    if not charset:
        return ""
    return "".join(secrets.choice(charset) for _ in range(length))

def on_generate():
    length = length_var.get()
    charset = build_charset(lower_var.get(), upper_var.get(), digits_var.get(), symbols_var.get(), ambiguous_var.get())
    if not charset:
        messagebox.showwarning("No characters", "Please select at least one character type.")
        return
    pw = generate_password(length, charset)
    result_var.set(pw)
    strength_label.config(text=password_strength(pw))

def on_copy():
    pw = result_var.get()
    if not pw:
        return
    root.clipboard_clear()
    root.clipboard_append(pw)
    messagebox.showinfo("Copied", "Password copied to clipboard.")

def on_save():
    pw = result_var.get()
    if not pw:
        messagebox.showwarning("No password", "Generate a password first.")
        return
    path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(pw + "\n")
        messagebox.showinfo("Saved", f"Password saved to {path}")

def password_strength(pw):
    # Simple entropy-ish heuristic (not precise)
    kinds = 0
    if any(c.islower() for c in pw): kinds += 1
    if any(c.isupper() for c in pw): kinds += 1
    if any(c.isdigit() for c in pw): kinds += 1
    if any(c in SYMBOLS for c in pw): kinds += 1
    score = len(pw) * kinds
    if score < 28: return "Weak"
    if score < 56: return "Moderate"
    return "Strong"

# GUI
root = tk.Tk()
root.title("Password Generator")
root.resizable(False, False)
frame = ttk.Frame(root, padding=12)
frame.grid(row=0, column=0)

length_var = tk.IntVar(value=16)
lower_var = tk.BooleanVar(value=True)
upper_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
ambiguous_var = tk.BooleanVar(value=False)
result_var = tk.StringVar()

ttk.Label(frame, text="Length:").grid(row=0, column=0, sticky="w")
length_scale = ttk.Scale(frame, from_=6, to=64, orient="horizontal", command=lambda v: length_display.config(text=str(int(float(v)))), variable=length_var)
length_scale.set(16)
length_scale.grid(row=0, column=1, padx=6, sticky="we")
length_display = ttk.Label(frame, text=str(length_var.get()), width=3)
length_display.grid(row=0, column=2)

# checkboxes
ttk.Checkbutton(frame, text="Lowercase", variable=lower_var).grid(row=1, column=0, sticky="w")
ttk.Checkbutton(frame, text="Uppercase", variable=upper_var).grid(row=1, column=1, sticky="w")
ttk.Checkbutton(frame, text="Digits", variable=digits_var).grid(row=2, column=0, sticky="w")
ttk.Checkbutton(frame, text="Symbols", variable=symbols_var).grid(row=2, column=1, sticky="w")
ttk.Checkbutton(frame, text="Avoid ambiguous (I, l, 1, O, 0)", variable=ambiguous_var).grid(row=3, column=0, columnspan=3, sticky="w")

ttk.Button(frame, text="Generate", command=on_generate).grid(row=4, column=0, pady=(8,0))
ttk.Button(frame, text="Copy", command=on_copy).grid(row=4, column=1, pady=(8,0))
ttk.Button(frame, text="Save", command=on_save).grid(row=4, column=2, pady=(8,0))

ttk.Entry(frame, textvariable=result_var, width=40).grid(row=5, column=0, columnspan=3, pady=(8,0))
strength_label = ttk.Label(frame, text="", font=("TkDefaultFont", 9, "italic"))
strength_label.grid(row=6, column=0, columnspan=3, sticky="w")

root.mainloop()
