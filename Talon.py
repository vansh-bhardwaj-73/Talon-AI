import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import os
import time
from datetime import datetime
import subprocess
import threading
import json
from PIL import Image, ImageTk
import pvporcupine
import pyaudio
import struct
import pystray




# ============================================
# CONFIGURATION
# ============================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

USER_NAME = "User"
ASSISTANT_NAME = "Talon"
DEFAULT_CITY = "Delhi"
WAKE_WORD = "hey Talon"

HISTORY_FILE = "Talon_chat_history.json"

print("="*60)
print(f"      {ASSISTANT_NAME} - AI Voice Assistant")
print("="*60)
print(f"✅ Groq API: Configured")
print(f"🎤 Wake Word: '{WAKE_WORD}'")
print(f"🎧 Background Listening: ENABLED")
print("="*60 + "\n")


# ============================================
# WEBSITES DICTIONARY
# ============================================
websites = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "facebook": "https://www.facebook.com",
    "linkedin": "https://www.linkedin.com",
    "twitter": "https://www.twitter.com",
    "github": "https://www.github.com",
    "instagram": "https://www.instagram.com",
    "reddit": "https://www.reddit.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "netflix": "https://www.netflix.com",
    "stackoverflow": "https://stackoverflow.com",
    "wikipedia": "https://www.wikipedia.org"
}


# ============================================
# SPEECH FUNCTIONS
# ============================================
recognizer = sr.Recognizer()
recognizer.energy_threshold = 100
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.5


def speak(text):
    """Speak text using TTS"""
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
        del engine
    except Exception as e:
        print(f"Speech error: {e}")


def listen_for_command(timeout=10):
    """Listen for voice command"""
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
        
        command = recognizer.recognize_google(audio)
        return command
    
    except:
        return ""


# ============================================
# UTILITY FUNCTIONS
# ============================================

def get_time():
    """Get current time"""
    try:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The time is {time_str}"
    except:
        return "Could not get time"


def get_date():
    """Get current date"""
    try:
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        day_name = now.strftime("%A")
        return f"Today is {day_name}, {date_str}"
    except:
        return "Could not get date"


def get_weather(command=None):
    """Get weather information"""
    if not WEATHER_API_KEY:
        return "Weather service not configured. Get free API key from openweathermap.org"
    
    try:
        city = DEFAULT_CITY
        if command:
            words = command.replace("weather", "").replace("in", "").replace("of", "").strip()
            if words:
                city = words
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get("cod") == 200:
            temp = round(data["main"]["temp"], 1)
            feels = round(data["main"]["feels_like"], 1)
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            
            report = f"Weather in {city} is {desc}. "
            report += f"Temperature is {temp} degrees Celsius. "
            report += f"Feels like {feels} degrees. "
            report += f"Humidity is {humidity} percent."
            
            return report
        else:
            return f"Could not find weather for {city}"
    
    except:
        return "Weather service unavailable"


def shutdown_computer():
    """Shutdown computer with confirmation"""
    confirm = messagebox.askyesno("Confirm Shutdown", "Are you sure you want to SHUTDOWN the computer?")
    if confirm:
        speak("Shutting down computer now. Goodbye!")
        time.sleep(1)
        os.system("shutdown /s /t 1")
        return "Computer is shutting down..."
    else:
        return "Shutdown cancelled"


def restart_computer():
    """Restart computer with confirmation"""
    confirm = messagebox.askyesno("Confirm Restart", "Are you sure you want to RESTART the computer?")
    if confirm:
        speak("Restarting computer now")
        time.sleep(1)
        os.system("shutdown /r /t 1")
        return "Computer is restarting..."
    else:
        return "Restart cancelled"


def sleep_computer():
    """Put computer to sleep with confirmation"""
    confirm = messagebox.askyesno("Confirm Sleep", "Are you sure you want to put the computer to SLEEP?")
    if confirm:
        speak("Going to sleep. Good night!")
        time.sleep(1)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Computer is going to sleep..."
    else:
        return "Sleep cancelled"


