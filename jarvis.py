import os
import webbrowser
import speech_recognition as sr
import pyttsx3
import subprocess
import datetime
import time

# ===== INITIAL SETUP =====
def install_dependencies():
    """Auto-install required packages if missing"""
    try:
        import speech_recognition, pyttsx3, pyaudio
    except ImportError:
        print("Installing required libraries...")
        os.system('pip install SpeechRecognition pyttsx3 pyaudio')
        print("Please restart the script after installation.")
        exit()

install_dependencies()

# ===== VOICE ENGINE =====
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Try to set a pleasant voice (different indices for different systems)
try:
    engine.setProperty('voice', voices[0].id)  # Usually [0] = male, [1] = female
except:
    pass

# Adjust speech rate
engine.setProperty('rate', 150)

def speak(text):
    """Make JARVIS speak with improved error handling"""
    print(f"JARVIS: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech Error: {e}")

# ===== SPEECH RECOGNITION =====
def take_command():
    """Take voice command with better error handling"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5)
            print("Processing...")
            query = r.recognize_google(audio).lower()
            print(f"You: {query}")
            return query
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except Exception as e:
            print(f"Recognition Error: {e}")
            return ""

# ===== CORE FUNCTIONS =====
def greet():
    """Personalized greeting"""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak("Good morning ma'am! JARVIS at your service.")
    elif 12 <= hour < 18:
        speak("Good afternoon ma'am! Welcome Home")
    else:
        speak("Good evening anushka ma'am! JARVIS at your service.")

def open_app(app_name):
    """Open applications with path validation"""
    app_paths = {
        'word': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
        'excel': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE',
        'powerpoint': 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE',
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    }
    
    if app_name in app_paths:
        try:
            subprocess.Popen(app_paths[app_name])
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Couldn't open {app_name}. It might not be installed.")
            print(f"Error: {e}")
    else:
        speak("That application isn't configured yet.")

# ===== MAIN LOOP =====
if __name__ == "__main__":
    greet()
    
    while True:
        query = take_command()
        
        if not query:
            continue
            
        # Basic commands
        if 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")
            
        elif 'open google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")
            
        elif 'open word' in query:
            open_app('word')
            
        elif 'open notepad' in query:
            open_app('notepad')
            
        elif 'time' in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")
            
        elif 'date' in query:
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            speak(f"Today is {current_date}")
            
        elif 'exit' in query or 'bye' in query:
            speak("Shutting down. Have a great day ma'am!")
            break
            
        elif 'jarvis' in query:
            speak("Yes ma'am?")
            
        else:
            speak("I didn't understand that command. Try something like 'open YouTube' or 'what time is it?'")
