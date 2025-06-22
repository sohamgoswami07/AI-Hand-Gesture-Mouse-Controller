Here is the **updated `README.md`** reflecting all the **latest enhancements and gesture features** from the analyzed code:

---

```markdown
# ✋ AI Virtual Mouse Controller using Hand Gestures

Control your computer's mouse using **AI-based hand gesture recognition via webcam**!  
This touchless system combines **MediaPipe**, **OpenCV**, and **PyAutoGUI** to offer a complete virtual mouse experience.

---

## 🚀 Features

- 🎯 **Move Cursor** with index finger
- 🤏 **Left Click** with a thumb-index pinch
- 👆 **Double Click** with two quick pinches
- 🧲 **Drag & Drop** by holding the pinch for 0.25s
- 📜 **Scroll** by touching index + middle fingers and moving
- 👉 **Right Click** by short hold of index + middle fingers
- 🔍 **Zoom In/Out** using thumb + index + middle distance
- 🧭 **Four-Finger Swipes** to:
  - 🔼 Swipe Up: Open Task View (`Win + Tab`)
  - 🔽 Swipe Down: Show Desktop (`Win + D`)
  - ◀️ Swipe Left: Switch to Previous App (`Alt + Shift + Tab`)
  - ▶️ Swipe Right: Switch to Next App (`Alt + Tab`)
- 🧠 Smart state handling (drag, debounce, scroll, zoom, swipe) with live feedback

---

## 📂 Project Structure

```

.
├── AiVirtualMouseProject.py       # Main AI virtual mouse application
├── HandTrackingModule.py          # MediaPipe-based hand and finger detector
├── MouseController.py             # PyAutoGUI-based cursor and mouse event manager
├── requirements.txt               # Required Python libraries
└── README.md                      # You’re reading it!

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
python AiVirtualMouseProject.py
```

---

## 🎮 Gesture Controls

| ✋ Gesture                         | 🖱️ Action             |
| --------------------------------- | ---------------------- |
| Index finger up                   | Move mouse cursor      |
| Thumb + Index pinch               | Left click             |
| Double pinch                      | Double click           |
| Hold pinch (0.25s)                | Drag start / release   |
| Index + Middle fingers (held)     | Activate scroll mode   |
| Index + Middle (short hold)       | Right click            |
| Thumb + Index + Middle (3-finger) | Zoom in/out            |
| 4/5 Finger Swipe Up               | Open Task View         |
| 4/5 Finger Swipe Down             | Show Desktop           |
| 4/5 Finger Swipe Left             | Switch to Previous App |
| 4/5 Finger Swipe Right            | Switch to Next App     |

---

## 💻 Requirements

* Python 3.7+
* Webcam
* OS: Windows / macOS / Linux
* Screen Control Permissions (macOS)
* Well-lit background for optimal detection

---

## 🧪 Dependencies

Key libraries:

* `opencv-python`
* `mediapipe`
* `numpy`
* `pyautogui`

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
Inspired by natural human-computer interaction through computer vision.

---

## ✅ Contribution & Feedback

Want to contribute or suggest a feature?
Reach out on [LinkedIn](https://www.linkedin.com/in/soham-python-developer/), or raise an issue in the repo.

```

---

Let me know if you'd like this saved back into your project folder as an updated `README.md`.
```