def lock_computer():
    """Lock computer"""
    confirm = messagebox.askyesno("Confirm Lock", "Are you sure you want to LOCK the computer?")
    if confirm:
        speak("Locking computer")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Computer locked"
    else:
        return "Lock cancelled"


def search_youtube(query):
    """Search YouTube"""
    try:
        query = query.replace("search", "").replace("youtube", "").replace("on", "").replace("for", "").replace("find", "").strip()
        
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Searching YouTube for '{query}'"
        else:
            return "What do you want to search on YouTube?"
    except:
        return "Could not search YouTube"


def search_google(query):
    """Search Google"""
    try:
        query = query.replace("search", "").replace("google", "").replace("on", "").replace("for", "").replace("find", "").replace("look up", "").strip()
        
        if query:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Searching Google for '{query}'"
        else:
            return "What do you want to search?"
    except:
        return "Could not search Google"


def play_music_on_youtube(command):
    """Play music on YouTube - NO CONFIRMATION"""
    try:
        song = command.replace("play", "").replace("song", "").replace("music", "").replace("video", "").strip()
        
        if song:
            url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Playing {song} on YouTube"
        else:
            return "What song do you want to play?"
    except:
        return "Could not play music"


def get_news():
    """Fetch news headlines"""
    if not NEWS_API_KEY:
        return "News service not configured. Get free API key from newsapi.org"
    
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data.get('status') == 'ok':
            articles = data.get('articles', [])[:5]
            
            if articles:
                news_text = "Here are top 5 headlines:\n\n"
                for i, article in enumerate(articles, 1):
                    headline = article.get('title', 'No title')
                    news_text += f"{i}. {headline}\n"
                
                return news_text.strip()
            else:
                return "No news found"
        else:
            return "Could not get news"
    
    except:
        return "News service unavailable"


def open_file(command):
    """Open file or folder"""
    try:
        paths = {
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
            "videos": os.path.join(os.path.expanduser("~"), "Videos"),
            "music": os.path.join(os.path.expanduser("~"), "Music")
        }
        
        for folder, path in paths.items():
            if folder in command:
                if os.path.exists(path):
                    confirm = messagebox.askyesno("Confirm", f"Open {folder} folder?")
                    if confirm:
                        os.startfile(path)
                        return f"Opening {folder}"
                    else:
                        return "Cancelled"
                else:
                    return f"{folder} not found"
        
        return "Which file do you want to open?"
    
    except:
        return "Could not open file"


def smart_web_handler(command):
    """Handle web requests"""
    try:
        cmd = command.lower()
        
        # Direct website opening (no confirmation for common sites)
        for site, url in websites.items():
            if site in cmd and "open" in cmd:
                webbrowser.open(url)
                return f"Opening {site}"
        
        # Extract the actual query/site name
        for word in ["open", "go to", "visit", "launch"]:
            cmd = cmd.replace(word, "")
        cmd = cmd.replace("website", "").replace("site", "").strip()
        
        if cmd:
            # Try to open as website
            if "." not in cmd:
                url = f"https://www.{cmd}.com"
            else:
                url = f"https://{cmd}"
            
            confirm = messagebox.askyesno("Confirm", f"Open {cmd}?")
            if confirm:
                webbrowser.open(url)
                return f"Opening {cmd}"
            else:
                return "Cancelled"
        
        return "Could not open website"
    except:
        return "Could not open website"


def open_application(app_name):
    """Open applications"""
    try:
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "explorer": "explorer.exe",
            "file explorer": "explorer.exe",
            "task manager": "taskmgr.exe",
            "cmd": "cmd.exe",
            "command prompt": "cmd.exe",
            "control panel": "control.exe",
            "settings": "ms-settings:"
        }
        
        for app, exe in apps.items():
            if app in app_name.lower():
                confirm = messagebox.askyesno("Confirm", f"Open {app}?")
                if confirm:
                    if exe == "ms-settings:":
                        os.system(f"start {exe}")
                    else:
                        subprocess.Popen(exe, shell=True)
                    return f"Opening {app}"
                else:
                    return "Cancelled"
        
        return None
    except:
        return "Could not open application"


