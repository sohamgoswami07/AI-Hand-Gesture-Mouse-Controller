import ttkbootstrap as tb
from ttkbootstrap.constants import *
from config import config

def start_ui():
    root = tb.Window(themename="flatly")  # Available Themes: cosmo, flatly, minty, cyborg, journal
    root.title("Virtual Mouse Settings")
    root.geometry("450x450")

    feedback_var = tb.BooleanVar(value=config.visual_feedback_enabled)

    def toggle_feedback():
        config.visual_feedback_enabled = feedback_var.get()

    def stop_program():
        config.shutdown_requested = True
        root.quit()
        root.destroy()

    # Toggle Button
    tb.Checkbutton(root, text="Enable Camera Visual Feedback", variable=feedback_var, command=toggle_feedback).pack(pady=10)

    # Stop Button
    tb.Button(root, text="Stop Program", bootstyle="danger", command=stop_program).pack(pady=20)

    def slider(label, attr, frm, to, res):
        tb.Label(root, text=label).pack()
        tb.Scale(root, from_=frm, to=to, orient='horizontal', length=300,
                 command=lambda val: setattr(config, attr, float(val))).pack(pady=5)

    slider("Smoothening", "smoothening", 1, 20, 1)
    slider("Click Threshold Ratio", "click_threshold_ratio", 0.05, 0.3, 0.01)
    slider("Scroll Sensitivity", "scroll_sensitivity", 0.5, 5.0, 0.1)
    slider("Zoom Threshold Change", "zoom_threshold_change", 1, 50, 1)

    root.mainloop()
