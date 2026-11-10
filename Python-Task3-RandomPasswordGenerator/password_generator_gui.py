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
        self.length_var = tk.IntVar(value=12)
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
        len_Frame = tk.Frame(self.root)
        len_Frame.pack(fill="x", padx=20, pady=5)
        tk.Label(len_Frame, text="Password length (8-64):", font=("Arial", 11)).pack(side="left")
        self.len_spinbox = tk.Spinbox(len_Frame, from_=8, to=64, textvariable=self.length_var, width=5, font=("Arial", 11))
        self.len_spinbox.pack(side="right")


        # checkboxes for Criteria
        chk_Frame = tk.LabelFrame(self.root, text="Complexity Settings ", font=("Arial", 10, "bold"), padx=15, pady=10)
        chk_Frame.pack(fill="x", padx=20, pady=10)



        tk.Checkbutton(chk_Frame, text="Include Uppercase Letters (A-Z)", variable=self.upper_var, font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Checkbutton(chk_Frame, text="Include Lowercase Letters (a-z)", variable=self.lower_var, font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Checkbutton(chk_Frame, text="Include Numbers (0-9)", variable=self.num_var, font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Checkbutton(chk_Frame, text="Include Symbols (!@#$%)", variable=self.sym_var, font=("Arial", 10)).pack(anchor="w", pady=2)
        tk.Checkbutton(chk_Frame, text="Exclude Ambiguous Characters (0, O, l, 1, I)", variable=self.ambiguous_var, font=("Arial", 10)).pack(anchor="w", pady=2)


        # Generate Button
        gen_btn = tk.Button(self.root, text="Generate Password", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=self.generate_password)
        gen_btn.pack(fill="x", padx=20, pady=10)


        # Result Field & Copy Button
        res_Frame = tk.Frame(self.root)
        res_Frame.pack(fill="x", padx=20, pady=5)
        
        self.result_entry = tk.Entry(res_Frame, font=("Courier", 12), justify="center")
        self.result_entry.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 5))

        copy_btn = tk.Button(res_Frame, text="Copy", font=("Arial", 10), command=self.copy_to_clipboard)
        copy_btn.pack(side="right")

        # Strength Indicator Label
        self.strength_label = tk.Label(self.root, text="Strength: -", font=("Arial", 11, "bold"))
        self.strength_label.pack(pady=5)

        # History Section
        hist_Frame = tk.LabelFrame(self.root, text=" Recent Session History (Last 5) ", font=("Arial", 10, "bold"), padx=10, pady=5)
        hist_Frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.history_box = tk.Listbox(hist_Frame, font=("Courier", 9), height=5)
        self.history_box.pack(fill="both", expand=True)

    def generate_password(self):
        length = self.length_var.get()
        
        # Collect character pools
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        nums = string.digits
        syms = string.punctuation

        if self.ambiguous_var.get():
            ambiguous = "0O1lI"
            lower = "".join(c for c in lower if c not in ambiguous)
            upper = "".join(c for c in upper if c not in ambiguous)
            nums = "".join(c for c in nums if c not in ambiguous)
            syms = "".join(c for c in syms if c not in ambiguous)

        char_pool = ""
        required_chars = []

        if self.upper_var.get():
            char_pool += upper
            required_chars.append(secrets.choice(upper))
        if self.lower_var.get():
            char_pool += lower
            required_chars.append(secrets.choice(lower))
        if self.num_var.get():
            char_pool += nums
            required_chars.append(secrets.choice(nums))
        if self.sym_var.get():
            char_pool += syms
            required_chars.append(secrets.choice(syms))

        if not char_pool:
            messagebox.showerror("Error", "Please select at least one character type!")
            return

        if length < len(required_chars):
            length = len(required_chars)
            self.length_var.set(length)

        # Fill remaining length using cryptographically secure choices
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [secrets.choice(char_pool) for _ in range(remaining_length)]
        
        # Shuffle securely
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)

        # Display result
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)

        # Calculate Strength
        self.evaluate_strength(password)

        # Update History (Keep last 5)
        self.history.insert(0, password)
        if len(self.history) > 5:
            self.history.pop()
        
        self.history_box.delete(0, tk.END)
        for pwd in self.history:
            self.history_box.insert(tk.END, pwd)

        # Auto copy to clipboard
        pyperclip.copy(password)

    def evaluate_strength(self, password):
        score = 0
        if len(password) >= 12: score += 1
        if len(password) >= 16: score += 1
        if any(c.isupper() for c in password) and any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in string.punctuation for c in password): score += 1

        if score <= 2:
            self.strength_label.config(text="Strength: Weak", fg="red")
        elif score <= 4:
            self.strength_label.config(text="Strength: Medium", fg="orange")
        else:
            self.strength_label.config(text="Strength: Strong", fg="green")

    def copy_to_clipboard(self):
        pwd = self.result_entry.get()
        if pwd:
            pyperclip.copy(pwd)
            messagebox.showinfo("Success", "Password copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()