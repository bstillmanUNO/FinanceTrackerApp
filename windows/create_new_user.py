# windows/create_new_user.py
import tkinter as tk
from tkinter import ttk, messagebox
from data import create_new_user_data
from windows.center_window import center_window
from windows.finance_tracker_window import FinanceTracker

def create_new_user_window(parent):
    parent.withdraw()

    new_user_window = tk.Toplevel(parent)
    new_user_window.title("Create New User")
    new_user_window.geometry("1100x700")
    bg_image = tk.PhotoImage(file='images/image3.png')
    bg_label = tk.Label(new_user_window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    new_user_window.bg_image = bg_image
    center_window(new_user_window)

    label_font = ("Arial", 12)
    entry_font = ("Arial", 12)
    bg_color = '#eff5f6'

    tk.Label(new_user_window, text="Create New User", font=("Helvetica", 32), bg=bg_color).pack(pady=10)

    tk.Label(new_user_window, text="Name:", font=("Arial", 14), bg=bg_color).pack()
    name_entry = tk.Entry(new_user_window, font=("Arial", 14))
    name_entry.pack(pady=15)

    tk.Label(new_user_window, text="Weekly Revenue:", font=("Arial", 14), bg=bg_color).pack()
    weekly_revenue_entry = tk.Entry(new_user_window, font=("Arial", 14))
    weekly_revenue_entry.pack(pady=15)

    tk.Label(new_user_window, text="Weekly Expenses:", font=("Arial", 14), bg=bg_color).pack()
    weekly_expenses_entry = tk.Entry(new_user_window, font=entry_font)
    weekly_expenses_entry.pack(pady=15)

    tk.Label(new_user_window, text="Current Balance:", font=("Arial", 14), bg=bg_color).pack()
    current_balance_entry = tk.Entry(new_user_window, font=("Arial", 14))
    current_balance_entry.pack(pady=15)

    def submit_new_user_data():
        name = name_entry.get()
        weekly_revenue = weekly_revenue_entry.get()
        weekly_expenses = weekly_expenses_entry.get()
        current_balance = current_balance_entry.get()

        # Validation checks
        if not name.isalpha():
            messagebox.showerror("Invalid Input", "Name should contain only alphabetical characters.")
            return
        if not (weekly_revenue.replace('.', '', 1).isdigit() and weekly_revenue.count('.') < 2):
            messagebox.showerror("Invalid Input", "Weekly Revenue should be a number.")
            return
        if not (weekly_expenses.replace('.', '', 1).isdigit() and weekly_expenses.count('.') < 2):
            messagebox.showerror("Invalid Input", "Weekly Expenses should be a number.")
            return
        if not (current_balance.replace('.', '', 1).isdigit() and current_balance.count('.') < 2):
            messagebox.showerror("Invalid Input", "Current Balance should be a number.")
            return

        weekly_revenue = float(weekly_revenue)
        weekly_expenses = float(weekly_expenses)
        current_balance = float(current_balance)

        user_data = create_new_user_data(name, weekly_revenue, weekly_expenses, current_balance)
        new_user_window.destroy()
        parent.destroy()  # Close the welcome window
        FinanceTracker(user_data).mainloop()

    submit_btn = tk.Button(new_user_window, text="Submit", font=("Arial", 14), command=submit_new_user_data)
    submit_btn.pack(pady=10)

    def cancel_and_return():
        new_user_window.destroy()
        parent.deiconify()

    cancel_btn = tk.Button(new_user_window, text="Cancel", font=("Arial", 14), command=cancel_and_return)
    cancel_btn.pack(pady=10)
