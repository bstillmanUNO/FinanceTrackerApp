import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from .center_window import center_window
from data import load_user_data, save_data

selectionbar_color = '#eff5f6'
sidebar_color = '#85F28C'
header_color = '#27832D'

class FinanceTracker(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.title("Finance Tracker")
        self.geometry("1100x700")
        self.resizable(0, 0)
        self.config(background='#C7FFCB')
        center_window(self)
        
        # Header
        self.header = tk.Frame(self, bg=header_color)
        self.header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.1)

        # Sidebar
        self.sidebar = tk.Frame(self, bg=sidebar_color)
        self.sidebar.place(relx=0, rely=0, relwidth=0.3, relheight=1)

        # Sidebar Tabs
        self.tabs = ['Summary', 'Income', 'Balance', 'Expenses', 'Update Finances']
        for idx, tab in enumerate(self.tabs):
            btn = tk.Button(self.sidebar, text=tab, command=lambda tab=tab: self.show_frame(tab))
            btn.place(relx=0, rely=idx * 0.1, relwidth=1, relheight=0.1)
        
        # Time Period Dropdown
        tk.Label(self.sidebar, text="Time Period", font=("Arial", 12), bg=sidebar_color).place(relx=0, rely=0.6, relwidth=1, relheight=0.05)
        self.time_period_var = tk.StringVar()
        time_periods = ['Current', '1 week', '1 month', '3 months', '6 months', '1 year']
        self.time_period_dropdown = ttk.Combobox(self.sidebar, textvariable=self.time_period_var, values=time_periods, state="readonly")
        self.time_period_dropdown.set('Current')  # Set default value as 'Current'
        self.time_period_dropdown.place(relx=0, rely=0.65, relwidth=1, relheight=0.05)
        self.time_period_dropdown.bind("<<ComboboxSelected>>", self.on_time_period_change)

        log_out_btn = tk.Button(self.sidebar, text="Log Out", command=self.confirm_logout, font=("Arial", 12, "bold"))
        log_out_btn.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
        
        self.show_frame("Summary")

    def show_frame(self, tab):
        # Clear the current header
        for widget in self.header.winfo_children():
            widget.destroy()
        for widget in self.winfo_children():
            if widget not in [self.header, self.sidebar]:
                widget.destroy()

        # Update the header
        tk.Label(self.header, text=tab, font=("Arial", 16), fg="white", bg=header_color).pack(fill=tk.BOTH, expand=True)

        if tab == "Summary":
            if self.time_period_var.get() == 'Current':
                self.display_summary()
            else:
                self.on_time_period_change()
        elif tab == "Income":
            self.display_income()
        elif tab == "Balance":
            self.display_balance()
        elif tab == "Expenses":
            self.display_expenses()
        elif tab == "Update Finances":
            self.update_finances()
    
    def get_latest_user_data(self, user_name):
        all_user_data = load_user_data()
        user_data = all_user_data.get(user_name, {})
        if not user_data:
            return {}

        latest_timestamp = max(user_data.keys(), key=lambda d: datetime.datetime.fromisoformat(d))
        return user_data[latest_timestamp]
    
    def calculate_financial_changes(self, time_period):
        user_name = self.user_data['name']
        all_user_data = load_user_data()
        user_data = all_user_data.get(user_name, {})

        end_time = datetime.datetime.now()
        start_time = self.get_start_time(time_period, end_time)

        relevant_data = {datetime.datetime.fromisoformat(k): v for k, v in user_data.items() if start_time <= datetime.datetime.fromisoformat(k) <= end_time}

        if not relevant_data:
            return {}

        if len(relevant_data) == 1:
            return {
                'weekly_revenue': (0, 0),
                'current_balance': (0, 0),
                'weekly_expenses': (0, 0)
            }

        earliest_data = relevant_data[min(relevant_data.keys())]
        latest_data = relevant_data[max(relevant_data.keys())]

        changes = {
            'weekly_revenue': self.calculate_change_average(relevant_data, 'weekly_revenue'),
            'current_balance': self.calculate_change_simple(earliest_data, latest_data, 'current_balance'),
            'weekly_expenses': self.calculate_change_average(relevant_data, 'weekly_expenses')
        }

        return changes


    @staticmethod
    def calculate_change_simple(earliest_data, latest_data, key):
        initial = earliest_data.get(key)
        final = latest_data.get(key)
        if initial is None or final is None:
            return None
        change = final - initial
        percent_change = (change / initial * 100) if initial != 0 else float('inf')
        return change, percent_change

    def calculate_change_average(self, relevant_data, key):
        sorted_keys = sorted(relevant_data.keys())
        final = relevant_data[sorted_keys[-1]].get(key)
        old_data = sorted_keys[:-1]

        total = sum(relevant_data[date][key] for date in old_data if key in relevant_data[date])
        average = total / len(old_data) if old_data else 0

        if average == 0 or final is None:
            return None
        change = final - average
        percent_change = (change / average * 100)
        return change, percent_change
    
    def get_start_time(self, time_period, end_time):
        if time_period == '1 week':
            return end_time - datetime.timedelta(weeks=1)
        elif time_period == '1 month':
            return end_time - datetime.timedelta(weeks=4)
        elif time_period == '3 months':
            return end_time - datetime.timedelta(weeks=12)
        elif time_period == '6 months':
            return end_time - datetime.timedelta(weeks=24)
        elif time_period == '1 year':
            return end_time - datetime.timedelta(weeks=52)
            
    def display_summary(self):
        user_name = self.user_data['name']
        all_user_data = load_user_data()
        user_data = all_user_data.get(user_name, {})
        latest_timestamp = max(user_data.keys(), key=lambda d: datetime.datetime.fromisoformat(d))
        latest_data = user_data[latest_timestamp]

        for widget in self.winfo_children():
            if widget not in [self.header, self.sidebar]:
                widget.destroy()

        summary_frame = tk.Frame(self, bg="#C7FFCB")
        summary_frame.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        for category in ['weekly_revenue', 'current_balance', 'weekly_expenses']:
            if category in latest_data:
                value = latest_data[category]
                formatted_category = " ".join(word.capitalize() for word in category.split('_'))
                tk.Label(summary_frame, text=f"{formatted_category}: {value}", font=("Arial", 14), bg=selectionbar_color).pack(pady=5)
            else:
                formatted_category = " ".join(word.capitalize() for word in category.split('_'))
                tk.Label(summary_frame, text=f"{formatted_category} Data Not Available", font=("Arial", 14), bg=selectionbar_color).pack(pady=5)


    def display_income(self):
        if self.time_period_var.get() == 'Current':
            income = self.user_data.get('weekly_revenue', 'N/A')
            self.display_info("Income", f"Weekly Revenue: {income}")
        else:
            financial_changes = self.calculate_financial_changes(self.time_period_var.get())
            change_data = financial_changes.get('weekly_revenue')
            if change_data:
                change, percent_change = change_data
                sign = '+' if change >= 0 else ''
                income_text = f"Revenue Over the Past {self.time_period_var.get().capitalize()}:\n" \
                            f"{sign}{change} / {sign}{(percent_change):.2f}%"
            else:
                income_text = "Data Not Available"
            self.display_info("Income", income_text)

    def display_balance(self):
        if self.time_period_var.get() == 'Current':
            balance = self.user_data.get('current_balance', 'N/A')
            self.display_info("Balance", f"Current Balance: {balance}")
        else:
            financial_changes = self.calculate_financial_changes(self.time_period_var.get())
            change_data = financial_changes.get('current_balance')
            if change_data:
                change, percent_change = change_data
                sign = '+' if change >= 0 else ''
                balance_text = f"Balance Over the Past {self.time_period_var.get().capitalize()}:\n" \
                            f"{sign}{change} / {sign}{(percent_change):.2f}%"
            else:
                balance_text = "Data Not Available"
            self.display_info("Balance", balance_text)

    def display_expenses(self):
        if self.time_period_var.get() == 'Current':
            expenses = self.user_data.get('weekly_expenses', 'N/A')
            self.display_info("Expenses", f"Weekly Expenses: {expenses}")
        else:
            financial_changes = self.calculate_financial_changes(self.time_period_var.get())
            change_data = financial_changes.get('weekly_expenses')
            if change_data:
                change, percent_change = change_data
                sign = '+' if change >= 0 else ''
                expenses_text = f"Expenses Over the Past {self.time_period_var.get().capitalize()}:\n" \
                                f"{sign}{change} / {sign}{(percent_change):.2f}%"
            else:
                expenses_text = "Data Not Available"
            self.display_info("Expenses", expenses_text)

    def display_info(self, title, value):
        info_frame = tk.Frame(self, bg="#C7FFCB")
        info_frame.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)
        tk.Label(info_frame, text=value, font=("Arial", 14), bg=selectionbar_color).pack()
    
    def update_finances(self):
        for widget in self.winfo_children():
            if widget not in [self.header, self.sidebar]:
                widget.destroy()

        main_frame = tk.Frame(self, bg="#C7FFCB")
        main_frame.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        tk.Label(main_frame, text="What finances do you want to change?", font=("Arial", 14, "bold"), bg=selectionbar_color).pack(pady=10)

        self.finance_options = {'Income': tk.IntVar(), 'Balance': tk.IntVar(), 'Expenses': tk.IntVar()}
        for idx, (text, var) in enumerate(self.finance_options.items()):
            tk.Checkbutton(main_frame, text=text, variable=var, font=("Arial", 12)).pack(anchor=tk.W, padx=20, pady=5)

        next_btn = tk.Button(main_frame, text="Next", command=self.next_update_finances, font=("Arial", 12))
        next_btn.pack(pady=20)
    
    def next_update_finances(self):
        if not any(var.get() for var in self.finance_options.values()):
            messagebox.showwarning("No Selection", "Please select at least one option to continue.")
            return
        for widget in self.winfo_children():
            if widget not in [self.header, self.sidebar]:
                widget.destroy()

        update_frame = tk.Frame(self, bg=selectionbar_color)
        update_frame.place(relx=0.3, rely=0.1, relwidth=0.7, relheight=0.9)

        self.finance_entries = {}
        finance_mapping = {
            'Income': 'weekly_revenue',
            'Balance': 'current_balance',
            'Expenses': 'weekly_expenses'
        }
        
        for option, var in self.finance_options.items():
            if var.get():
                label_text = f"New {option}"
                tk.Label(update_frame, text=label_text, font=("Arial", 12), bg=selectionbar_color).pack(pady=5)
                entry = ttk.Entry(update_frame, font=("Arial", 12))
                entry.pack(pady=5)
                self.finance_entries[finance_mapping[option]] = entry

        submit_btn = tk.Button(update_frame, text="Submit", command=self.submit_finances, font=("Arial", 12))
        submit_btn.pack(pady=20)
        cancel_btn = tk.Button(update_frame, text="Cancel", command=lambda: self.show_frame("Summary"), font=("Arial", 12))
        cancel_btn.pack(pady=20)

    def cancel_update_finances(self):
        self.show_frame("Summary")
            
    def submit_finances(self):
        user_name = self.user_data['name']
        timestamp = datetime.datetime.now().isoformat()
        new_record = {}

        for key, entry_widget in self.finance_entries.items():
            new_value = entry_widget.get()

            # Validation check for numeric input
            if not (new_value.replace('.', '', 1).isdigit() and new_value.count('.') < 2):
                messagebox.showerror("Invalid Input", f"{key.replace('_', ' ').title()} should be a number.")
                return

            new_record[key] = float(new_value)

        # Load existing data and add the new record
        all_user_data = load_user_data()
        if user_name not in all_user_data:
            all_user_data[user_name] = {}

        all_user_data[user_name][timestamp] = new_record
        save_data(all_user_data)
        messagebox.showinfo("Update Successful", "Your financial data has been updated.")

    def on_time_period_change(self, event=None):
        selected_time_period = self.time_period_var.get()
        current_tab = self.header.winfo_children()[0].cget("text")
        
        if selected_time_period == 'Current':
            if current_tab == "Income":
                self.display_income()
            elif current_tab == "Balance":
                self.display_balance()
            elif current_tab == "Expenses":
                self.display_expenses()
            else:
                self.display_summary()
        else:
            if current_tab == "Income":
                self.display_income()
            elif current_tab == "Balance":
                self.display_balance()
            elif current_tab == "Expenses":
                self.display_expenses()
            else:
                self.display_summary()

    
    def confirm_logout(self):
        logout_popup = tk.Toplevel(self)
        logout_popup.title("Log Out")
        logout_popup.geometry("300x150")
        logout_popup.config(background="white")

        tk.Label(logout_popup, text="Are you sure you want to log out?", font=("Arial", 12), bg="white").pack(pady=10)

        tk.Button(logout_popup, text="Yes", command=self.logout, font=("Arial", 12)).pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Button(logout_popup, text="No", command=logout_popup.destroy, font=("Arial", 12)).pack(side=tk.RIGHT, padx=10, pady=10)
        
        center_window(logout_popup, 300, 150)


    def logout(self):
        from windows.welcome_window import WelcomeWindow
        self.destroy()
        WelcomeWindow().mainloop()