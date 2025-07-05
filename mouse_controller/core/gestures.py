import math
import numpy as np
import pyautogui
import keyboard

from core.constants import *
from input.MouseController import move_cursor, click_mouse, double_click, right_click, mouse_press, mouse_release


def handle_zoom(fingers, lmList, state, config, current_time, handedness="Right"):
    if fingers == [1, 1, 1, 0, 0]:
        x_thumb, y_thumb = lmList[4][1:3]
        x_index, y_index = lmList[8][1:3]
        x_middle, y_middle = lmList[12][1:3]
        d1 = math.hypot(x_thumb - x_index, y_thumb - y_index)
        d2 = math.hypot(x_thumb - x_middle, y_thumb - y_middle)
        d3 = math.hypot(x_index - x_middle, y_index - y_middle)
        avg = (d1 + d2 + d3) / 3

        if not state.zoom_active:
            state.last_zoom_distance = avg
            state.zoom_active = True
        else:
            delta = avg - state.last_zoom_distance
            if abs(delta) > config.zoom_threshold_change:
                pyautogui.hotkey('ctrl', '+' if delta > 0 else '-')
                state.last_zoom_distance = avg
    else:
        state.zoom_active = False


def handle_scroll(fingers, lmList, state, config, current_time, click_threshold):
    if fingers[1] and fingers[2]:
        index_middle_dist = math.hypot(lmList[8][1] - lmList[12][1], lmList[8][2] - lmList[12][2])
        if index_middle_dist < click_threshold and sum(fingers) < SWIPE_MIN_FINGERS:
            if not state.fingers_touching:
                state.fingers_touching = True
                state.scroll_start_time = current_time
                state.scroll_anchor_x = lmList[8][1]
                state.scroll_anchor_y = lmList[8][2]
                state.last_scroll_time = current_time
            else:
                if current_time - state.scroll_start_time >= RIGHT_CLICK_HOLD_THRESHOLD:
                    state.scrolling = True
                    dy = state.scroll_anchor_y - lmList[8][2]
                    dx = lmList[8][1] - state.scroll_anchor_x
                    sy = int(dy * config.scroll_sensitivity)
                    sx = int(dx * config.scroll_sensitivity)

                    if current_time - state.last_scroll_time > SCROLL_UPDATE_INTERVAL:
                        if abs(sy) > SCROLL_DEADZONE:
                            pyautogui.scroll(sy * SCROLL_SCALE)
                        if abs(sx) > SCROLL_DEADZONE:
                            pyautogui.hscroll(sx * SCROLL_SCALE)
                        state.last_scroll_time = current_time
            return

    if state.fingers_touching:
        held = current_time - state.scroll_start_time
        if held < RIGHT_CLICK_HOLD_THRESHOLD:
            right_click()
    state.fingers_touching = False
    state.scrolling = False


def handle_cursor_move(state, fingers, index_up, lmList, config, screenW, screenH, action_x1, action_x2, action_y1, action_y2):
    if config.cursor_enabled and ((sum(fingers) == 1 and index_up) or state.dragging) and not state.fingers_touching:
        x_index, y_index = lmList[8][1], lmList[8][2]
        x_index = np.clip(x_index, action_x1, action_x2)
        y_index = np.clip(y_index, action_y1, action_y2)
        x3 = np.interp(x_index, (action_x1, action_x2), (0, screenW))
        y3 = np.interp(y_index, (action_y1, action_y2), (0, screenH))

        alpha = 0.6
        dx = x3 - state.plocX
        dy = y3 - state.plocY

        max_jump = 100
        dx = max(-max_jump, min(max_jump, dx))
        dy = max(-max_jump, min(max_jump, dy))

        state.clocX = state.plocX + dx * alpha
        state.clocY = state.plocY + dy * alpha

        move_cursor(screenW, screenH, state.clocX, state.clocY)
        state.plocX, state.plocY = state.clocX, state.clocY


def handle_pinch_drag_click(fingers, lmList, state, current_time, click_threshold, handedness="Right"):
    index_up = fingers[1]
    thumb_up = fingers[0]
    middle_up = fingers[2]

    # Use consistent landmark indices for tip positions
    x_index, y_index = lmList[8][1:3]
    x_thumb, y_thumb = lmList[4][1:3]
    index_thumb_dist = math.hypot(x_index - x_thumb, y_index - y_thumb)

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

    if state.pinch_active and not state.dragging:
        held = current_time - state.pinch_start_time
        if held >= DRAG_HOLD_THRESHOLD and index_thumb_dist < click_threshold:
            mouse_press()
            state.dragging = True


def handle_swipe(fingers, lmList, state, current_time):
    if sum(fingers) >= SWIPE_MIN_FINGERS:
        tip_ids = [8, 12, 16, 20]
        avg_x = sum(lmList[id][1] for id in tip_ids) / 4
        avg_y = sum(lmList[id][2] for id in tip_ids) / 4

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
