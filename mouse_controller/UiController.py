import tkinter as tk
from config import config

def start_ui():
    root = tk.Tk()
    root.title("Virtual Mouse Settings")
    root.geometry("400x300")

    tk.Checkbutton(
        root, text="Enable Cursor Movement",
        variable=tk.BooleanVar(value=config.cursor_enabled),
        command=lambda: setattr(config, "cursor_enabled", not config.cursor_enabled)
    ).pack(pady=10)

    def slider(label, attr, frm, to, res):
        tk.Label(root, text=label).pack()
        tk.Scale(root, from_=frm, to=to, resolution=res, orient=tk.HORIZONTAL,
                 command=lambda val: setattr(config, attr, float(val))).pack()

    slider("Smoothening", "smoothening", 1, 20, 1)
    slider("Click Threshold Ratio", "click_threshold_ratio", 0.05, 0.3, 0.01)
    slider("Scroll Sensitivity", "scroll_sensitivity", 0.5, 5.0, 0.1)
    slider("Zoom Threshold Change", "zoom_threshold_change", 1, 50, 1)

    root.mainloop()
