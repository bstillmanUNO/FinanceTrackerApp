from windows.finance_tracker_window import FinanceTracker
from windows.welcome_window import WelcomeWindow
from windows.existing_users_window import ExistingUsersWindow
from data import load_user_data, save_data
from windows.center_window import center_window

if __name__ == "__main__":
    user_data = load_user_data()
    app = WelcomeWindow(user_data)
    app.mainloop()
