import json
import os
import datetime

# File to store the data
data_file = 'finance_data.json'

def load_user_data():
    """Loads user data from a JSON file."""
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return {}

def save_data(data):
    """Saves data to a JSON file."""
    with open(data_file, 'w') as file:
        json.dump(data, file)

def create_new_user_data(name, weekly_revenue, weekly_expenses, current_balance):
    timestamp = datetime.datetime.now().isoformat()

    new_user_data = {
        timestamp: {
            'weekly_revenue': weekly_revenue,
            'weekly_expenses': weekly_expenses,
            'current_balance': current_balance
        }
    }

    all_user_data = load_user_data()

    if name in all_user_data:
        all_user_data[name].update(new_user_data)
    else:
        all_user_data[name] = new_user_data

    save_data(all_user_data)

    return {'name': name, **new_user_data[timestamp]}
