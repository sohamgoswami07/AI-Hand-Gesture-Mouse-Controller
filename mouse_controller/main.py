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
cap.set(3, 320)
cap.set(4, 240)

wCam, hCam = int(cap.get(3)), int(cap.get(4))
screenW, screenH = pyautogui.size()

# === Action Area Definition ===
action_margin_x = int(wCam * 0.1)
action_margin_y = int(hCam * 0.1)
action_x1, action_y1 = action_margin_x, action_margin_y
action_x2, action_y2 = wCam - action_margin_x, hCam - action_margin_y

# === Hand Detector ===
detector = handDetector(detectionCon=0.7, trackCon=0.7)

# === State Class ===
class GestureState:
    def __init__(self):
        self.plocX = 0
        self.plocY = 0
        self.clocX = 0
        self.pinch_active = False
        self.pinch_start_time = 0
        self.last_pinch_time = 0
        self.pinch_count = 0
        self.dragging = False
        self.fingers_touching = False
        self.scrolling = False
        self.scroll_start_time = 0
        self.scroll_anchor_y = 0
        self.scroll_anchor_x = 0
        self.last_scroll_time = 0
        self.zoom_active = False
        self.last_zoom_distance = 0
        self.last_swipe_time = 0
        self.swipe_start_pos = None
        self.swipe_direction_triggered = False

state = GestureState()

# === Gesture Thresholds ===
PINCH_DEBOUNCE = 0.15
DOUBLE_CLICK_GAP = 0.5
DRAG_HOLD_THRESHOLD = 0.25
RIGHT_CLICK_HOLD_THRESHOLD = 0.25
SCROLL_SCALE = 3
SCROLL_UPDATE_INTERVAL = 0.01
SCROLL_DEADZONE = 2
SWIPE_MIN_FINGERS = 4
SWIPE_DEBOUNCE_TIME = 1.0
SWIPE_THRESHOLD = 40

