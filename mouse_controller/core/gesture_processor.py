import math
from core.gestures import handle_zoom, handle_scroll, handle_cursor_move, handle_pinch_drag_click, handle_swipe

class GestureProcessor:
    def __init__(self, config, state, screenW, screenH, action_bounds):
        self.config = config
        self.state = state
        self.screenW = screenW
        self.screenH = screenH
        self.action_x1, self.action_x2, self.action_y1, self.action_y2 = action_bounds

    def process(self, fingers, lmList, handedness, current_time, click_threshold):
        handle_zoom(fingers, lmList, self.state, self.config, current_time, handedness)
        handle_scroll(fingers, lmList, self.state, self.config, current_time, click_threshold)
        handle_cursor_move(self.state, fingers, fingers[1] == 1, lmList, self.config,
                           self.screenW, self.screenH,
                           self.action_x1, self.action_x2, self.action_y1, self.action_y2)
        handle_pinch_drag_click(fingers, lmList, self.state, current_time, click_threshold, handedness)
        handle_swipe(fingers, lmList, self.state, current_time)
