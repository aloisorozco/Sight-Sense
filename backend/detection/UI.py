from tkinter import ttk
import cv_capture
import tkinter as tk


class User_Interface:

    def __init__(self, args):
        self.app = tk.Tk()
        self.app.title('Sight Sense - UI')
        self.app.geometry("1920x1080+10+20")

        s = ttk.Style(self.app)
        s.configure("TNotebook", tabposition='n')

        notebook = ttk.Notebook(self.app)
        notebook.pack()

        tab_start_camera = ttk.Frame(notebook)
        tab_settings = ttk.Frame(notebook)

        notebook.add(tab_start_camera, text="Camera")
        notebook.add(tab_settings, text="Settings")

        # Add content to Tab 1
        self.label_screen = tk.Label(tab_start_camera)
        self.label_screen.grid(row=0, column=0, padx=125, pady=5)
        self.btn_start_cam = tk.Button(
            tab_start_camera, text="Open Camera", command=lambda: self.open_camera(args))
        self.btn_start_cam.grid(row=1, column=0, padx=725, pady=5)

        label_conf = tk.Label(tab_settings, text="Confidence Percentage:")
        label_conf.grid(row=0, column=0, padx=300, pady=25)

        self.slider_conf = tk.Scale(
            tab_settings, from_=40, to=80, orient="horizontal", length=300)
        self.slider_conf.grid(row=0, column=1, padx=50, pady=25)

        label_upd = tk.Label(tab_settings, text="Update Rate (sec/update):")
        label_upd.grid(row=1, column=0, padx=300, pady=25)

        self.slider_upd = tk.Scale(
            tab_settings, from_=3, to=20, orient="horizontal", length=300)
        self.slider_upd.grid(row=1, column=1, padx=50, pady=25)

        label_msg = tk.Label(tab_settings, text="Message Per Update:")
        label_msg.grid(row=2, column=0, padx=300, pady=25)

        self.slider_msg = tk.Scale(
            tab_settings, from_=1, to=3, orient="horizontal", length=300)
        self.slider_msg.grid(row=2, column=1, padx=50, pady=25)

        label_obj_size = tk.Label(
            tab_settings, text="Hazard Object Size Percentage Threshold:")
        label_obj_size.grid(row=3, column=0, padx=300, pady=25)

        self.slider_obj_size = tk.Scale(
            tab_settings, from_=60, to=90, orient="horizontal", length=300)
        self.slider_obj_size.grid(row=3, column=1, padx=50, pady=25)

        notebook.pack(expand=True, fill="both")
        self.OBSTACLE_SET = {"door", "person", "car",
                             "bicycle", "bus", "train", "truck", "bench", "chair"}

        self.timed_out = 0

        # # Initialize the thread pool executor
        # self.executor = concurrent.futures.ThreadPoolExecutor(
        #     max_workers=1)

        self.app.mainloop()

    def get_confidence(self):
        return self.slider_conf.get()

    def get_upd(self):
        return self.slider_upd.get()

    def get_msg(self):
        return self.slider_msg.get()

    def open_camera(self, args):
        self.app.withdraw()
        ai_object = cv_capture.Capture(args)
        ai_object.start_capture()
        