import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("To-Do List")
root.geometry("500x600")
root.config(bg="#f0f0f0") # Light grey background

# Store tasks in a list so we can use them later
tasks = []

# Title label, styled and formatted properly with nice padding
title = tk.Label(root, text="My Task Agenda", font=("Arial", 18, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# Frame for input field and add button so we can add tasks
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10) # Input frame for better layout

task_entry = tk.Entry(input_frame, width=35, font=("Arial", 11))
task_entry.pack(side=tk.LEFT, padx=5)

# Add task to list and update display
def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append(task)
        task_entry.delete(0, tk.END)
        update_task_list()
    else:
        messagebox.showwarning("Empty Task", "Please enter a task") # Handle empty task input

# Remove selected task from list and update display
def remove_task():
    try:
        index = task_listbox.curselection()[0]
        tasks.pop(index)
        update_task_list()
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to remove") # Handle case where no task is selected

# Refresh the task display so we can see the updated list
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

add_btn = tk.Button(input_frame, text="Add Task", command=add_task, bg="#4CAF50", fg="white", font=("Arial", 10))
add_btn.pack(side=tk.LEFT, padx=5) # Add button to add tasks

# Listbox to display tasks with scrollbar so we can see the tasks
task_listbox = tk.Listbox(root, font=("Arial", 11), height=15, bg="white")
task_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Remove task button so any tasks that have bene completed will be removed
remove_btn = tk.Button(root, text="Remove Task", command=remove_task, bg="#f44336", fg="white", font=("Arial", 10))
remove_btn.pack(pady=10)

root.mainloop()
