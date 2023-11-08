import json
from datetime import datetime, timedelta

# Define the JSON file path
file_path = "tasks.json"

# Load tasks from the JSON file
def load_tasks():
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"tasks": []}

# Save tasks to the JSON file
def save_tasks(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# View tasks with sorting and filtering
def view_tasks(tasks, sort_by, filter_by_status):
    # Filter tasks by status
    filtered_tasks = [task for task in tasks if not filter_by_status or task["status"] == filter_by_status]

    # Sort tasks by the specified attribute
    sorted_tasks = sorted(filtered_tasks, key=lambda x: x.get(sort_by, "") or "")

    for task in sorted_tasks:
        print(f"Task {task['id']}: {task['title']} ({task['status']})")
        if task.get("deadline"):
            print(f"   Deadline: {task['deadline']}")
        if task.get("priority"):
            print(f"   Priority: {task['priority']}")
        if task.get("labels"):
            print(f"   Labels: {', '.join(task['labels'])}")
        if task.get("comments"):
            print("   Comments:")
            for i, comment in enumerate(task['comments']):
                print(f"   {i+1}. {comment}")

# Task reminder function
def task_reminder(tasks):
    today = datetime.now()
    for task in tasks:
        if task.get("deadline"):
            deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
            if today >= deadline and task["status"] != "DONE":
                print(f"Reminder: Task {task['id']} '{task['title']}' is overdue!")

# Keyboard shortcuts
def display_keyboard_shortcuts():
    print("\nKeyboard Shortcuts:")
    print("V: View Tasks")
    print("A: Add Task")
    print("U: Update Task")
    print("D: Delete Task")
    print("R: Task Reminders")
    print("K: Keyboard Shortcuts")
    print("X: Exit")

# Main menu
def main():
    tasks_data = load_tasks()
    sort_by = "deadline"  # Default sorting by deadline
    filter_by_status = None

    while True:
        print("\nMain Menu (Press 'K' for Keyboard Shortcuts)")
        choice = input("Select an option (V/A/U/D/R/K/X): ").upper()

        if choice == "V":
            view_tasks(tasks_data["tasks"], sort_by, filter_by_status)

        elif choice == "A":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            deadline = input("Enter task deadline (YYYY-MM-DD) or leave empty: ")
            priority = input("Enter task priority (e.g., high, medium, low) or leave empty: ")
            labels = input("Enter task labels (comma-separated) or leave empty: ")
            status = "TODO"
            labels = [label.strip() for label in labels.split(",")] if labels else []

            new_task = {
                "id": len(tasks_data["tasks"]) + 1,
                "title": title,
                "description": description,
                "status": status,
                "deadline": deadline if deadline else None,
                "priority": priority if priority else None,
                "labels": labels,
                "comments": []
            }
            tasks_data["tasks"].append(new_task)
            save_tasks(tasks_data)
            print("Task added successfully.")

        elif choice == "U":
            task_id = int(input("Enter the task ID to update: "))
            for task in tasks_data["tasks"]:
                if task["id"] == task_id:
                    new_status = input("Enter the new status (e.g., TODO, IN PROGRESS, DONE): ")
                    task["status"] = new_status
                    save_tasks(tasks_data)
                    print("Task updated successfully.")
                    break

        elif choice == "D":
            task_id = int(input("Enter the task ID to delete: "))
            for task in tasks_data["tasks"]:
                if task["id"] == task_id:
                    tasks_data["tasks"].remove(task)
                    save_tasks(tasks_data)
                    print("Task deleted successfully.")
                    break

        elif choice == "R":
            task_reminder(tasks_data["tasks"])

        elif choice == "K":
            display_keyboard_shortcuts()

        elif choice == "X":
            print("Exiting the application.")
            break

if __name__ == "__main__":
    main()
