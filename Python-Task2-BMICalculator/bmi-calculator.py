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
