import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime
import os

FILENAME = "expenses.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(FILENAME):
    with open(FILENAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])

# Functions
def add_expense():
    date = date_entry.get()
    if date.strip() == "":
        date = datetime.today().strftime("%Y-%m-%d")
    category = category_entry.get()
    amount = amount_entry.get()
    description = desc_entry.get()

    if category == "" or amount == "":
        messagebox.showerror("Error", "Category and Amount are required!")
        return

    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    messagebox.showinfo("Success", "Expense added!")
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    desc_entry.delete(0, tk.END)
    load_expenses()

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            tree.insert("", tk.END, values=row)

def total_expense():
    total = 0
    with open(FILENAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            total += float(row[2])
    messagebox.showinfo("Total Expense", f"Total Expenses: {total}")

# GUI
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")

# Input Frame
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Category").grid(row=0, column=2, padx=5, pady=5)
category_entry = tk.Entry(frame)
category_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame, text="Amount").grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(frame)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Description").grid(row=1, column=2, padx=5, pady=5)
desc_entry = tk.Entry(frame)
desc_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Button(frame, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10)
tk.Button(frame, text="Total Expense", command=total_expense, bg="#2196F3", fg="white").grid(row=2, column=2, pady=10)

# Treeview for displaying expenses
columns = ("Date", "Category", "Amount", "Description")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(pady=20)

load_expenses()
root.mainloop()
