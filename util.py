import tkinter as tk
from tkinter import messagebox


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground="black",
        activeforeground="white",
        highlightbackground=color,
        highlightcolor=color,
        relief=tk.FLAT,
        fg=fg,
        bg=color,
        command=command,
        height=2,
        width=20,
        font=('Helvetica', 12)  # Adjusted the font size
    )
    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Helvetica", 12), justify="left")  # Adjusted the font size
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window, height=2, width=15, font=("Arial", 12))  # Adjusted the font size
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)

    
  