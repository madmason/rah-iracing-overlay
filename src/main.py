import io
import sys

# Disable logging to prevent output in the GUI
class dummyOut:
    def write(self, data):
        pass
sys.stderr = dummyOut()

import os
from PIL import Image, ImageTk 
import tkinter as tk
import threading
from ir_telemetry import IRTelemetry
from ir_webapp import IRWebApp
import time
import webbrowser
import pkgutil
import logging
import multiprocessing

class TelemetryInterface:
    def __init__(self, root):
        """
        Initializes the tkinter-based GUI and the default parameters for port and frequency.
        """
        self.root = root
        self.root.title("RAH Telemetry Overlay")
        self.root.geometry("600x300")
        self.root.configure(bg="#F5F5F5")  

        self.web_app = None
        self.telemetry = None
        self.telemetry_thread = None
        self.webapp_thread = None
        self.is_running = False
        self.port = 8085
        self.frequency = 50 

        self.font_style = ("Roboto", 12)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_ui()
        
    def start_webapp(self):
        """ Start the Flask web server in a separate process. """
        def run_server():
            try:
                self.web_app.run(host="127.0.0.1", port=self.port, debug=False)
            except Exception as e:
                logging.error("Exception occurred in web server process", exc_info=True)

        self.webapp_process = multiprocessing.Process(target=run_server)
        self.webapp_process.start()
        
    def on_closing(self):
        """ Handle application closing """
        self.is_running = False
        if hasattr(self, 'webapp_process') and self.webapp_process.is_alive():
            self.webapp_process.terminate()
        self.root.destroy()

    def setup_ui(self):
        """
        Set up the user interface, including buttons, labels, input fields, and social media icons.
        """
        title_label = tk.Label(self.root, text="RAH Telemetry Overlay", font=("Roboto", 18, "bold"), bg="#F5F5F5", fg="#37474F")
        title_label.pack(pady=10)

        main_frame = tk.Frame(self.root, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=0)

        left_frame = tk.Frame(main_frame, bg="#F5F5F5", padx=10, pady=0)
        left_frame.pack(side="left", padx=10, pady=0, fill="both", expand=True)

        self.status_label = tk.Label(left_frame, text="Status: Stopped", fg="red", bg="#F5F5F5", font=self.font_style)
        self.status_label.pack(pady=5)

        tk.Label(left_frame, text="Port:", bg="#F5F5F5", font=self.font_style).pack()
        self.port_entry = tk.Entry(left_frame, highlightthickness=0, relief="flat", font=self.font_style)
        self.port_entry.insert(0, str(self.port))
        self.port_entry.pack(pady=5)

        tk.Label(left_frame, text="Frequency (Hz):", bg="#F5F5F5", font=self.font_style).pack()
        self.freq_entry = tk.Entry(left_frame, highlightthickness=0, relief="flat", font=self.font_style)
        self.freq_entry.insert(0, str(self.frequency))
        self.freq_entry.pack(pady=5)

        self.start_button = tk.Button(left_frame, text="Start", font=self.font_style, bg="#009688", fg="white", activebackground="#00796B", activeforeground="white", padx=10, pady=5, relief="flat", highlightthickness=0)
        self.start_button.config(command=self.start_app)
        self.start_button.pack(pady=10)

        self.url_label = tk.Label(left_frame, text="", fg="blue", bg="#F5F5F5", font=self.font_style, cursor="hand2")
        self.url_label.pack(pady=10)
        self.url_label.bind("<Button-1>", lambda e: webbrowser.open(self.url_label.cget("text")))

        right_frame = tk.Frame(main_frame, bg="#F5F5F5", padx=10, pady=0)
        right_frame.pack(side="right", padx=10, pady=0, fill="both", expand=True)

        thank_label = tk.Label(right_frame, text="Thank you for using my overlay!\nany feedback is useful", font=self.font_style, bg="#F5F5F5", fg="#37474F")
        thank_label.pack(pady=10)

        icon_frame = tk.Frame(right_frame, bg="#F5F5F5")
        icon_frame.pack(pady=0)

        self.add_social_media_icon(icon_frame, 'static/img/twitch_logo.png', "https://www.twitch.tv/dizca")
        self.add_social_media_icon(icon_frame, 'static/img/github_logo.png', "https://github.com/RaulArcos")
        self.add_social_media_icon(icon_frame, 'static/img/linkedin_logo.png', "https://www.linkedin.com/in/ra%C3%BAl-arcos-herrera-b11514175/")

        # For the PayPal icon
        paypal_frame = tk.Frame(right_frame, bg="#F5F5F5")
        paypal_frame.pack(pady=0, padx=50, fill="both", expand=True)

        self.add_social_media_icon(paypal_frame, 'static/img/paypal_logo.png', "https://paypal.me/raularcosherrera")

        coffee_label = tk.Label(paypal_frame, text="Coffee? ;)", font=self.font_style, bg="#F5F5F5", fg="#37474F")
        coffee_label.pack(side="left", padx=10)

    def resource_path(self, relative_path):
        """ Get the absolute path to the resource, whether running from source or as a PyInstaller bundle. """
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def add_social_media_icon(self, parent, icon_path, url):
        """ Helper function to add clickable social media icons as images. """
        full_icon_path = self.resource_path(icon_path)
        try:
            with open(full_icon_path, 'rb') as f:
                img_data = f.read()
            img = Image.open(io.BytesIO(img_data))
        except Exception as e:
            print(f"Error opening image {full_icon_path}: {e}")
            return 

        aspect_ratio = img.width / img.height
        new_width = int(50 * aspect_ratio)
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.LANCZOS
        img_resized = img.resize((new_width, 50), resample=resample_filter)

        icon = ImageTk.PhotoImage(img_resized)

        label = tk.Label(parent, image=icon, cursor="hand2", bg="#F5F5F5")
        label.image = icon 
        label.pack(side="left", padx=10)
        label.bind("<Button-1>", lambda e: webbrowser.open(url))


    def update_status(self, status):
        """ Update the status label based on the current state. """
        if status == "running":
            self.status_label.config(text="Status: Running", fg="green")
        elif status == "no_data":
            self.status_label.config(text="Status: No Data", fg="orange")
        else:
            self.status_label.config(text="Status: Stopped", fg="red")

    def start_webapp(self):
        """ Start the Flask web server in a separate thread. """
        self.web_app.run(host="127.0.0.1", port=self.port, debug=False)

    def start_app(self):
        """ Start the telemetry application and web app. """
        if not self.is_running:
            self.port = int(self.port_entry.get())
            self.frequency = int(self.freq_entry.get())

            self.web_app = IRWebApp()
            self.telemetry = IRTelemetry(self.web_app.socketio)

            self.webapp_thread = threading.Thread(target=self.start_webapp, daemon=True)
            self.webapp_thread.start()

            def telemetry_run():
                while self.is_running:
                    self.telemetry.check_iracing()
                    if self.telemetry.state.ir_connected:
                        self.telemetry.retrieve_data()
                    time.sleep(1 / self.frequency)

            self.telemetry_thread = threading.Thread(target=telemetry_run, daemon=True)
            self.is_running = True
            self.telemetry_thread.start()

            self.update_status("running")
            
            self.url_label.config(text=f"http://127.0.0.1:{self.port}/input-telemetry")
            self.url_label.config(fg="blue")


if __name__ == '__main__':
    root = tk.Tk()
    app = TelemetryInterface(root)
    root.mainloop()
