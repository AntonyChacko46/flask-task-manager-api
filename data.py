import requests

# Base URL of your Flask API
BASE_URL = "http://127.0.0.1:5000"

# Insert User
def create_user(user_id, uname, uemail):
    user_data = {
        "user_id": user_id,
        "uname": uname,
        "uemail": uemail
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print("Create User:", response.status_code, response.json())

# Insert Task
def create_task(task_id, title, description, due_date, priority):
    task_data = {
        "task_id": task_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority
    }
    response = requests.post(f"{BASE_URL}/tasks/", json=task_data)
    print("Create Task:", response.status_code, response.json())

# Sample Data
if __name__ == "__main__":
    create_user(1001, "Alice Smith", "alice@example.com")
    create_user(1002, "Bob Brown", "bob@example.com")

    create_task(2001, "Design Logo", "Create a new logo", "2025-07-01", "HIGH")
    create_task(2002, "Write Docs", "Write API documentation", "2025-07-05", "MEDIUM")
