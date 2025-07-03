import tkinter as tk
from config import config

def start_ui():
    root = tk.Tk()
    root.title("Virtual Mouse Settings")
    root.geometry("400x300")

    feedback_var = tk.BooleanVar(value=config.visual_feedback_enabled)

    def toggle_feedback():
        config.visual_feedback_enabled = feedback_var.get()

    def stop_program():
        config.shutdown_requested = True
        root.quit()       # Exit the Tkinter UI
        root.destroy()    # Close the window completely

    # Visual Feedback Toggle
    tk.Checkbutton(
        root, text="Enable Camera Visual Feedback",
        variable=feedback_var,
        command=toggle_feedback
    ).pack(pady=10)

    # Stop Program Button
    tk.Button(
        root, text="Stop Program", fg="white", bg="red",
        command=stop_program
    ).pack(pady=20)

    def slider(label, attr, frm, to, res):
        tk.Label(root, text=label).pack()
        tk.Scale(root, from_=frm, to=to, resolution=res, orient=tk.HORIZONTAL,
                 command=lambda val: setattr(config, attr, float(val))).pack()

    slider("Smoothening", "smoothening", 1, 20, 1)
    slider("Click Threshold Ratio", "click_threshold_ratio", 0.05, 0.3, 0.01)
    slider("Scroll Sensitivity", "scroll_sensitivity", 0.5, 5.0, 0.1)
    slider("Zoom Threshold Change", "zoom_threshold_change", 1, 50, 1)

    root.mainloop()
