import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("To-Do List")
root.geometry("500x600")
root.config(bg="#f0f0f0")

# Store tasks in a list
tasks = []

# Title label
title = tk.Label(root, text="My Task Agenda", font=("Arial", 18, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# Frame for input
input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=10)

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
        messagebox.showwarning("Empty Task", "Please enter a task")

# Remove selected task from list
def remove_task():
    try:
        index = task_listbox.curselection()[0]
        tasks.pop(index)
        update_task_list()
    except IndexError:
        messagebox.showwarning("No Selection", "Please select a task to remove")

# Refresh the task display
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, task)

add_btn = tk.Button(input_frame, text="Add Task", command=add_task, bg="#4CAF50", fg="white", font=("Arial", 10))
add_btn.pack(side=tk.LEFT, padx=5)

# Listbox to display tasks
task_listbox = tk.Listbox(root, font=("Arial", 11), height=15, bg="white")
task_listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Remove task button
remove_btn = tk.Button(root, text="Remove Task", command=remove_task, bg="#f44336", fg="white", font=("Arial", 10))
remove_btn.pack(pady=10)

root.mainloop()
