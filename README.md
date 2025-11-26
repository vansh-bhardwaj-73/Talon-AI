

# 🦅 Talon – AI Voice Assistant

Talon is a **Python-based AI Voice Assistant** with a GUI interface, wake-word activation, AI-powered conversation, system control, web browsing, and media playback. It listens to your commands via voice or text and responds intelligently.

---

## 🚀 Features

### 🎤 Voice Interaction

* Hotword detection with **Porcupine** (`"hey Talon"`)
* Continuous background listening
* Manual mic input mode via **🎤 button**
* Voice recognition using **SpeechRecognition + Google API**
* Natural text-to-speech using **pyttsx3**

---

### 🧠 AI Capabilities

* Conversational AI powered by **Groq LLM API**
* Answers general knowledge questions, explains concepts, solves problems
* Basic predefined responses for greetings, thank yous, and introductions
* Example queries:

  * “What is machine learning?”
  * “Explain Python in 2 sentences”
  * “Who are you?”

---

### 🌐 Web and Media

* Open websites (`youtube`, `google`, `facebook`, `github`, etc.)
* Google searches and YouTube searches/playback
* Play music or videos directly on YouTube
* Top 5 news headlines (via NewsAPI)
* Weather reports (via OpenWeatherMap API)

---

### 🖥️ System Controls

* Shutdown, restart, sleep, lock computer with confirmation dialogs
* Open/close applications: Notepad, Chrome, Edge, Calculator, Paint, File Explorer, Task Manager
* Open standard folders: Downloads, Documents, Desktop, Pictures, Videos, Music

---

### 📂 File Handling

* Attach files in chat using **📎 button**
* Manage previous chat sessions via GUI sidebar
* Save and load chat history in JSON format

---

### 🖱️ GUI Interface

* Built with **Tkinter**
* **Top bar**: Logo, menu, status indicator
* **Chat area**: Scrollable, color-coded user/assistant messages
* **Sidebar**: Chat history with load/delete functionality
* **Bottom input**: Text entry + mic button + file attachment

---

### 🔧 Settings

* Change **User Name**
* Change **Default City** for weather reports

---

### ⚡ Additional Features

* Always-on background listening even when minimized
* Minimizes to **system tray** using **pystray**
* Handles errors gracefully (speech recognition, API failures)
* Fast, threaded response handling for smooth performance

---

## 📂 Project Structure

```
Talon/
│
├── Talon.py                  # Main application
├── Talon_logo.png            # GUI logo
├── Talon_icon.png            # Tray icon
├── Talon.ppn                 # Custom wake-word model
├── Talon_chat_history.json   # Saved chat sessions
└── requirements.txt          # Python dependencies
```

---

## 🔧 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/vansh-bhardwaj-73/Talon.git
cd Talon
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

Activate it:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

If `pyaudio` fails on Windows:

```bash
pip install pipwin
pipwin install pyaudio
```

### 4️⃣ Add API Keys

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
NEWS_API_KEY=your_news_api_key
WEATHER_API_KEY=your_weather_api_key
```

---

## ▶️ Running Talon

```bash
python main.py
```

* Say `"hey Talon"` to wake the assistant
* Speak or type commands in the GUI
* Use buttons to attach files, toggle mic input, or manage settings

**Example Commands**:

* `"hey Talon, what time is it?"`
* `"play Despacito"`
* `"open youtube"`
* `"search python programming"`
* `"shutdown computer"`

---

## 🧠 Technologies Used

| Feature             | Library/Tool         |
| ------------------- | -------------------- |
| GUI                 | Tkinter              |
| Speech Recognition  | SpeechRecognition    |
| Text-to-Speech      | pyttsx3              |
| Wake Word Detection | Porcupine, pyaudio   |
| Tray Icon           | pystray              |
| AI Responses        | Groq LLM API         |
| Web/Networking      | requests, webbrowser |
| Image Handling      | PIL / Pillow         |
| File Handling       | os, filedialog       |

---

## 📝 License

Open-source. Free to use and modify.


