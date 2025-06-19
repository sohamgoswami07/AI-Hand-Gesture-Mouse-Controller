import cv2
import numpy as np
import time
import math
import HandTrackingModule as htm
import MouseController as mc
import pyautogui

# === Constants ===
SMOOTHENING = 5
CLICK_THRESHOLD_RATIO = 0.10
PINCH_RELEASE_BUFFER = 5
PINCH_DEBOUNCE = 0.15
DOUBLE_CLICK_GAP = 0.5
DRAG_HOLD_THRESHOLD = 0.25
RIGHT_CLICK_HOLD_THRESHOLD = 0.25
SCROLL_SENSITIVITY = 1.8
SCROLL_SCALE = 3
SCROLL_UPDATE_INTERVAL = 0.01
SCROLL_DEADZONE = 2

ZOOM_THRESHOLD_CHANGE = 15
ZOOM_MIN_DISTANCE = 30
ZOOM_MAX_DISTANCE = 300

SWIPE_MIN_FINGERS = 4
SWIPE_DEBOUNCE_TIME = 1.0
SWIPE_THRESHOLD = 100

# === Camera Setup ===
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
wCam, hCam = int(cap.get(3)), int(cap.get(4))
click_threshold = int(min(wCam, hCam) * CLICK_THRESHOLD_RATIO)
screenW, screenH = pyautogui.size()

# === State Variables ===
plocX, plocY = 0, 0
clocX, clocY = 0, 0

pinch_active = False
pinch_start_time = 0
last_pinch_time = 0
pinch_count = 0

dragging = False
fingers_touching = False
scrolling = False
scroll_start_time = 0
scroll_anchor_y = 0
scroll_anchor_x = 0
last_scroll_time = 0

zoom_active = False
last_zoom_distance = 0

last_swipe_time = 0
swipe_start_pos = None
swipe_direction_triggered = False

# === Hand Detector ===
detector = htm.handDetector(detectionCon=0.7, trackCon=0.7)

