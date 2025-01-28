import json
import os

# --- Constants ---
TASKS_FILE = "tasks.json"

# --- Helper Functions ---
def load_tasks():
    """
    Load tasks from a JSON file.
    Returns a list of task dictionaries:
       [ 
         {"task": "<string>", "completed": <bool>}, 
         ...
       ]
    """
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        try:
            tasks = json.load(file)
        except json.JSONDecodeError:
            tasks = []
    return tasks

def save_tasks(tasks):
    """
    Save tasks to a JSON file.
    """
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def list_tasks(tasks):
    """
    Print out the list of tasks with an index.
    Also shows if a task is completed.
    """
    if not tasks:
        print("\nYour to-do list is empty!\n")
        return

    print("\nYour To-Do List:")
    for i, t in enumerate(tasks, start=1):
        status = "✓" if t["completed"] else " "
        print(f"{i}. [{status}] {t['task']}")
    print()  # Newline for spacing

def add_task(tasks):
    """
    Prompt the user to enter a new task and add it to the list.
    """
    new_task = input("Enter a new task: ").strip()
    if new_task:
        tasks.append({"task": new_task, "completed": False})
        save_tasks(tasks)
        print(f"Added task: {new_task}")
    else:
        print("No task entered. Returning to main menu.")

def complete_task(tasks):
    """
    Mark a task as completed by index.
    """
    list_tasks(tasks)
    if not tasks:
        return
    
    try:
        index = int(input("Enter the number of the task to mark as completed: "))
        if 1 <= index <= len(tasks):
            tasks[index - 1]["completed"] = True
            save_tasks(tasks)
            print(f"Marked task #{index} as completed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def remove_task(tasks):
    """
    Remove a task by its index.
    """
    list_tasks(tasks)
    if not tasks:
        return

    try:
        index = int(input("Enter the number of the task to remove: "))
        if 1 <= index <= len(tasks):
            removed = tasks.pop(index - 1)
            save_tasks(tasks)
            print(f"Removed task: {removed['task']}")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

# --- Main Application Loop ---
def main():
    print("Welcome to the To-Do List App!")
    
    while True:
        # Load tasks in each loop iteration to keep data fresh
        tasks = load_tasks()

        print("\nMenu:")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Mark a task as completed")
        print("4. Remove a task")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            remove_task(tasks)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
