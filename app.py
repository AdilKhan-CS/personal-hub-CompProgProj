import tkinter as tk
import json
import random
from tkinter import messagebox

def show_message():
    text_box.delete("1.0", tk.END)

root = tk.Tk()
root.title("quote display")
root.geometry("1280x760")

with open('quotes.json') as f:
    quotes_data = json.load(f)  

text_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 12))
text_box.pack(pady=20)

def show_message():
    text_box.delete("1.0", tk.END)
    quote = random.choice(quotes_data)
    text_box.insert("1.0", quote)

button = tk.Button(root, text="Show Quote", command=show_message)
button.pack()

root.mainloop()