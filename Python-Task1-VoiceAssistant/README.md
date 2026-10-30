# Python Task 1: Voice Assistant

This is my project for Task 1 of the Oasis Infobyte Python Programming internship. It is a voice-controlled assistant built in Python that handles daily tasks through speech.

---

## The Problem
When building a voice assistant from scratch, a few major roadblocks usually come up:
* **Rigid Command Matching:** Traditional assistants only understand exact phrasing, meaning if a user speaks in a natural, free-form sentence, the program fails to recognize the intent.
* **Audio Processing & Dependencies:** Getting a microphone to reliably pick up speech and converting it to text requires handling external system libraries and audio drivers, which often throw installation errors.
* **Network & Authentication Hurdles:** Pulling live external data like weather updates or automating emails requires handling secure API keys and managing command-line Git authentication securely without using plain passwords.

---

## What This Project Solves
* Eliminates rigid keyword restrictions by using **NLTK (Natural Language Toolkit)** tokenization to break down and interpret free-form user speech.
* Automates everyday utility tasks—such as checking real-time weather, setting background timers, sending emails, and looking up web queries—all hands-free.
* Provides graceful error handling so the assistant never crashes when speech isn't understood or when the network drops.

---

## How It Was Solved
* **Intent Parsing:** Integrated `nltk` to tokenize spoken commands into individual words, allowing the script to catch key intent triggers regardless of exact sentence structure.
* **Audio & Speech Handling:** Used the `speech_recognition` library paired with Google's speech recognition API to capture microphone input, alongside `pyttsx3` for offline text-to-speech feedback.
* **API & Automation Integration:** Connected third-party endpoints via the `requests` library for live weather data, used `smtplib` for email handling, and implemented Python multi-threading so timer alerts run in the background without freezing the assistant.
* **Version Control Setup:** Resolved command-line Git push limitations by properly configuring local tracking, setting up a virtual environment (`venv`) to keep dependencies isolated, and authenticating via a secure GitHub Personal Access Token (PAT).

---

## Features
* **Voice Recognition:** Listens to your spoken commands through your mic.
* **Text-to-Speech:** Talks back to you with audio responses.
* **Date & Time:** Tells you the current time and date when asked.
* **Web Search:** Opens up Google searches automatically.
* **Weather Updates:** Fetches live weather information using an API.
* **Reminders:** Sets background timers and alerts you when time's up.
* **Email:** Sends simple emails via voice commands.


## Requirements
* Python 3.x
* `SpeechRecognition`
* `pyttsx3`
* `requests`
* `nltk`

---

## How to Run It

1. Clone the repository and navigate into the task folder:
   ```bash
   cd Python-Task1-VoiceAssistant