# === Main Loop ===
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
    current_time = time.time()

    if lmList:
        fingers = detector.fingersUp()
        x_index, y_index = lmList[8][1], lmList[8][2]
        x_thumb, y_thumb = lmList[4][1], lmList[4][2]
        x_middle, y_middle = lmList[12][1], lmList[12][2]

        index_up = fingers[1] == 1
        thumb_up = fingers[0] == 1
        middle_up = fingers[2] == 1

        index_thumb_dist = math.hypot(x_index - x_thumb, y_index - y_thumb)
        index_middle_dist = math.hypot(x_index - x_middle, y_index - y_middle)

        finger_count = fingers.count(1)

        # === Zoom ===
        if thumb_up and index_up and middle_up and finger_count == 3:
            d1 = math.hypot(x_thumb - x_index, y_thumb - y_index)
            d2 = math.hypot(x_thumb - x_middle, y_thumb - y_middle)
            d3 = math.hypot(x_index - x_middle, y_index - y_middle)
            avg_distance = (d1 + d2 + d3) / 3

            if not state.zoom_active:
                state.last_zoom_distance = avg_distance
                state.zoom_active = True
            else:
                delta = avg_distance - state.last_zoom_distance
                if abs(delta) > ZOOM_THRESHOLD_CHANGE:
                    pyautogui.hotkey('ctrl', '+' if delta > 0 else '-')
                    state.last_zoom_distance = avg_distance
        else:
            state.zoom_active = False

        # === Scroll + Right Click ===
        if index_up and middle_up and index_middle_dist < click_threshold and finger_count < SWIPE_MIN_FINGERS:
            if not state.fingers_touching:
                state.fingers_touching = True
                state.scroll_start_time = current_time
                state.scroll_anchor_y = y_index
                state.scroll_anchor_x = x_index
                state.last_scroll_time = current_time
            else:
                held = current_time - state.scroll_start_time
                if held >= RIGHT_CLICK_HOLD_THRESHOLD:
                    state.scrolling = True
                    dy = state.scroll_anchor_y - y_index
                    dx = x_index - state.scroll_anchor_x
                    sy = int(dy * SCROLL_SENSITIVITY)
                    sx = int(dx * SCROLL_SENSITIVITY)
                    if current_time - state.last_scroll_time > SCROLL_UPDATE_INTERVAL:
                        if abs(sy) > SCROLL_DEADZONE:
                            pyautogui.scroll(sy * SCROLL_SCALE)
                        if abs(sx) > SCROLL_DEADZONE:
                            pyautogui.hscroll(sx * SCROLL_SCALE)
                        state.last_scroll_time = current_time
        else:
            if state.fingers_touching:
                held = current_time - state.scroll_start_time
                if held < RIGHT_CLICK_HOLD_THRESHOLD:
                    right_click()
            state.fingers_touching = False
            state.scrolling = False

        # === Cursor Movement ===
        if config.cursor_enabled and ((finger_count == 1 and index_up) or state.dragging) and not state.fingers_touching:
            x_index = np.clip(x_index, action_x1, action_x2)
            y_index = np.clip(y_index, action_y1, action_y2)
            x3 = np.interp(x_index, (action_x1, action_x2), (0, screenW))
            y3 = np.interp(y_index, (action_y1, action_y2), (0, screenH))
            state.clocX = state.plocX + (x3 - state.plocX) / SMOOTHENING
            state.clocY = state.plocY + (y3 - state.plocY) / SMOOTHENING
            move_cursor(screenW, screenH, state.clocX, state.clocY)
            state.plocX, state.plocY = state.clocX, state.clocY

        # === Pinch / Drag / Click ===
        if index_up and thumb_up and not middle_up:
            if index_thumb_dist < click_threshold:
                if not state.pinch_active:
                    state.pinch_active = True
                    state.pinch_start_time = current_time
                    if current_time - state.last_pinch_time < DOUBLE_CLICK_GAP:
                        state.pinch_count += 1
                    else:
                        state.pinch_count = 1
                    state.last_pinch_time = current_time
            else:
                if state.pinch_active:
                    state.pinch_active = False
                    held = current_time - state.pinch_start_time
                    if state.dragging:
                        mouse_release()
                        state.dragging = False
                        state.pinch_count = 0
                    elif state.pinch_count == 1 and held < DRAG_HOLD_THRESHOLD:
                        click_mouse()
                    elif state.pinch_count == 2 and held < DRAG_HOLD_THRESHOLD:
                        double_click()
                        state.pinch_count = 0
        else:
            if state.pinch_active:
                state.pinch_active = False
                if state.dragging:
                    mouse_release()
                    state.dragging = False
                    state.pinch_count = 0
            if current_time - state.last_pinch_time > DOUBLE_CLICK_GAP:
                state.pinch_count = 0

        # === Drag Start ===
        if state.pinch_active and not state.dragging:
            held = current_time - state.pinch_start_time
            if held >= DRAG_HOLD_THRESHOLD and index_thumb_dist < click_threshold:
                mouse_press()
                state.dragging = True

        # === Swipe Detection ===
        if finger_count >= SWIPE_MIN_FINGERS:
            tip_ids = [8, 12, 16, 20]
            avg_x = sum([lmList[id][1] for id in tip_ids]) / 4
            avg_y = sum([lmList[id][2] for id in tip_ids]) / 4
            if not state.swipe_start_pos:
                state.swipe_start_pos = (avg_x, avg_y)
                state.swipe_direction_triggered = False
            else:
                dx = avg_x - state.swipe_start_pos[0]
                dy = avg_y - state.swipe_start_pos[1]
                if not state.swipe_direction_triggered and current_time - state.last_swipe_time > SWIPE_DEBOUNCE_TIME:
                    if abs(dy) > SWIPE_THRESHOLD and abs(dy) > abs(dx):
                        keyboard.press_and_release('windows+tab' if dy < 0 else 'windows+d')
                    elif abs(dx) > SWIPE_THRESHOLD:
                        keyboard.press_and_release('alt+shift+tab' if dx < 0 else 'alt+tab')
                    state.swipe_direction_triggered = True
                    state.last_swipe_time = current_time
        else:
            state.swipe_start_pos = None
            state.swipe_direction_triggered = False

    # === Visual Feedback ===
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
