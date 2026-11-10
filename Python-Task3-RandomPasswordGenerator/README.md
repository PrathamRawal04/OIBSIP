ask 3: Random Password Generator

📌 Executive Summary

The Random Password Generator is a Python application developed as part of the Oasis Infobyte Virtual Internship Program. The primary objective of this project is to provide users with a reliable tool for generating strong, customized, and cryptographically secure passwords.

The project is structured into two implementation levels:

Beginner Tier (CLI): A command-line script utilizing Python's built-in random and string modules for lightweight, interactive execution.

Advanced Tier (GUI): A desktop application built with tkinter, leveraging Python's secrets module for cryptographic security, interactive controls, strength estimation, history tracking, and clipboard integration.

🚀 Features

1. Beginner Tier (Command-Line Interface)

Length Validation: User specifies password length (enforces a minimum of 8 characters for basic security standard).

Dynamic Character Selection: Interactive prompts allow users to include/exclude:

Uppercase letters (A-Z)

Lowercase letters (a-z)

Numeric digits (0-9)

Special symbols (!@#$%^&*()...)

Input Validation & Fallback: Prevents zero-length selections or invalid non-numeric inputs by falling back to safe default choices.

Execution Loop: Allows generating multiple passwords in a single session without restarting the script.

2. Advanced Tier (Graphical User Interface)

User-Friendly UI: Designed with tkinter for an intuitive desktop interface.

Cryptographically Secure PRNG: Uses Python's secrets module instead of pseudo-random algorithms to guard against entropy prediction.

Guaranteed Character Inclusion: Guarantees that at least one character from each selected category is present in the final generated string.

Ambiguous Character Filter: Provides a toggle option to exclude visually similar characters (0, O, l, 1, I) to reduce manual typing errors.

Real-time Password Strength Meter: Evaluates password complexity dynamically and ranks it as Weak, Medium, or Strong based on length and character diversity.

Session History: Retains the last 5 generated passwords during the active app session.

Clipboard Integration: Integrates pyperclip to automatically copy generated passwords to the system clipboard.

🛠️ Project Structure & Directory Layout

To comply with Oasis Infobyte repository rules, the files within your OIBSIP repository should follow this hierarchy:

OIBSIP/
├── Python-Task1-VoiceAssistant/
├── Python-Task2-BMICalculator/
└── Python-Task3-RandomPasswordGenerator/
    ├── README.md
    ├── requirements.txt
    ├── password_generator_cli.py
    └── password_generator_gui.py


💻 Tech Stack & Requirements

Language: Python 3.8+

GUI Framework: tkinter (Built-in with standard Python installations)

Standard Libraries: secrets, random, string, messagebox

External Dependencies:

pyperclip (Handles cross-platform system clipboard operations)

## Features
* **Custom Length:** Choose your desired password length (minimum 8 characters).
* **Character Customization:** Toggle uppercase letters, lowercase letters, numbers, and symbols.
* **Cryptographically Secure:** Uses Python's built-in `secrets` module for secure randomness.
* **Auto-Copy:** Automatically copies the generated password to your clipboard.


📥 Installation & Setup Instructions

Step 1: Clone the Repository

Open your terminal or command prompt and clone the workspace:

git clone https://github.com/PrathamRawal04/OIBSIP.git
cd OIBSIP/Python-Task3-RandomPasswordGenerator


Step 2: Set Up Virtual Environment (Optional but Recommended)

# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate on Linux/macOS
source venv/bin/activate


Step 3: Install Required Dependencies

Install the required packages using the provided requirements.txt:

pip install -r requirements.txt


🏃 Execution Guide

Running the CLI Version

To execute the interactive command-line application:

python password_generator_cli.py


Running the GUI Application

To launch the graphical desktop application:

python password_generator_gui.py


🔒 Security Best Practices Implemented

Entropy & Randomness: Standard pseudo-random number generators (random) are deterministic and unsuitable for security keys. This project uses secrets.SystemRandom(), which accesses OS-level cryptographic entropy.

Ambiguity Prevention: Disabling ambiguous characters reduces typos when entering passwords on devices without copy-paste capabilities.

No Local Logging: Passwords generated during the session are held strictly in memory and are discarded when the application closes.