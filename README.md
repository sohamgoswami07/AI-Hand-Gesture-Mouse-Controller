# ✋ AI Virtual Mouse Controller using Hand Gestures

Control your computer's mouse using **AI-based hand gesture recognition via webcam**!  
This touchless system uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to create an intelligent, smooth, and customizable virtual mouse experience.

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
- ⚙️ **Live UI Settings Panel** to control:
  - Visual feedback toggle
  - Gesture smoothening
  - Click sensitivity
  - Scroll sensitivity
  - Zoom threshold
- 🧠 Smart gesture state handling with debounce logic, drag-and-drop memory, scroll state, zoom tracking, and swipe cooldown

---

## 📂 Project Structure

```

.
├── main.py                      # Entry point; initializes webcam & gesture loop
├── config.py                   # Shared config object (thresholds, flags, UI state)
├── ui/
│   └── UiController.py         # Real-time GUI settings window using ttkbootstrap
├── vision/
│   └── HandTrackingModule.py   # MediaPipe-based hand landmark tracker
├── input/
│   └── MouseController.py      # Mouse action wrapper using PyAutoGUI
├── core/
│   ├── gesture\_state.py        # Stores gesture states (drag, pinch, zoom, etc.)
│   ├── gestures.py             # Gesture logic: pinch, scroll, zoom, swipe
│   └── constants.py            # Thresholds and debounce values
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation

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
python -m venv venv_mouse
# Activate:
# On Windows:
venv_mouse\Scripts\activate
# On macOS/Linux:
source venv_mouse/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
cd mouse_controller\
python main.py
```

---

## 🎮 Gesture Controls

| ✋ Gesture                    | 🖱️ Action           |
| ----------------------------- | -------------------- |
| Index finger up               | Move mouse cursor    |
| Thumb + Index pinch           | Left click           |
| Double pinch                  | Double click         |
| Hold pinch (0.25s)            | Drag start / release |
| Index + Middle fingers (held) | Activate scroll mode |
| Index + Middle (short hold)   | Right click          |
| Thumb + Index + Middle        | Zoom in/out          |
| 4-Finger Swipe Up             | Open Task View       |
| 4-Finger Swipe Down           | Show Desktop         |
| 4-Finger Swipe Left           | Previous App         |
| 4-Finger Swipe Right          | Next App             |

---

## ⚙️ Live UI Panel

A built-in settings window will appear with sliders and buttons:

* ✅ Toggle Visual Feedback Window
* 🎚️ Adjust:

  * Smoothening (cursor delay)
  * Click Threshold (pinch sensitivity)
  * Scroll Sensitivity
  * Zoom Sensitivity
* ❌ Stop Button to exit the app

All settings update the app in real-time using a shared `Config` object.

---

## 💻 Requirements

* Python 3.7+
* Webcam
* OS: Windows / macOS / Linux
* Permissions to control keyboard/mouse (on macOS)
* Good lighting and visible hand in webcam

---

## 📦 Dependencies

Install via `requirements.txt`:

```txt
opencv-python
mediapipe
numpy
pyautogui
ttkbootstrap
keyboard
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## 🧠 Internal Modules Breakdown

| Module                  | Responsibility                               |
| ----------------------- | -------------------------------------------- |
| `main.py`               | Captures video, detects gestures, dispatches |
| `HandTrackingModule.py` | Detects hand & fingers using MediaPipe       |
| `MouseController.py`    | Performs mouse actions                       |
| `gesture_state.py`      | Stores gesture states and cooldowns          |
| `gestures.py`           | Gesture logic (scroll, pinch, zoom, swipe)   |
| `constants.py`          | Thresholds and timings for gestures          |
| `UiController.py`       | Live UI to tune gesture parameters           |

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙌 Author

Developed by [Soham Goswami](https://www.linkedin.com/in/soham-python-developer/)
Passionate about building natural user interfaces with computer vision & AI.

---

## ✅ Contribute or Feedback

Found a bug? Want a new gesture?
Open an issue or contact me on [LinkedIn](https://www.linkedin.com/in/soham-python-developer/)

---
