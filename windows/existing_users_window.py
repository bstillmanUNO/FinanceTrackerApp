import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime


from windows.finance_tracker_window import FinanceTracker
from data import load_user_data
from windows.center_window import center_window

selectionbar_color = '#eff5f6'

data_file = 'finance_data.json'

class ExistingUsersWindow(tk.Tk):
    def __init__(self, user_data):
        super().__init__()
        self.title("Select User")
        self.geometry("1100x700")
        self.bg_image = tk.PhotoImage(file='images/image2.png')
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        tk.Label(self, text="Select an Existing User", font=("Helvetica", 32), bg=selectionbar_color).pack(pady=10)
        
        center_window(self)

        self.user_vars = {}
        self.checkbuttons = []

        self.btn_login = tk.Button(self, text="Login", command=self.login, font=("Arial", 14))
        self.btn_delete = tk.Button(self, text="Delete", command=self.delete_users, font=("Arial", 14))
        self.btn_cancel = tk.Button(self, text="Cancel", command=self.cancel, font=("Arial", 14))

        for user in user_data.keys():
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=user, variable=var, font=("Arial", 16))
            chk.pack(pady=10)
            self.user_vars[user] = var
            self.checkbuttons.append(chk)

        self.after(100, self.center_checkboxes)

    def center_checkboxes(self):
        for chk in self.checkbuttons:
            chk.pack_forget()
            chk.place(x=(self.winfo_width() - chk.winfo_reqwidth()) / 2, y=chk.winfo_y())

        # Calculate positions for the buttons
        btn_width = 200
        btn_spacing = 20 
        total_width = 3 * btn_width + 2 * btn_spacing
        start_x = ((self.winfo_reqwidth() - total_width) / 2) + 325

        self.btn_login.place(x=start_x, y=650, width=btn_width)
        self.btn_delete.place(x=start_x + btn_width + btn_spacing, y=650, width=btn_width)
        self.btn_cancel.place(x=start_x + 2 * btn_width + 2 * btn_spacing, y=650, width=btn_width)

    def login(self):
        selected_user = next((user for user, var in self.user_vars.items() if var.get() == 1), None)
        if selected_user:
            all_user_data = load_user_data()
            user_data = all_user_data.get(selected_user, {})
            latest_timestamp = max(user_data.keys(), key=lambda d: datetime.datetime.fromisoformat(d))
            latest_data = user_data[latest_timestamp]

            self.destroy()
            FinanceTracker({'name': selected_user, **latest_data}).mainloop()

    def delete_users(self):
        from windows.welcome_window import WelcomeWindow
        user_data = load_user_data()
        users_to_delete = [user for user, var in self.user_vars.items() if var.get() == 1]

        for user in users_to_delete:
            user_data.pop(user, None)

        with open(data_file, 'w') as file:
            json.dump(user_data, file)

        messagebox.showinfo("Users Deleted", "Selected users have been deleted.")
        self.destroy()
        WelcomeWindow().mainloop()

    def cancel(self):
        from windows.welcome_window import WelcomeWindow
        self.destroy()
        WelcomeWindow().mainloop()
