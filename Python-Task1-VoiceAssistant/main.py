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
import pyaudiowpatch as pyaudio

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
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            speak("sorry, I didn't catch that. cloud you please repeat?")
            return ""
        except sr.RequestsError:
            speak("Network error. please check your internet connection.")
            return ""

def set_timer(seconds):
    """Advanced Features: sets a background timed remainder."""

    def timer_thread():
        time.sleep(seconds)
        speak(f"Remainder! Your {seconds} seconds timer has finished.")

    threading.Thread(target=timer_thread).start()
    speak(f"Timer set for {seconds} seconds.")

def get_weather():
  """Advanced Feature: Fetches live weather updates using OpenWeatherMap API."""
  api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your free API key
  city = "London"
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
  try:
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
      temp = data["main"]["temp"]
      desc = data["weather"][0]["description"]
      speak(
          f"The current temperature in {city} is {temp} degrees Celsius with"
          f" {desc}."
      )
    else:
      speak("Could not fetch weather data for that location.")
  except Exception:
    speak("Weather service is currently unavailable.")


def send_email():
  """Advanced Feature: Sends an email via voice command using smtplib."""
  try:
    sender_email = "your_test_email@gmail.com"
    sender_password = "your_app_password"
    receiver_email = "recipient_email@gmail.com"

    speak("What message should I send in the email?")
    message_content = listen_command()

    if not message_content:
      speak("No message detected. Canceling email.")
      return

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(
        sender_email,
        receiver_email,
        f"Subject: Voice Assistant Alert\n\n{message_content}",
    )
    server.quit()
    speak("Email has been sent successfully!")
  except Exception:
    speak("Failed to send email due to an authentication or network error.")


def run_assistant():
  # Local knowledge base for general questions (Advanced Checklist Requirement)
  knowledge_base = {
      "what is python": (
          "Python is a high-level, interpreted programming language known for"
          " its readability and versatility."
      ),
      "what is artificial intelligence": (
          "Artificial intelligence is the simulation of human intelligence in"
          " machines programmed to think and learn."
      ),
      "what is an api": (
          "An API, or application programming interface, allows different"
          " software applications to communicate with each other."
      ),
  }

  speak("Advanced Voice Assistant is online. How can I help you today?")

  while True:
    raw_command = listen_command()

    if not raw_command:
      continue

    # 1. Advanced NLTK Intent Parsing
    tokens = word_tokenize(raw_command)

    # 2. Check General Knowledge Base
    matched_kb = False
    for query, answer in knowledge_base.items():
      if query in raw_command:
        speak(answer)
        matched_kb = True
        break
    if matched_kb:
      continue

    # 3. Standard Core & Advanced Routing
    if "hello" in tokens or "hi" in tokens:
      speak("Hello there! How can I assist you?")

    elif "time" in tokens:
      current_time = datetime.datetime.now().strftime("%I:%M %p")
      speak(f"The current time is {current_time}")

    elif "date" in tokens:
      current_date = datetime.datetime.now().strftime("%B %d, %Y")
      speak(f"Today's date is {current_date}")

    elif "search" in tokens:
      speak("What would you like me to search for?")
      query = listen_command()
      if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        speak(f"Here are the search results for {query}")

    elif "weather" in tokens:
      get_weather()

    elif "timer" in tokens or "reminder" in tokens:
      speak("How many seconds should I set the timer for?")
      sec_command = listen_command()
      try:
        seconds = int([int(s) for s in sec_command.split() if s.isdigit()][0])
        set_timer(seconds)
      except Exception:
        speak("I couldn't understand the duration. Please try again.")

    elif "email" in tokens:
      send_email()

    elif "exit" in tokens or "stop" in tokens or "quit" in tokens:
      speak("Goodbye! Have a great day.")
      break

    else:
      speak(
          "I heard your input, but that command is not recognized in my"
          " current knowledge base."
      )


if __name__ == "__main__":
  run_assistant()