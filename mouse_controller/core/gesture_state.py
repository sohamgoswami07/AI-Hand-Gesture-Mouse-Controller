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
