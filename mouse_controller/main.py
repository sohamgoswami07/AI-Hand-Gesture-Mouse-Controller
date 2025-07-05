import cv2
import numpy as np
import time
import math
import threading
import pyautogui
import keyboard
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from config import config
from ui.UiController import start_ui
from vision.HandTrackingModule import handDetector
from input.MouseController import move_cursor, click_mouse, double_click, right_click, mouse_press, mouse_release
from core.gesture_state import GestureState
from core.constants import *
from core.gestures import handle_zoom, handle_scroll, handle_cursor_move, handle_pinch_drag_click, handle_swipe

# === Launch UI in Background Thread ===
threading.Thread(target=start_ui, daemon=True).start()

# === Camera Setup ===
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)

wCam, hCam = int(cap.get(3)), int(cap.get(4))
screenW, screenH = pyautogui.size()

# === Action Area Definition ===
action_margin_x = int(wCam * 0.2)
action_margin_y = int(hCam * 0.2)
action_x1, action_y1 = action_margin_x, action_margin_y
action_x2, action_y2 = wCam - action_margin_x, hCam - action_margin_y

# === Hand Detector ===
detector = handDetector(detectionCon=0.7, trackCon=0.7)
state = GestureState()
window_open = False

while True:
    success, img = cap.read()
    if not success:
        continue

    SMOOTHENING = config.smoothening
    CLICK_THRESHOLD_RATIO = config.click_threshold_ratio
    click_threshold = int(min(wCam, hCam) * CLICK_THRESHOLD_RATIO)
    SCROLL_SENSITIVITY = config.scroll_sensitivity
    ZOOM_THRESHOLD_CHANGE = config.zoom_threshold_change

    img = cv2.flip(img, 1)
    img = detector.findHands(img, draw=False)
    lmList, _ = detector.findPosition(img, draw=False)
    handedness = detector.getHandedness() or "Right"
    current_time = time.time()

    # Display handedness on screen
    cv2.putText(img, f"Hand: {handedness}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 100), 2)

    if lmList:
        fingers = detector.fingersUp(handedness)

        index_up = fingers[1] == 1
        thumb_up = fingers[0] == 1
        middle_up = fingers[2] == 1

        x_index, y_index = lmList[8][1], lmList[8][2]
        x_thumb, y_thumb = lmList[4][1], lmList[4][2]
        x_middle, y_middle = lmList[12][1], lmList[12][2]

        index_thumb_dist = math.hypot(x_index - x_thumb, y_index - y_thumb)
        index_middle_dist = math.hypot(x_index - x_middle, y_index - y_middle)

        # Gesture Handling (handedness passed into zoom)
        handle_zoom(fingers, lmList, state, config, current_time, handedness)
        handle_scroll(fingers, lmList, state, config, current_time, click_threshold)
        handle_cursor_move(state, fingers, index_up, lmList, config, screenW, screenH,
                           action_x1, action_x2, action_y1, action_y2)
        handle_pinch_drag_click(fingers, lmList, state, current_time, click_threshold, handedness)
        handle_swipe(fingers, lmList, state, current_time)

        # Draw fingertip feedback
        circle_color = (255, 255, 255)
        circle_thickness = 2
        circle_radius = 10
        active_action = state.pinch_active or state.dragging or state.fingers_touching or state.scrolling
        tip_ids = [4, 8, 12, 16, 20]

        for i, finger_up in enumerate(fingers):
            if finger_up:
                tip_id = tip_ids[i]
                if tip_id < len(lmList):
                    x, y = lmList[tip_id][1], lmList[tip_id][2]
                    if active_action:
                        cv2.circle(img, (x, y), circle_radius, circle_color, -1)
                    else:
                        cv2.circle(img, (x, y), circle_radius, circle_color, circle_thickness)

    cv2.rectangle(img, (action_x1, action_y1), (action_x2, action_y2), (0, 255, 0), 1)

    if config.visual_feedback_enabled:
        if not window_open:
            window_open = True
        cv2.imshow("AI Virtual Mouse", img)
    else:
        if window_open:
            cv2.destroyWindow("AI Virtual Mouse")
            window_open = False

    if config.shutdown_requested or (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
