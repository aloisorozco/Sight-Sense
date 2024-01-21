import tkinter as tk
from PIL import Image, ImageTk 
from tkinter import ttk
from filter import filter_objects, Obstacle
from notify import sort_and_trim_objects

import cv2
import supervision as sv
import numpy as np
import time

class User_Interface:

    def __init__(self, model, cap, zone, zone_polygon, zone_annotator, box_annotator):
        self.app = tk.Tk()
        self.app.bind('<Escape>', lambda e: self.app.quit()) 
        self.app.title('Sight Sense')
        self.app.geometry("1920x1080+10+20")
        self.app.attributes("-fullscreen", True)

        notebook = ttk.Notebook(self.app)
        notebook.pack()

        tab_start_camera = ttk.Frame(notebook)
        tab_settings = ttk.Frame(notebook)

        notebook.add(tab_start_camera, text="Open Camera")
        notebook.add(tab_settings, text="Settings")

        # Add content to Tab 1
        self.label_screen = tk.Label(tab_start_camera)
        self.label_screen.grid(row=0, column=0)
        self.btn_start_cam = tk.Button(tab_start_camera, text="Open Camera", command= lambda: self.open_camera(model, cap, zone, zone_polygon, zone_annotator, box_annotator)) 
        self.btn_start_cam.grid(row=0, column=1)

        label_conf = tk.Label(tab_settings, text="Confidence Percentage:")
        label_conf.grid(row=0, column=0, padx=5, pady=5)

        self.slider_conf = tk.Scale(tab_settings, from_=40, to=80, orient="horizontal", length=300)
        self.slider_conf.grid(row=0, column=1, padx=5, pady=5)

        label_upd = tk.Label(tab_settings, text="Update Rate (sec/update):")
        label_upd.grid(row=1, column=0, padx=5, pady=5)

        self.slider_upd = tk.Scale(tab_settings, from_=3, to=20, orient="horizontal", length=300)
        self.slider_upd.grid(row=1, column=1, padx=5, pady=5)

        label_msg = tk.Label(tab_settings, text="Message Per Update:")
        label_msg.grid(row=2, column=0, padx=5, pady=5)

        self.slider_msg = tk.Scale(tab_settings, from_=1, to=3, orient="horizontal", length=300)
        self.slider_msg.grid(row=2, column=1, padx=5, pady=5)

        label_obj_size = tk.Label(tab_settings, text="Hazard Object Size Percentage Threshold:")
        label_obj_size.grid(row=3, column=0, padx=5, pady=5)

        self.slider_obj_size = tk.Scale(tab_settings, from_=60, to=90, orient="horizontal", length=300)
        self.slider_obj_size.grid(row=3, column=1, padx=5, pady=5)

        notebook.pack(expand=True, fill="both")
        self.OBSTACLE_SET = {"door", "person", "car", "bicycle", "bus", "train", "truck", "bench", "chair", "cell phone", "bottle"}

        self.timed_out = 0

        self.app.mainloop()


    def get_confidence(self):
        return self.slider_conf.get()
    

    def get_upd(self):
        return self.slider_upd.get()
    

    def get_msg(self):
        return self.slider_msg.get()


    def open_camera(self, model, cap, zone, zone_polygon, zone_annotator, box_annotator):
        ret, frame = cap.read()

        self.btn_start_cam.config(state=tk.DISABLED)

        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_yolov8(result)
        labels = [
            f"{model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections
        ]

        obstacles = [
            Obstacle(model.model.names[class_id], confidence, xyxy, zone_polygon)
            for xyxy, confidence, class_id, _
            in detections
        ]

        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
        )
        
        obstacles = sort_and_trim_objects(filter_objects(obstacles, self.OBSTACLE_SET, self.slider_conf.get() / 100), self.slider_msg.get(), self.slider_obj_size.get() / 100)

        #print(obstacles)

        if len(obstacles) > 0 and time.time() > self.timed_out:
            print(obstacles)
            self.timed_out = time.time() + self.slider_upd.get()

        zone.trigger(detections=detections)
        frame = zone_annotator.annotate(scene=frame)      
        
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

        captured_image = Image.fromarray(opencv_image) 
 
        photo_image = ImageTk.PhotoImage(image=captured_image) 

        self.label_screen.photo_image = photo_image 

        self.label_screen.configure(image=photo_image) 

        self.label_screen.after(10, lambda: self.open_camera(model, cap, zone, zone_polygon, zone_annotator, box_annotator)) 