def close_application(app_name):
    """Close applications"""
    try:
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "microsoft edge": "msedge.exe"
        }
        
        for app, exe in apps.items():
            if app in app_name.lower():
                confirm = messagebox.askyesno("Confirm", f"Close {app}?")
                if confirm:
                    os.system(f"taskkill /f /im {exe}")
                    return f"Closing {app}"
                else:
                    return "Cancelled"
        
        return "Application not found or not running"
    except:
        return "Could not close application"


# ============================================
# GROQ AI RESPONSE
# ============================================

def ai_response(prompt):
    """Get AI response using Groq API"""
    
    basic_responses = {
        "hello": "Hello! How can I help you today?",
        "hi": "Hi there! What can I do for you?",
        "hey": "Hey! How can I assist you?",
        "how are you": "I'm doing great! Thanks for asking.",
        "who are you": f"I am {ASSISTANT_NAME}, your AI voice assistant.",
        "what is your name": f"My name is {ASSISTANT_NAME}.",
        "thank you": "You're welcome!",
        "thanks": "You're welcome!",
    }
    
    prompt_lower = prompt.lower().strip()
    for key, response in basic_responses.items():
        if key in prompt_lower:
            return response
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are {ASSISTANT_NAME}, a helpful AI assistant. Give clear, concise answers in 2-3 sentences."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result['choices'][0]['message']['content'].strip()
            return answer
        else:
            return "I'm having trouble connecting to the AI service."
    
    except:
        return "I'm having trouble right now. Please try again."


# ============================================
# COMMAND PROCESSING
# ============================================
def start_listening_for_command(self):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Talon activated! Say your command...\n", "assistant")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, phrase_time_limit=8)
    try:
        command = recognizer.recognize_google(audio)
        self.sendmessage_from_voice(command)
    except sr.UnknownValueError:
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Sorry, I did not understand your command.\n", "assistant")
        self.chat_display.config(state=tk.DISABLED)
    except sr.RequestError:
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "Speech recognition service unavailable.\n", "assistant")
        self.chat_display.config(state=tk.DISABLED)

def sendmessage_from_voice(self, command):
    self.current_session_messages.append({"role": "user", "content": command})
    self.chat_display.config(state=tk.NORMAL)
    self.chat_display.insert(tk.END, f"You said: {command}\n", "user")
    self.chat_display.see(tk.END)
    self.chat_display.config(state=tk.DISABLED)
    threading.Thread(target=self.get_response, args=(command,), daemon=True).start()


def process_command(command):
    """Process commands and return response"""
    if not command:
        return "I didn't catch that. Please try again."
    
    cmd = command.lower()
    
    # System commands - SHUTDOWN, RESTART, SLEEP, LOCK
    if "shutdown" in cmd or "shut down" in cmd:
        return shutdown_computer()
    
    elif "restart" in cmd or "reboot" in cmd:
        return restart_computer()
    
    elif ("sleep" in cmd or "hibernate" in cmd) and ("computer" in cmd or "pc" in cmd or "system" in cmd):
        return sleep_computer()
    
    elif "lock" in cmd and ("computer" in cmd or "pc" in cmd or "system" in cmd):
        return lock_computer()
    
    # Time
    elif "time" in cmd and "what" in cmd:
        return get_time()
    
    # Date
    elif ("date" in cmd or "today" in cmd) and ("what" in cmd or "tell" in cmd):
        return get_date()
    
    # Weather
    elif "weather" in cmd:
        return get_weather(cmd)
    
    # News
    elif "news" in cmd or "headlines" in cmd:
        return get_news()
    
    # Music/Video playback on YouTube - PRIORITY
    elif "play" in cmd:
        return play_music_on_youtube(cmd)
    
    # YouTube search (specific)
    elif "youtube" in cmd and any(word in cmd for word in ["search", "find", "look"]):
        return search_youtube(cmd)
    
    # Google search (explicit)
    elif any(word in cmd for word in ["search", "google", "find", "look up"]) and not "youtube" in cmd:
        return search_google(cmd)
    
    # Close applications
    elif "close" in cmd:
        return close_application(cmd)
    
    # Open files/folders
    elif "open file" in cmd or "open folder" in cmd:
        return open_file(cmd)
    
    # Open websites/apps
    elif any(word in cmd for word in ["open", "go to", "visit", "launch"]):
        result = smart_web_handler(cmd)
        if result and result != "Could not open website":
            return result
        result = open_application(cmd)
        if result:
            return result
        return "Could not find that"
    
    # AI response
    else:
        return ai_response(cmd)


