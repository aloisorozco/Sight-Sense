from PIL import Image, ImageTk
from tkinter import ttk
from filter import Obstacle
from ultralytics import YOLO
from annotators import Annotators

import audio.tts as tts
import threading
import concurrent.futures
import cv2
import supervision as sv
import time
import tkinter as tk


class User_Interface:

    speech_thread = None

    def __init__(self, args):
        self.app = tk.Tk()
        self.app.title('Sight Sense - UI')
        self.app.geometry("1920x1080+10+20")

        self.speech = tts.TTS()

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

    def _speak_messages(self, obstacles):
        for obstacle in obstacles:
            self.speech.generate_and_play(obstacle.__str__())

    def open_camera(self, args):

        self.app.withdraw()
        frame_width, frame_height = args.webcam_resolution
        CONFIDENCE_THRESHOLD = 0.5
        TIME_OUT = 2

        # change to 1 for webcam - if you have another device connected, otherwise leave at 0 for your default webcam
        # Capture vide + load model
        cap = cv2.VideoCapture(0)
        model = YOLO("yolov8n.pt")
        model.fuse()

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        annotators = Annotators(args.webcam_resolution)

        while True:

            succ, frame = cap.read()
            if not succ:
                print("frame not returned - exiting")
                break  # Break the loop if no frame is returned

            result = model(frame, agnostic_nms=True)[0]
            detections = sv.Detections.from_ultralytics(result)
            labels = [
                f"{model.names[class_id]} {confidence:0.2f}"
                for _, _, confidence, class_id, _, _ in detections
            ]

            time_red = time.time()

            obstacles = [
                Obstacle(model.names[class_id],
                         confidence, xyxy, annotators.zone_polygon, time_red, frame_width)
                for xyxy, _, confidence, class_id, _, _ in detections
            ]

            # render only objects that are still on screen
            # time_now = time.time()
            # obstacles_to_speak = [
            #     obstacle for obstacle in obstacles if obstacle is not None and time_now - obstacle.time_registered < TIME_OUT]
            # # submit task to thread pool
            # self.executor.submit(self._speak_messages, obstacles_to_speak)

            if (User_Interface.speech_thread == None or not User_Interface.speech_thread.is_alive()):
                obstacles_to_speak = [obstacle for obstacle in obstacles if obstacle != None and time.time(
                ) - obstacle.time_registered < TIME_OUT]
                User_Interface.speech_thread = threading.Thread(
                    target=self._speak_messages, args=(obstacles_to_speak,))
                User_Interface.speech_thread.start()

            frame = annotators.bb_annotator.annotate(
                scene=frame,
                detections=detections
            )

            frame = annotators.label_annotator.annotate(
                scene=frame,
                detections=detections,
                labels=labels
            )

            annotators.zone.trigger(detections=detections)
            frame = annotators.zone_annotator.annotate(scene=frame)

            cv2.imshow("Sight Sence - Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the capture object and close all windows
        cap.release()
        cv2.destroyAllWindows()
