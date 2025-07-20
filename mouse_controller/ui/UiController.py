import ttkbootstrap as tb
from ttkbootstrap.constants import *
from config import config

def start_ui():
    root = tb.Window(themename="flatly")
    root.title("Virtual Mouse Settings")
    root.geometry("600x520")

    feedback_var = tb.BooleanVar(value=config.visual_feedback_enabled)
    profile_var = tb.StringVar(value="Precise")

    sliders = {}

    # MODE PROFILES with saved values
    mode_values = {
        "Fast": {
            "smoothening": 3,
            "click_threshold_ratio": 0.07,
            "scroll_sensitivity": 4.5,
            "zoom_threshold_change": 10,
        },
        "Precise": {
            "smoothening": 7,
            "click_threshold_ratio": 0.10,
            "scroll_sensitivity": 2.0,
            "zoom_threshold_change": 20,
        },
        "Relaxed": {
            "smoothening": 12,
            "click_threshold_ratio": 0.2,
            "scroll_sensitivity": 1.0,
            "zoom_threshold_change": 35,
        },
        "Manual": {
            "smoothening": config.get("smoothening"),
            "click_threshold_ratio": config.get("click_threshold_ratio"),
            "scroll_sensitivity": config.get("scroll_sensitivity"),
            "zoom_threshold_change": config.get("zoom_threshold_change"),
        }
    }

    def toggle_feedback():
        config.set("visual_feedback_enabled", feedback_var.get())

    def stop_program():
        config.set("shutdown_requested", True)
        root.quit()
        root.destroy()

    def on_slider_change(attr, value):
        if profile_var.get() == "Manual":
            config.set(attr, value)
            mode_values["Manual"][attr] = value

    def apply_profile(profile):
        is_manual = profile == "Manual"
        for attr, slider in sliders.items():
            slider.config(state=NORMAL if is_manual else DISABLED)
            value = mode_values[profile][attr]
            config.set(attr, value)
            slider.set(value)

    # Toggle Camera Visual Feedback
    tb.Checkbutton(root, text="Enable Camera Visual Feedback", variable=feedback_var,
                   command=toggle_feedback).pack(pady=5)

    # Gesture Sensitivity Profile Section (moved above sliders)
    tb.Label(root, text="Gesture Sensitivity Profile").pack(pady=(15, 0))
    profile_frame = tb.Frame(root)
    profile_frame.pack(pady=10)

    for profile in ["Fast", "Precise", "Relaxed", "Manual"]:
        tb.Radiobutton(
            profile_frame,
            text=profile,
            variable=profile_var,
            value=profile,
            bootstyle="primary-toolbutton",
            width=10,
            command=lambda p=profile: apply_profile(p)
        ).pack(side="left", padx=5)

    # Sliders
    def create_slider(label, attr, frm, to, res):
        tb.Label(root, text=label).pack()
        var = tb.DoubleVar(value=config.get(attr))
        scale = tb.Scale(
            root, from_=frm, to=to, orient='horizontal', length=400,
            variable=var,
            command=lambda val, a=attr: on_slider_change(a, float(val))
        )
        scale.pack(pady=5)
        sliders[attr] = scale

    create_slider("Smoothening", "smoothening", 1, 20, 1)
    create_slider("Click Threshold Ratio", "click_threshold_ratio", 0.05, 0.3, 0.01)
    create_slider("Scroll Sensitivity", "scroll_sensitivity", 0.5, 5.0, 0.1)
    create_slider("Zoom Threshold Change", "zoom_threshold_change", 1, 50, 1)

    # Stop button full width (same as 4 buttons × width 10 + paddings)
    tb.Button(root, text="Stop Program", bootstyle="danger", command=stop_program)\
        .pack(pady=(20, 10), ipadx=188, ipady=5)

    apply_profile("Precise")
    root.mainloop()