# ============================================
# GUI APPLICATION
# ============================================

class TalonAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Talon - AI Voice Assistant")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2C3E50")
        
        # Store chat sessions
        self.chat_sessions = []
        self.current_session_messages = []
        
        # Load saved history
        self.load_history()
        
        # Mic state
        self.is_listening = False
        self.background_listening = True  # Always-on background mode
        self.listening_thread = None
        
        self.create_widgets()
        
        # Start always-on wake word detection
        threading.Thread(target=self.porcupine_background_listener, daemon=True).start()
        
        # Save history on close
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)
        # Minimize to tray on window minimize
        self.root.bind("<Unmap>", lambda event: self.minimize_to_tray() if self.root.state() == 'iconic' else None)
    
    def minimize_to_tray(self):
        # Load a small PNG for the tray icon (must exist—resize to 32x32px for best results!)
        image = Image.open('Talon_icon.png')
        def on_show(icon, item):
            icon.stop()
            self.root.after(0, self.root.deiconify)
        icon = pystray.Icon(
            "Talon",
            image,
            "Talon AI",
            menu=pystray.Menu(
                pystray.MenuItem("Show Talon", on_show)
            )
        )
        self.root.withdraw()
        icon.run()

    def porcupine_background_listener(self):
        ACCESS_KEY = "/b0jowcqiFtU6dv1mGDIMiLfjQ3XVCZz1aSuledVQMdTkfxIyRga+w=="
        CUSTOM_WAKE_PATH = r"D:\Talon\Talon.ppn"
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[CUSTOM_WAKE_PATH]
        )
        audio = pyaudio.PyAudio()
        stream = audio.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        recognizer = sr.Recognizer()
        try:
            print("Talon always-on background listening started (Porcupine)...")
            while self.background_listening:
                pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
                pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                keyword_index = porcupine.process(pcm)
                if keyword_index >= 0:
                    print("Wake word detected!")
                    # Offload command processing to a separate thread, so listening can resume
                    threading.Thread(target=self.start_listening_for_command, daemon=True).start()
                    # Optionally: add a small sleep delay to prevent duplicate triggers in noisy environments
                    time.sleep(2)  # 2-second cooldown, adjust as needed
        except Exception as e:
            print("Porcupine listener error:", e)
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            porcupine.delete()


    def start_listening_for_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "Talon activated! Say your command...\n", "assistant")
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, phrase_time_limit=8)
        try:
            command = recognizer.recognize_google(audio)
            self.sendmessage_from_voice(command)
        except sr.UnknownValueError:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "Sorry, I did not understand your command.\n", "assistant")
            self.chat_display.config(state=tk.DISABLED)
        except sr.RequestError:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, "Speech recognition service unavailable.\n", "assistant")
            self.chat_display.config(state=tk.DISABLED)

    def sendmessage_from_voice(self, command):
        self.current_session_messages.append({"role": "user", "content": command})
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You said: {command}\n", "user")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        threading.Thread(target=self.get_response, args=(command,), daemon=True).start()

    def continuous_speech_mode(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            if self.root.state() != 'withdrawn':
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.insert(tk.END, "Continuous speech mode: Listening for commands...\n", "assistant")
                self.chat_display.see(tk.END)
                self.chat_display.config(state=tk.DISABLED)
            while True:
                try:
                    audio = recognizer.listen(source, phrase_time_limit=8)
                    command = recognizer.recognize_google(audio)
                    command_lower = command.lower().strip()
                    if command_lower in ["stop listening", "go to sleep", "exit"]:
                        if self.root.state() != 'withdrawn':
                            self.chat_display.config(state=tk.NORMAL)
                            self.chat_display.insert(tk.END, "Exiting continuous speech mode.\n", "assistant")
                            self.chat_display.see(tk.END)
                            self.chat_display.config(state=tk.DISABLED)
                        break
                    self.sendmessage_from_voice(command)
                except sr.UnknownValueError:
                    if self.root.state() != 'withdrawn':
                        self.chat_display.config(state=tk.NORMAL)
                        self.chat_display.insert(tk.END, "Sorry, I did not understand your command.\n", "assistant")
                        self.chat_display.config(state=tk.DISABLED)
                    # Optionally: speak error with TTS if minimized
                except sr.RequestError:
                    if self.root.state() != 'withdrawn':
                        self.chat_display.config(state=tk.NORMAL)
                        self.chat_display.insert(tk.END, "Speech recognition service unavailable.\n", "assistant")
                        self.chat_display.config(state=tk.DISABLED)




        
    def load_history(self):
        """Load chat history from file"""
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r') as f:
                    self.chat_sessions = json.load(f)
                print(f"✅ Loaded {len(self.chat_sessions)} chat sessions")
        except Exception as e:
            print(f"⚠️ Could not load history: {e}")
            self.chat_sessions = []
    
    def save_history(self):
        """Save chat history to file"""
        try:
            with open(HISTORY_FILE, 'w') as f:
                json.dump(self.chat_sessions, f, indent=2)
            print(f"💾 Saved {len(self.chat_sessions)} chat sessions")
        except Exception as e:
            print(f"⚠️ Could not save history: {e}")
    
    def on_closing(self):
        """Handle window close"""
        # Stop background listening
        self.background_listening = False
        
        # Save current session if exists
        if self.current_session_messages:
            first_msg = self.current_session_messages[0]['content']
            title = first_msg[:40] + "..." if len(first_msg) > 40 else first_msg
            
            session = {
                'title': title,
                'messages': self.current_session_messages.copy(),
                'timestamp': datetime.now().strftime("%H:%M")
            }
            self.chat_sessions.append(session)
        
        # Save all history
        self.save_history()
        
        # Close window
        self.root.destroy()
    
    def background_listener(self):
        """Always-on background voice listener"""
        print(f"🎧 Background listening started - Say '{WAKE_WORD}' or any command")
        
        while self.background_listening:
            try:
                # Listen for any voice input
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)
                
                # Recognize
                command = recognizer.recognize_google(audio)
                command_lower = command.lower()
                
                print(f"🎤 Heard: {command}")
                
                # Check if wake word is mentioned
                if WAKE_WORD in command_lower:
                    # Remove wake word from command
                    actual_command = command_lower.replace(WAKE_WORD, "").strip()
                    
                    if actual_command:
                        # Execute the command directly
                        print(f"✅ Executing: {actual_command}")
                        self.root.after(0, lambda cmd=actual_command: self.execute_background_command(cmd))
                    else:
                        # Just wake word, start listening
                        print(f"✅ Wake word detected, ready for command")
                        self.root.after(0, self.start_listening)
                
                # If no wake word but background mode is active, still process commands
                elif len(command.split()) > 2:  # Only process if more than 2 words
                    print(f"📢 Processing background command: {command}")
                    self.root.after(0, lambda cmd=command: self.execute_background_command(cmd))
                
                time.sleep(0.1)  # Small delay
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"Background listener error: {e}")
                time.sleep(1)
    
    def execute_background_command(self, command):
        """Execute command from background listener"""
        # Add to current session
        self.current_session_messages.append({
            'role': 'user',
            'content': command
        })
        
        # Display in chat
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n🎤 Voice Command: {command}\n", "user")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Process command in separate thread
        threading.Thread(target=self.get_response, args=(command,), daemon=True).start()
        
        # Bring window to front and flash
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # ========== TOP BAR ==========
        top_frame = tk.Frame(self.root, bg="#34495E", height=60)
        top_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Logo
        try:
            logo_img = Image.open("Talon_logo.png")
            logo_img = logo_img.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            
            logo_label = tk.Label(top_frame, image=self.logo_photo, bg="#34495E")
            logo_label.pack(side=tk.LEFT, padx=20, pady=5)
            print("✅ Logo loaded successfully!")
        except Exception as e:
            print(f"⚠️ Could not load logo: {e}")
            logo_label = tk.Label(top_frame, text="🤖", font=("Arial", 30), bg="#34495E", fg="white")
            logo_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Menu button
        menu_btn = tk.Menubutton(top_frame, text="☰ Menu", font=("Arial", 12), 
                                 bg="#34495E", fg="white", relief=tk.FLAT, cursor="hand2")
        menu_btn.pack(side=tk.LEFT, padx=10)
        
        menu = tk.Menu(menu_btn, tearoff=0)
        menu_btn.config(menu=menu)
        menu.add_command(label="New Chat", command=self.new_chat_session)
        menu.add_command(label="Toggle Background Mode", command=self.toggle_background_mode)
        menu.add_command(label="Clear All History", command=self.clear_all_history)
        menu.add_command(label="Settings", command=self.show_settings)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.on_closing)
        
        # Title
        title_label = tk.Label(top_frame, text="Talon AI Assistant", 
                              font=("Arial", 18, "bold"), bg="#34495E", fg="white")
        title_label.pack(side=tk.LEFT, padx=20)
        
        # Status indicator
        self.status_label = tk.Label(top_frame, text="🎧 Listening", 
                              font=("Arial", 10, "bold"), bg="#34495E", fg="#2ECC71")
        self.status_label.pack(side=tk.RIGHT, padx=20)
        
        # ========== MAIN CONTAINER ==========
        main_container = tk.Frame(self.root, bg="#2C3E50")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # ========== LEFT SIDEBAR ==========
        sidebar_frame = tk.Frame(main_container, bg="#34495E", width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        sidebar_title = tk.Label(sidebar_frame, text="Previous Chats", 
                                font=("Arial", 12, "bold"), bg="#34495E", fg="white")
        sidebar_title.pack(pady=10)
        
        # Scrollable frame for history with delete buttons
        self.history_canvas = tk.Canvas(sidebar_frame, bg="#2C3E50", highlightthickness=0)
        self.history_scrollbar = tk.Scrollbar(sidebar_frame, orient="vertical", command=self.history_canvas.yview)
        self.history_frame = tk.Frame(self.history_canvas, bg="#2C3E50")
        
        self.history_frame.bind(
            "<Configure>",
            lambda e: self.history_canvas.configure(scrollregion=self.history_canvas.bbox("all"))
        )
        
        self.history_canvas.create_window((0, 0), window=self.history_frame, anchor="nw")
        self.history_canvas.configure(yscrollcommand=self.history_scrollbar.set)
        
        self.history_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.history_scrollbar.pack(side="right", fill="y")
        
        # Update history display
        self.update_history_list()
        
        # ========== MAIN CHAT AREA ==========
        chat_frame = tk.Frame(main_container, bg="#ECF0F1", relief=tk.RAISED, bd=2)
        chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Chat display - READ ONLY, STARTS BLANK
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, font=("Arial", 11), 
            bg="#ECF0F1", fg="#2C3E50", relief=tk.FLAT, bd=0, 
            padx=15, pady=15, state=tk.DISABLED
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure tags
        self.chat_display.tag_config("user", foreground="#2980B9", font=("Arial", 11, "bold"))
        self.chat_display.tag_config("assistant", foreground="#27AE60", font=("Arial", 11))
        
        # ========== BOTTOM INPUT AREA ==========
        input_frame = tk.Frame(self.root, bg="#34495E", height=80)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)
        
        # Text input
        self.input_box = tk.Entry(input_frame, font=("Arial", 12), bg="#2C3E50", 
                                  fg="white", relief=tk.FLAT, bd=5, 
                                  insertbackground="white")
        self.input_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)
        self.input_box.bind("<Return>", lambda e: self.send_message())
        self.input_box.focus()
        
        # Mic button
        self.mic_btn = tk.Button(input_frame, text="🎤", font=("Arial", 20), 
                                bg="#3498DB", fg="white", relief=tk.FLAT, 
                                cursor="hand2", width=3, command=self.toggle_voice_input)
        self.mic_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # File button
        file_btn = tk.Button(input_frame, text="📎", font=("Arial", 20), 
                           bg="#2ECC71", fg="white", relief=tk.FLAT, 
                           cursor="hand2", width=3, command=self.add_file)
        file_btn.pack(side=tk.LEFT, padx=5, pady=10)
    
    def toggle_background_mode(self):
        """Toggle background listening mode"""
        self.background_listening = not self.background_listening
        
        if self.background_listening:
            messagebox.showinfo("Background Mode", "Background listening enabled! Talon will listen even when minimized.")
            threading.Thread(target=self.background_listener, daemon=True).start()
            self.status_label.config(text="🎧 Listening", fg="#2ECC71")
        else:
            messagebox.showinfo("Background Mode", "Background listening disabled.")
            self.status_label.config(text="🔇 Paused", fg="#E74C3C")
    
    def update_history_list(self):
        """Update the chat history sidebar with delete buttons"""
        # Clear existing widgets
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Add sessions in reverse order (newest first)
        for i, session in enumerate(reversed(self.chat_sessions)):
            # Frame for each history item
            item_frame = tk.Frame(self.history_frame, bg="#2C3E50")
            item_frame.pack(fill=tk.X, padx=2, pady=2)
            
            # Delete button (❌)
            delete_btn = tk.Button(
                item_frame, text="❌", font=("Arial", 10), 
                bg="#E74C3C", fg="white", relief=tk.FLAT,
                cursor="hand2", width=2,
                command=lambda idx=len(self.chat_sessions)-1-i: self.delete_chat(idx)
            )
            delete_btn.pack(side=tk.LEFT, padx=2)
            
            # Chat title button
            display_text = f"[{session['timestamp']}] {session['title']}"
            chat_btn = tk.Button(
                item_frame, text=display_text, font=("Arial", 9),
                bg="#2C3E50", fg="white", relief=tk.FLAT,
                cursor="hand2", anchor="w",
                command=lambda idx=len(self.chat_sessions)-1-i: self.load_chat_session_by_index(idx)
            )
            chat_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def delete_chat(self, index):
        """Delete a specific chat session"""
        try:
            confirm = messagebox.askyesno("Delete Chat", "Are you sure you want to delete this chat?")
            if confirm:
                del self.chat_sessions[index]
                self.update_history_list()
                self.save_history()
                print(f"🗑️ Deleted chat at index {index}")
        except Exception as e:
            print(f"Error deleting chat: {e}")
    
    def clear_all_history(self):
        """Clear all chat history"""
        confirm = messagebox.askyesno("Clear History", "Are you sure you want to delete ALL chat history?")
        if confirm:
            self.chat_sessions = []
            self.update_history_list()
            self.save_history()
            messagebox.showinfo("Success", "All chat history cleared!")
    
    def load_chat_session_by_index(self, index):
        """Load a previous chat session by index"""
        try:
            session = self.chat_sessions[index]
            
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            
            for msg in session['messages']:
                if msg['role'] == 'user':
                    self.chat_display.insert(tk.END, f"You: {msg['content']}\n", "user")
                else:
                    self.chat_display.insert(tk.END, f"\n{ASSISTANT_NAME}: {msg['content']}\n\n", "assistant")
            
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error loading chat: {e}")
    
    def new_chat_session(self):
        """Start a new chat session"""
        # Save current session if it has messages
        if self.current_session_messages:
            first_msg = self.current_session_messages[0]['content']
            title = first_msg[:40] + "..." if len(first_msg) > 40 else first_msg
            
            session = {
                'title': title,
                'messages': self.current_session_messages.copy(),
                'timestamp': datetime.now().strftime("%H:%M")
            }
            self.chat_sessions.append(session)
            self.update_history_list()
            self.save_history()
        
        # Start new session
        self.current_session_messages = []
        
        # Clear display
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def toggle_voice_input(self):
        """Toggle voice input on/off"""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()
    
    def start_listening(self):
        """Start manual listening"""
        self.is_listening = True
        self.mic_btn.config(bg="#E74C3C", text="🔴")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\n🎤 Listening... Speak now! (Click mic again to stop)\n", "assistant")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        def listen():
            command = listen_for_command(timeout=30)
            
            if self.is_listening:
                if command:
                    self.current_session_messages.append({
                        'role': 'user',
                        'content': command
                    })
                    
                    self.chat_display.config(state=tk.NORMAL)
                    self.chat_display.delete("end-2l", "end-1l")
                    self.chat_display.insert(tk.END, f"You said: {command}\n", "user")
                    self.chat_display.see(tk.END)
                    self.chat_display.config(state=tk.DISABLED)
                    
                    self.stop_listening()
                    self.get_response(command)
                else:
                    self.stop_listening()
                    self.chat_display.config(state=tk.NORMAL)
                    self.chat_display.delete("end-2l", "end-1l")
                    self.chat_display.insert(tk.END, "\n❌ Could not understand. Please try again.\n\n", "assistant")
                    self.chat_display.see(tk.END)
                    self.chat_display.config(state=tk.DISABLED)
        
        self.listening_thread = threading.Thread(target=listen, daemon=True)
        self.listening_thread.start()
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        self.mic_btn.config(bg="#3498DB", text="🎤")
    
    def send_message(self):
        """Send text message"""
        user_input = self.input_box.get().strip()
        
        if not user_input:
            return
        
        self.current_session_messages.append({
            'role': 'user',
            'content': user_input
        })
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You: {user_input}\n", "user")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        self.input_box.delete(0, tk.END)
        
        threading.Thread(target=self.get_response, args=(user_input,), daemon=True).start()
        
    def get_response(self, user_input):
        """Get response from AI"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{ASSISTANT_NAME}: Thinking...\n", "assistant")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        response = process_command(user_input)
        
        self.current_session_messages.append({
            'role': 'assistant',
            'content': response
        })
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("end-2l", "end-1l")
        self.chat_display.insert(tk.END, f"{ASSISTANT_NAME}: {response}\n\n", "assistant")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        threading.Thread(target=lambda: speak(response), daemon=True).start()
        
    def add_file(self):
        """Add file"""
        filename = filedialog.askopenfilename()
        
        if filename:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"\n📎 File attached: {os.path.basename(filename)}\n\n", "assistant")
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
        
    def show_settings(self):
        """Show settings"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x350")
        settings_window.configure(bg="#34495E")
        
        tk.Label(settings_window, text="⚙️ Settings", font=("Arial", 16, "bold"), 
                bg="#34495E", fg="white").pack(pady=20)
        
        tk.Label(settings_window, text="User Name:", font=("Arial", 12), 
                bg="#34495E", fg="white").pack(pady=5)
        name_entry = tk.Entry(settings_window, font=("Arial", 12))
        name_entry.insert(0, USER_NAME)
        name_entry.pack(pady=5)
        
        tk.Label(settings_window, text="Default City:", font=("Arial", 12), 
                bg="#34495E", fg="white").pack(pady=5)
        city_entry = tk.Entry(settings_window, font=("Arial", 12))
        city_entry.insert(0, DEFAULT_CITY)
        city_entry.pack(pady=5)
        
        def save_settings():
            global USER_NAME, DEFAULT_CITY
            USER_NAME = name_entry.get()
            DEFAULT_CITY = city_entry.get()
            messagebox.showinfo("Settings", "Settings saved!")
            settings_window.destroy()
        
        tk.Button(settings_window, text="💾 Save Settings", font=("Arial", 12), 
                 bg="#2ECC71", fg="white", command=save_settings).pack(pady=20)


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("🚀 Starting Talon AI...\n")
    
    root = tk.Tk()
    app = TalonAI(root)
    
    print("✅ Talon AI is ready!")
    print(f"🎧 Background listening is ACTIVE")
    print(f"💡 Say '{WAKE_WORD}' + command")
    print(f"💡 Or just speak any command (3+ words)\n")
    print("📋 Example Commands:")
    print(f"   • '{WAKE_WORD}, what time is it'")
    print(f"   • '{WAKE_WORD}, play despacito'")
    print(f"   • '{WAKE_WORD}, open youtube'")
    print("   • 'play shape of you' (without wake word)")
    print("   • 'search python programming'\n")
    
    root.mainloop()