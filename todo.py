import os
import json


DATA_FILE = "todo_list.json"

def load_tasks():
    """Loads tasks from the json file. Returns empty list if no file exists."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'm') as f:
            return json.load(f)
    except:
        
        return []

def save_tasks(tasks):
    """Saves the current task list to the json file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def show_tasks(tasks):
    """Prints out the current tasks nicely."""
    if not tasks:
        print("\n--- Your To-Do List is empty! ---")
        return

    print("\n MY TO-DO LIST")
    for idx, task in enumerate(tasks, start=1):
        # Show a checkmark for completed tasks, blank space for pending
        status = "[✓]" if task['completed'] else "[ ]"
        print(f"{idx}. {status} {task['title']}")
    print("=========")

def main():
    tasks = load_tasks()
    
    while True:
        show_tasks(tasks)
        print("\nOptions:")
        print("1. Add a new task")
        print("2. Mark a task as completed")
        print("3. Delete a task")
        print("4. Exit program")
        
        choice = input("\nWhat would you like to do? (1-4): ").strip()
        
        if choice == '1':
            title = input("Enter the task description: ").strip()
            if title:
                new_task = {
                    "title": title,
                    "completed": False
                }
                tasks.append(new_task)
                save_tasks(tasks)
                print(f"Added: '{title}'")
            else:
                print("Task cannot be empty!")
                
        elif choice == '2':
            if not tasks:
                print("No tasks available to complete.")
                continue
            try:
                task_num = int(input("Enter the number of the task to complete: "))
                if 1 <= task_num <= len(tasks):
                    tasks[task_num - 1]['completed'] = True
                    save_tasks(tasks)
                    print("Task marked as completed!")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == '3':
            if not tasks:
                print("No tasks available to delete.")
                continue
            try:
                task_num = int(input("Enter the number of the task to delete: "))
                if 1 <= task_num <= len(tasks):
                    removed = tasks.pop(task_num - 1)
                    save_tasks(tasks)
                    print(f"Deleted task: '{removed['title']}'")
                else:
                    print("Invalid task number.")
            except ValueError:
                print("Please enter a valid number.")
                
        elif choice == '4':
            print("\nGoodbye! Thanks for staying organized.")
            break
            
        else:
            print("Invalid choice, please pick a number between 1 and 4.")

if __name__ == "__main__":
    main()
