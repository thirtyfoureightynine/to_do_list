import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# --- Constants ---
TASKS_FILE = "tasks.json"
console = Console()

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
    Display tasks in a beautiful table using Rich.
    """
    if not tasks:
        console.print(Panel("✨ Your to-do list is empty! ✨", 
                          style="cyan", 
                          title="Tasks"))
        return

    table = Table(title="📋 Your To-Do List", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=4)
    table.add_column("Task", min_width=20)
    table.add_column("Status", justify="center", width=10)

    for i, t in enumerate(tasks, start=1):
        status = "✅" if t["completed"] else "⏳"
        style = "dim" if t["completed"] else "none"
        table.add_row(
            str(i),
            t["task"],
            status,
            style=style
        )

    console.print(table)

def add_task(tasks):
    """
    Prompt the user to enter a new task and add it to the list.
    """
    new_task = Prompt.ask("✏️  Enter a new task").strip()
    if new_task:
        tasks.append({"task": new_task, "completed": False})
        save_tasks(tasks)
        console.print(f"✨ Added task: [green]{new_task}[/green]")
    else:
        console.print("[yellow]No task entered. Returning to main menu.[/yellow]")

def complete_task(tasks):
    """
    Mark a task as completed by index.
    """
    list_tasks(tasks)
    if not tasks:
        return
    
    try:
        index = int(Prompt.ask("📌 Enter the number of the task to mark as completed"))
        if 1 <= index <= len(tasks):
            tasks[index - 1]["completed"] = True
            save_tasks(tasks)
            console.print(f"✅ Marked task #{index} as completed!")
        else:
            console.print("[red]Invalid task number.[/red]")
    except ValueError:
        console.print("[red]Please enter a valid number.[/red]")

def remove_task(tasks):
    """
    Remove a task by its index.
    """
    list_tasks(tasks)
    if not tasks:
        return

    try:
        index = int(Prompt.ask("🗑️  Enter the number of the task to remove"))
        if 1 <= index <= len(tasks):
            removed = tasks.pop(index - 1)
            save_tasks(tasks)
            console.print(f"🗑️  Removed task: [red]{removed['task']}[/red]")
        else:
            console.print("[red]Invalid task number.[/red]")
    except ValueError:
        console.print("[red]Please enter a valid number.[/red]")

def display_menu():
    """
    Display the main menu using Rich styling.
    """
    console.print("\n[bold cyan]Menu[/bold cyan]")
    console.print("1. [blue]View tasks[/blue] 📋")
    console.print("2. [blue]Add a task[/blue] ✏️")
    console.print("3. [blue]Mark a task as completed[/blue] ✅")
    console.print("4. [blue]Remove a task[/blue] 🗑️")
    console.print("5. [blue]Exit[/blue] 👋")
    console.print()

# --- Main Application Loop ---
def main():
    console.print("\n✨ [bold yellow]Welcome to the To-Do List App![/bold yellow] ✨\n")
    
    while True:
        # Load tasks in each loop iteration to keep data fresh
        tasks = load_tasks()
        
        display_menu()
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5"])
        
        if choice == "1":
            list_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            remove_task(tasks)
        elif choice == "5":
            console.print("\n[bold cyan]👋 Goodbye! Have a great day![/bold cyan]\n")
            break

if __name__ == "__main__":
    main()