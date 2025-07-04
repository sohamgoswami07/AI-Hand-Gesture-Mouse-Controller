class Config:
    def __init__(self):
        self.cursor_enabled = True
        self.visual_feedback_enabled = True
        self.shutdown_requested = False
        self.smoothening = 2
        self.click_threshold_ratio = 0.10
        self.scroll_sensitivity = 1.8
        self.zoom_threshold_change = 15

config = Config()
