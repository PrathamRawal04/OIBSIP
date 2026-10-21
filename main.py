import datetime
import smtplib
import threading
import time 
import webbrowser
import nltk
from nltk.tokenize import word_tokenize
import pyttsx3
import requests
import speech_recognition as sr


# dowload necessary NLTK data for tokenization
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)


# Initialize Text-to-Speech Engine
engine = pyttsx3.init()


def speak(text):
    """"Speaks text out loud and prints to console."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen_command():
    """captures voice input from the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for commands...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.waitTimeoutError:
            return ""
        except sr.UnknowValueError:
            speak("sorry, I didn't catch that. cloud you please repeat?")
            return ""
        except sr.requestsError:
            speak("Network error. please check your internet connection.")
            return ""

def set_timer(seconds):
    """Advanced Features: sets a background timed remainder."""

    def timer_thread():
        time.sleep(seconds)
        speak(f"Remainder! Your {seconds} seconds timer has finished.")

    threading.Thread(target=timer_thread).start()
    speak(f"Timer set for {seconds} seconds.")
    