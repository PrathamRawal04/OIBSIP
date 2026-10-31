import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# DATABASE SETUP & UTILITIES
# -------------------------------------------------------------
DB_FILE = "bmi_history.db"

def init_db():
    """Initialize SQLite database for storing user records."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            recorded_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_record(username, weight, height, bmi, category):
    """Save calculation entry into local SQLite DB."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("""
        INSERT INTO bmi_records (username, weight, height, bmi, category, recorded_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username.strip().lower(), weight, height, bmi, category, timestamp))
    conn.commit()
    conn.close()

def fetch_history(username):
    """Retrieve all historical records for a specific user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT recorded_at, bmi FROM bmi_records
        WHERE username = ? ORDER BY id ASC
    """, (username.strip().lower(),))
    rows = cursor.fetchall()
    conn.close()
    return rows


# -------------------------------------------------------------
# CORE LOGIC
# -------------------------------------------------------------
def calculate_bmi(weight_kg, height_m):
    """Calculate BMI given weight in kg and height in meters."""
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi):
    """Classify BMI score based on WHO health categories."""
    if bmi < 18.5:
        return "Underweight", "#2980b9"   # Blue
    elif 18.5 <= bmi <= 24.9:
        return "Normal Weight", "#2ecc71" # Green
    elif 25.0 <= bmi <= 29.9:
        return "Overweight", "#f39c12"    # Orange
    else:
        return "Obese", "#e74c3c"         # Red


# -------------------------------------------------------------
# DESKTOP GUI INTERFACE (tkinter)
# -------------------------------------------------------------
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Body Mass Index Calculator & Tracker")
        self.root.geometry("460x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f6f9")

        init_db()

        # Custom Styling
        self.bg_color = "#f4f6f9"
        self.card_color = "#ffffff"

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Label(
            self.root,
            text="BMI Calculator & Tracker",
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg="#2c3e50"
        )
        header.pack(pady=(20, 5))

        sub_header = tk.Label(
            self.root,
            text="Track your health progress effortlessly",
            font=("Helvetica", 10, "italic"),
            bg=self.bg_color,
            fg="#7f8c8d"
        )
        sub_header.pack(pady=(0, 15))



        # Input Card
        input_card = tk.Frame(self.root, bg=self.card_color, bd=1, relief="ridge", padx=20, pady=15)
        input_card.pack(fill="x", padx=25, pady=5)

        # Name Input
        tk.Label(input_card, text="Username / ID:", font=("Helvetica", 10, "bold"), bg=self.card_color, fg="#34495e").grid(row=0, column=0, sticky="w", pady=8)
        self.user_entry = ttk.Entry(input_card, width=22, font=("Helvetica", 10))
        self.user_entry.grid(row=0, column=1, pady=8, padx=(10, 0))

        # Weight Input
        tk.Label(input_card, text="Weight (kg):", font=("Helvetica", 10, "bold"), bg=self.card_color, fg="#34495e").grid(row=1, column=0, sticky="w", pady=8)
        self.weight_entry = ttk.Entry(input_card, width=22, font=("Helvetica", 10))
        self.weight_entry.grid(row=1, column=1, pady=8, padx=(10, 0))

        # Height Input
        tk.Label(input_card, text="Height (m):", font=("Helvetica", 10, "bold"), bg=self.card_color, fg="#34495e").grid(row=2, column=0, sticky="w", pady=8)
        self.height_entry = ttk.Entry(input_card, width=22, font=("Helvetica", 10))
        self.height_entry.grid(row=2, column=1, pady=8, padx=(10, 0))

        # Buttons Panel
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=15)

        calc_btn = tk.Button(
            btn_frame,
            text="Calculate & Save",
            font=("Helvetica", 10, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.handle_calculation
        )
        calc_btn.grid(row=0, column=0, padx=8)

        trend_btn = tk.Button(
            btn_frame,
            text="View Trend Graph",
            font=("Helvetica", 10, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            activeforeground="white",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.handle_plot
        )
        trend_btn.grid(row=0, column=1, padx=8)

        # Result Display Area
        self.result_card = tk.Frame(self.root, bg=self.card_color, bd=1, relief="groove", height=150)
        self.result_card.pack(fill="x", padx=25, pady=10)
        self.result_card.pack_propagate(False)

        self.score_label = tk.Label(
            self.result_card,
            text="BMI: --",
            font=("Helvetica", 20, "bold"),
            bg=self.card_color,
            fg="#7f8c8d"
        )
        self.score_label.pack(pady=(25, 5))

        self.cat_label = tk.Label(
            self.result_card,
            text="Category: Enter values to compute",
            font=("Helvetica", 11),
            bg=self.card_color,
            fg="#95a5a6"
        )
        self.cat_label.pack()

    def handle_calculation(self):
        user = self.user_entry.get().strip()
        weight_raw = self.weight_entry.get().strip()
        height_raw = self.height_entry.get().strip()

        # Validation
        if not user:
            messagebox.showwarning("Missing Input", "Please enter a username to store your records.")
            return

        try:
            weight = float(weight_raw)
            height = float(height_raw)
            if weight <= 0 or height <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter positive numeric values for weight (kg) and height (m).")
            return

        # Perform Calculation
        bmi_score = calculate_bmi(weight, height)
        category_name, theme_color = classify_bmi(bmi_score)

        # Update GUI Output
        self.score_label.config(text=f"BMI: {bmi_score:.2f}", fg=theme_color)
        self.cat_label.config(text=f"Category: {category_name}", fg=theme_color)

        # Save to Local SQLite DB
        save_record(user, weight, height, bmi_score, category_name)
        messagebox.showinfo("Success", f"Record saved successfully for '{user}'!")

    def handle_plot(self):
        user = self.user_entry.get().strip()
        if not user:
            messagebox.showwarning("Username Required", "Enter your username in the input field to view your historical graph.")
            return

        records = fetch_history(user)
        if not records:
            messagebox.showinfo("No Records Found", f"No historical BMI data available for user '{user}'.")
            return

        dates = [r[0] for r in records]
        scores = [r[1] for r in records]

        # Matplotlib Visualization
        plt.figure(figsize=(7, 4.5))
        plt.plot(dates, scores, marker="o", color="#3498db", linewidth=2, markersize=6, label="BMI")
        
        # Color Reference Lines
        plt.axhline(y=18.5, color="#2980b9", linestyle="--", alpha=0.6, label="Underweight (<18.5)")
        plt.axhline(y=24.9, color="#2ecc71", linestyle="--", alpha=0.6, label="Normal (18.5-24.9)")
        plt.axhline(y=29.9, color="#f39c12", linestyle="--", alpha=0.6, label="Overweight (25-29.9)")

        plt.title(f"BMI History & Progress Trend - {user.capitalize()}", fontsize=12, fontweight="bold")
        plt.xlabel("Date & Time", fontsize=9)
        plt.ylabel("BMI Score", fontsize=9)
        plt.xticks(rotation=25, ha="right", fontsize=8)
        plt.grid(True, linestyle=":", alpha=0.6)
        plt.legend(fontsize=8, loc="upper right")
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()