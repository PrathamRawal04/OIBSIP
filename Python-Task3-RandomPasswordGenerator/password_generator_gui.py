import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Random Password Generator")
        self.root.geometry("450x550")
        self.root.resizable(False, False)



        # variables
        self.length_var = tk.intvar(value=12)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.num_var = tk.BooleanVar(value=True)
        self.sym_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=True)
        self.history = []


        self.create_widgets()


    def create_widgets(self):
        # Title
        tilte_label = tk.Label(self.root, text="Seccure Password Generator", font=("Arial", 16, "bold"))
        tilte_label.pack(pady=15)

        # length Selector
        len_frame = tk.frame(self.root)
        len_frame.pack(fill="x", padx=20, pady=5)
        tk.Label(len_frame, text="Password length (8-64):", font=("Arial", 11)).pack(side="left ")
        self.len_spinbox = tk.Spinbox(len_frame, from_=8, to=64, textvariable=self.length_var, width=5, font=("Arial", 11))
        self.len_spinbox.pack(side="right")


        # checkboxes for Criteria
        chk_frame = tk.LabelFrame(self.root, text="Complexity Settings ", font=("Arial", 10, "bold"), padx=15, pady=10)
        chk_frame.pack(fill="x", padx=20, pady=10)


        tk.checkbutton(chk_frame, text="Include Uppercase Letters (A-Z)", variables=self.upper_var, font=("Arial", 10)).pack(anchor="w", pady=2)