while True:
    success, img = cap.read()
    if not success:
        print("Camera frame not captured.")
        continue

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

        # === Zoom In/Out Detection
        if thumb_up and index_up and middle_up:
            dist_thumb_index = math.hypot(x_thumb - x_index, y_thumb - y_index)
            dist_thumb_middle = math.hypot(x_thumb - x_middle, y_thumb - y_middle)
            dist_index_middle = math.hypot(x_index - x_middle, y_index - y_middle)

            current_zoom_distance = (dist_thumb_index + dist_thumb_middle + dist_index_middle) / 3

            if not zoom_active:
                last_zoom_distance = current_zoom_distance
                zoom_active = True
            else:
                distance_change = current_zoom_distance - last_zoom_distance
                if abs(distance_change) > ZOOM_THRESHOLD_CHANGE:
                    if distance_change > 0:
                        print("Zooming In")
                        pyautogui.hotkey('ctrl', '+')
                    else:
                        print("Zooming Out")
                        pyautogui.hotkey('ctrl', '-')
                    last_zoom_distance = current_zoom_distance
        else:
            zoom_active = False

        # === Smart Scroll + Right Click
        if index_up and middle_up and index_middle_dist < click_threshold:
            if not fingers_touching:
                fingers_touching = True
                scroll_start_time = current_time
                scroll_anchor_y = y_index
                scroll_anchor_x = x_index
                last_scroll_time = current_time
            else:
                held_duration = current_time - scroll_start_time
                if held_duration >= RIGHT_CLICK_HOLD_THRESHOLD:
                    scrolling = True
                    dy = scroll_anchor_y - y_index
                    dx = x_index - scroll_anchor_x

                    scroll_speed_y = int(dy * SCROLL_SENSITIVITY)
                    scroll_speed_x = int(dx * SCROLL_SENSITIVITY)

                    if current_time - last_scroll_time > SCROLL_UPDATE_INTERVAL:
                        if abs(scroll_speed_y) > SCROLL_DEADZONE:
                            pyautogui.scroll(scroll_speed_y * SCROLL_SCALE)
                        if abs(scroll_speed_x) > SCROLL_DEADZONE:
                            pyautogui.hscroll(scroll_speed_x * SCROLL_SCALE)

                        last_scroll_time = current_time
        else:
            if fingers_touching:
                held_duration = current_time - scroll_start_time
                if held_duration < RIGHT_CLICK_HOLD_THRESHOLD:
                    print("Right Click")
                    mc.right_click()

            fingers_touching = False
            scrolling = False

        # === Cursor Movement
        if ((fingers.count(1) == 1 and index_up) or dragging) and not fingers_touching:
            x3 = np.interp(x_index, (0, wCam), (0, screenW))
            y3 = np.interp(y_index, (0, hCam), (0, screenH))
            clocX = plocX + (x3 - plocX) / SMOOTHENING
            clocY = plocY + (y3 - plocY) / SMOOTHENING
            mc.move_cursor(screenW, screenH, clocX, clocY)
            plocX, plocY = clocX, clocY

        # === Pinch Detection
        if index_up and thumb_up and not middle_up:
            if index_thumb_dist < click_threshold:
                if not pinch_active:
                    pinch_active = True
                    pinch_start_time = current_time
                    if current_time - last_pinch_time < DOUBLE_CLICK_GAP:
                        pinch_count += 1
                    else:
                        pinch_count = 1
                    last_pinch_time = current_time
            else:
                if pinch_active:
                    pinch_active = False
                    pinch_duration = current_time - pinch_start_time

                    if dragging:
                        print("Drag Released")
                        mc.mouse_release()
                        dragging = False
                        pinch_count = 0
                    elif pinch_count == 1 and pinch_duration < DRAG_HOLD_THRESHOLD:
                        print("Single Click")
                        mc.click_mouse()
                    elif pinch_count == 2 and pinch_duration < DRAG_HOLD_THRESHOLD:
                        print("Double Click")
                        mc.double_click()
                        pinch_count = 0
        else:
            if pinch_active:
                pinch_active = False
                if dragging:
                    print("Drag Released")
                    mc.mouse_release()
                    dragging = False
                    pinch_count = 0
            if current_time - last_pinch_time > DOUBLE_CLICK_GAP:
                pinch_count = 0

        # === Drag Start
        if pinch_active and not dragging:
            pinch_duration = current_time - pinch_start_time
            if pinch_duration >= DRAG_HOLD_THRESHOLD and index_thumb_dist < click_threshold:
                print("Drag Start")
                mc.mouse_press()
                dragging = True

        # === Improved Four/Five-Finger Swipe Detection ===
        if fingers.count(1) >= SWIPE_MIN_FINGERS:
            tip_ids = [8, 12, 16, 20]
            x_vals = [lmList[id][1] for id in tip_ids]
            y_vals = [lmList[id][2] for id in tip_ids]
            avg_x = sum(x_vals) / len(x_vals)
            avg_y = sum(y_vals) / len(y_vals)

            if not swipe_start_pos:
                swipe_start_pos = (avg_x, avg_y)
                swipe_direction_triggered = False
            else:
                dx = avg_x - swipe_start_pos[0]
                dy = avg_y - swipe_start_pos[1]

                if not swipe_direction_triggered and current_time - last_swipe_time > SWIPE_DEBOUNCE_TIME:
                    if abs(dy) > SWIPE_THRESHOLD and abs(dy) > abs(dx):
                        if dy < 0:
                            print("Swipe Up: Task View")
                            pyautogui.hotkey('win', 'tab')
                        else:
                            print("Swipe Down: Show Desktop")
                            pyautogui.hotkey('win', 'd')
                        swipe_direction_triggered = True
                        last_swipe_time = current_time
                    elif abs(dx) > SWIPE_THRESHOLD and abs(dx) > abs(dy):
                        if dx < 0:
                            print("Swipe Left: Previous App")
                            pyautogui.hotkey('alt', 'shift', 'tab')
                        else:
                            print("Swipe Right: Next App")
                            pyautogui.hotkey('alt', 'tab')
                        swipe_direction_triggered = True
                        last_swipe_time = current_time
        else:
            swipe_start_pos = None
            swipe_direction_triggered = False

        # === Draw Fingertip Circles
        for i, isUp in enumerate(fingers):
            if isUp:
                tip_id = detector.tipIds[i]
                cx, cy = lmList[tip_id][1], lmList[tip_id][2]
                cv2.circle(img, (cx, cy), 12, (255, 255, 255), 2)

        # === Visual Feedback
        if scrolling:
            cv2.putText(img, "Scrolling...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        elif fingers_touching:
            cv2.putText(img, "Touching (No Movement)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
        elif dragging:
            cv2.putText(img, "Dragging...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        elif pinch_active:
            cv2.putText(img, "Clicking...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif zoom_active:
            cv2.putText(img, "Zooming...", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        elif fingers.count(1) >= SWIPE_MIN_FINGERS and swipe_start_pos:
            cv2.putText(img, "Swipe Detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 128, 255), 2)

    # === Display Window
    cv2.imshow("AI Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
