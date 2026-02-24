import tkinter as tk
from tkinter import messagebox
import json
import os

def addTaskChecker(task):
    """Checks if the task input is valid (not empty or just whitespace)"""
    with open("data_files/personal_hub_data.json", "a") as f:
        if task.strip():
            f.write(task + "\n")
            return True
        else:
            return False

def removeTaskChecker(task):
    """Checks if the task input is valid for removal (exists in file)"""
    with open("data_files/personal_hub_data.json", "r") as f:
        tasks = f.read().splitlines()
    if task in tasks:
        tasks.remove(task)
        with open("data_files/personal_hub_data.json", "w") as f:
            f.write("\n".join(tasks) + "\n")
        return True
    else:
        return False

def doesTaskExist(task):
    """Helper function to check if a task exists in the file"""
    with open("data_files/personal_hub_data.json", "r") as f:
        tasks = f.read().splitlines()
    return task in tasks
class PersonalHubApp:

    # Constructor for PersonalHubApp Class
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Hub")
        self.root.geometry("600x650")
        self.root.config(bg="#f0f0f0")
        
        # File path for storing data persistently
        self.data_file = "data_files\\personal_hub_data.json"
        
        # Load tasks and goals from file, or create empty lists if file doesn't exist
        self.tasks = []
        self.goals = []
        self.load_data()
        
        self.show_main_hub()
    
    def load_data(self):
        """Load tasks and goals from JSON file if it exists.
        This runs when the app starts to restore previous session data.
        If file doesn't exist or is corrupted, starts with empty lists."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    self.tasks = data.get('tasks', [])
                    self.goals = data.get('goals', [])
        except (json.JSONDecodeError, IOError) as e:
            # If file is corrupted or unreadable, start fresh
            print(f"Error loading data: {e}")
            self.tasks = []
            self.goals = []
    
    def save_data(self):
        """Save current tasks and goals to JSON file.
        Called after every add/remove operation to ensure data persistence.
        Uses JSON format for human-readable storage that's easy to debug."""
        try:
            data = {
                'tasks': self.tasks,
                'goals': self.goals
            }
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")
            messagebox.showerror("Save Error", "Could not save data to file")
    
    def clear_window(self):
        """Remove all widgets from window to prepare for new screen.
        This is necessary when navigating between different views (hub vs workspace)
        because tkinter doesn't have built-in screen management."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_task_agenda(self, container):
        # Background for Task agenda
        task_frame = tk.Frame(container, bg="#f0f0f0", relief=tk.RIDGE, bd=2)
        task_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Title for Task agenda
        task_title = tk.Label(task_frame, text="📋 Task Agenda", font=("Arial", 16, "bold"), bg="#f0f0f0")
        task_title.pack(pady=10)
        
        # Input line for Task agenda
        task_input_frame = tk.Frame(task_frame, bg="#f0f0f0")
        task_input_frame.pack(pady=5)
        
        # Size of task agenda tab
        self.task_entry = tk.Entry(task_input_frame, width=25, font=("Arial", 10))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        # Add task button for Task agenda
        add_task_btn = tk.Button(task_input_frame, text="Add", command=self.add_task, 
                                bg="#4CAF50", fg="white", font=("Arial", 9))
        add_task_btn.pack(side=tk.LEFT)
        
        # Output for tasks for Task agenda
        self.task_listbox = tk.Listbox(task_frame, font=("Arial", 10), height=15, bg="white")
        self.task_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Remove task Button for Task agenda
        remove_task_btn = tk.Button(task_frame, text="Remove Task", command=self.remove_task,
                                    bg="#f44336", fg="white", font=("Arial", 9))
        remove_task_btn.pack(pady=5)

    def create_goals_list(self, container):
        # Background for goals list
        goals_frame = tk.Frame(container, bg="#f0f0f0", relief=tk.RIDGE, bd=2)
        goals_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Title for Goals list
        goals_title = tk.Label(goals_frame, text="🎯 Goals List", font=("Arial", 16, "bold"), bg="#f0f0f0")
        goals_title.pack(pady=10)
        
        # Input line for Goals list
        goals_input_frame = tk.Frame(goals_frame, bg="#f0f0f0")
        goals_input_frame.pack(pady=5)
        
        # Size of goals list tab
        self.goals_entry = tk.Entry(goals_input_frame, width=25, font=("Arial", 10))
        self.goals_entry.pack(side=tk.LEFT, padx=5)
        
        # Add goal button for Goals list
        add_goal_btn = tk.Button(goals_input_frame, text="Add", command=self.add_goal,
                                bg="#2196F3", fg="white", font=("Arial", 9))
        add_goal_btn.pack(side=tk.LEFT)
        
        # Output for goals in Goals list
        self.goals_listbox = tk.Listbox(goals_frame, font=("Arial", 10), height=15, bg="white")
        self.goals_listbox.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Remove goal button for Goals list
        remove_goal_btn = tk.Button(goals_frame, text="Remove Goal", command=self.remove_goal,
                                    bg="#f44336", fg="white", font=("Arial", 9))
        remove_goal_btn.pack(pady=5)
    
    def create_personal_workspace(self):
        # White space for personal workspace button
        nav_frame = tk.Frame(self.root, bg="#f0f0f0")
        nav_frame.pack(pady=15)
        
        # Personal workspace button to go to personal workspace
        workspace_btn = tk.Button(nav_frame, text="Go to Personalized Workspace →", 
                                command=self.show_personalized_workspace,
                                bg="#9C27B0", fg="white", font=("Arial", 11, "bold"),
                                padx=20, pady=10)
        workspace_btn.pack()
    def show_main_hub(self):
        """Build and display the main hub interface with side-by-side task and goals sections"""
        self.clear_window()
        
        title = tk.Label(self.root, text="Personal Hub", font=("Arial", 22, "bold"), bg="#f0f0f0")
        title.pack(pady=15)
        
        # Create container to hold both task and goals frames side by side
        container = tk.Frame(self.root, bg="#f0f0f0")
        container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # ======= LEFT SIDE - Task Agenda =======

        self.create_task_agenda(container)

        # ======= RIGHT SIDE - Goals List =======
        self.create_goals_list(container)

        # ===== BOTTOM - Personal Workspace =====
        self.create_personal_workspace()
        
        # Populate the listboxes with current data
        self.update_task_list()
        self.update_goals_list()
    
    # Add task function for the Task agenda
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.update_task_list()
            self.save_data()  # Save to file after adding
        else:
            messagebox.showwarning("Empty Task", "Please enter a task")
    
    def remove_task(self):
        """Remove the currently selected task from the listbox.
        Uses try-except because curselection() raises IndexError if nothing is selected."""
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks.pop(index)
            self.update_task_list()
            self.save_data()  # Save to file after removing
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a task to remove")
    
    def update_task_list(self):
        """Clear and repopulate the task listbox with current tasks.
        Called after any modification to ensure UI stays in sync with data."""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)
    
    def add_goal(self):
        """Once there is input from the entry line, 
        input the goal into the personal_hub_data.json file and update the goals tab.
        Has an output if no input was given."""
        goal = self.goals_entry.get().strip()
        if goal:
            self.goals.append(goal)
            self.goals_entry.delete(0, tk.END)
            self.update_goals_list()
            self.save_data()  # Save to file after adding
        else:
            messagebox.showwarning("Empty Goal", "Please enter a goal")
    
    # Remove Goal function for the Goals list
    def remove_goal(self):
        """Remove the currently selected goal from the listbox.
        Uses try-except because curselection() raises IndexError if nothing is selected."""
        try:
            index = self.goals_listbox.curselection()[0]
            self.goals.pop(index)
            self.update_goals_list()
            self.save_data()  # Save to file after removing
        except IndexError:
            messagebox.showwarning("No Selection", "Please select a goal to remove")
    
    def update_goals_list(self):
        """Clear and repopulate the goals listbox with current goals.
        Called after any modification to ensure UI stays in sync with data."""
        self.goals_listbox.delete(0, tk.END)
        for goal in self.goals:
            self.goals_listbox.insert(tk.END, goal)
    
    def show_personalized_workspace(self):
        """Display placeholder screen for future workspace features"""
        self.clear_window()
        
        title = tk.Label(self.root, text="Personalized Workspace", 
                        font=("Arial", 22, "bold"), bg="#f0f0f0")
        title.pack(pady=30)
        
        placeholder = tk.Label(self.root, text="Coming Soon!\n\n• Daily Quotes\n• Movie Recommendations\n• Sport Stat Tracker",
                            font=("Arial", 14), bg="#f0f0f0", fg="#666666", justify=tk.CENTER)
        placeholder.pack(pady=50)
        
        back_btn = tk.Button(self.root, text="← Back to Personal Hub", 
                            command=self.show_main_hub,
                            bg="#9C27B0", fg="white", font=("Arial", 11, "bold"),
                            padx=20, pady=10)
        back_btn.pack(pady=20)

# Main function
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalHubApp(root)
    root.mainloop()
