import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from windows.finance_tracker_window import FinanceTracker
from data import load_user_data
from windows.center_window import center_window
from windows.create_new_user import create_new_user_data
from windows.create_new_user import create_new_user_window

# Define global variables for colors
selectionbar_color = '#eff5f6'
sidebar_color = '#85F28C'
header_color = '#27832D'
visualisation_frame_color = "#ffffff"

class WelcomeWindow(tk.Tk):
    def __init__(self, user_data=None):
        super().__init__()
        self.title("Welcome Back")
        self.geometry("1100x700")
        self.bg_image = tk.PhotoImage(file='images/image1.png')
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        tk.Label(self, text="Welcome Back", font=("Helvetica", 32), bg=selectionbar_color).pack(pady=10)

        tk.Button(self, text="Existing Users", command=self.show_existing_users, font=("Arial", 24, "bold")).pack(pady=24)
        tk.Button(self, text="Create New User", command=lambda: create_new_user_window(self), font=("Arial", 24, "bold")).pack(pady=24)
        
        # Center the window
        center_window(self)

    def show_existing_users(self):
        user_data = load_user_data()
        if user_data:
            self.destroy()
            from windows.existing_users_window import ExistingUsersWindow
            ExistingUsersWindow(user_data).mainloop()
        else:
            messagebox.showinfo("No Users", "No existing users detected.")
            self.create_new_user()

    def create_new_user(self):
        create_new_user_window(self)

if __name__ == "__main__":
    welcome_app = WelcomeWindow()
    welcome_app.mainloop()
