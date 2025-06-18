# ✋ AI Virtual Mouse Controller using Hand Gestures

Control your computer's mouse with your **hand gestures via webcam**! This project uses **MediaPipe** and **OpenCV** to detect hand landmarks and translates them into mouse operations like moving the cursor, clicking, dragging, right-clicking, and even scrolling—completely touch-free!

---

## 🚀 Features

- 🎯 **Cursor Control** with your index finger
- 🤏 **Click** with a pinch (thumb + index)
- 🖱️ **Double Click** with a quick double pinch
- 🧲 **Drag & Drop** by holding the pinch
- 📜 **Scroll** by touching index + middle fingers and moving vertically or horizontally
- 👉 **Right Click** by short touch of index + middle fingers
- 🧠 Smart debounce, drag, and scroll logic with visual feedback

---

## 📂 Project Structure

```

<pre> 📁 <b>Project Root</b> ├── 📁 <b>mouse_controller</b> │ ├── 🧠 <b>AiVirtualMouseProject.py</b> # Main application logic │ ├── ✋ <b>HandTrackingModule.py</b> # Detects hands and gestures via MediaPipe │ └── 🖱️ <b>MouseController.py</b> # Wrapper for PyAutoGUI mouse actions ├── 📄 <b>requirements.txt</b> # List of Python packages ├── 📄 <b>.gitignore</b> # Ignore virtualenv, pycache, etc. └── 📄 <b>README.md</b> # This file! </pre>

````

---

## 🛠 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sohamgoswami07/AI-Hand-Gesture-Mouse-Controller.git
cd AI-Hand-Gesture-Mouse-Controller
````

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv_mouse_controller
# Activate it:
# Windows:
venv_mouse_controller\Scripts\activate
# macOS/Linux:
source venv_mouse_controller/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
cd mouse_controller\
python AiVirtualMouseProject.py
```

---

## 🎮 Gesture Controls

| ✋ Gesture                   | 🖱️ Action         |
| ---------------------------- | ------------------ |
| Index finger up              | Move mouse cursor  |
| Thumb + Index pinch          | Left click         |
| Double pinch                 | Double click       |
| Hold pinch                   | Drag and drop      |
| Index + Middle fingers held  | Scroll mode        |
| Short touch (Index + Middle) | Right click        |

---

## 💻 Requirements

* Python 3.7+
* Webcam
* OS: Windows / macOS / Linux
* Screen Control Permissions (for macOS users)
* Well-lit environment for optimal tracking

---

## 🧪 Dependencies

Key libraries used (full list in `requirements.txt`):

* `opencv-python`
* `mediapipe`
* `pyautogui`
* `numpy`
* `autopy`

Install all via:

```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is open-source under the **MIT License**.

---

## 🙌 Author

Developed by - [Soham Goswami](https://www.linkedin.com/in/soham-python-developer/)  
Inspired by gesture-based interfaces and the power of AI in human-computer interaction.

---

## ✅ Changes You Should Make

* Feel free to connect through [LinkedIn](https://www.linkedin.com/in/soham-python-developer/) for project feedback or collaborations
