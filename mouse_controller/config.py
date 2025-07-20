# mouse_controller/config.py
import threading

class Config:
    def __init__(self):
        self._lock = threading.Lock()
        self.cursor_enabled = True
        self.visual_feedback_enabled = True
        self.shutdown_requested = False
        self.smoothening = 2
        self.click_threshold_ratio = 0.10
        self.scroll_sensitivity = 1.8
        self.zoom_threshold_change = 15

    def set(self, key, value):
        with self._lock:
            setattr(self, key, value)

    def get(self, key):
        with self._lock:
            return getattr(self, key)

config = Config()
