'''from ultralytics import YOLO
#from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

model = YOLO("yolov8x.pt")

results = model.predict(source="0", show=True)

print(results)'''

import time

import cv2
import argparse

from tkinter import *
from PIL import Image, ImageTk 

from ultralytics import YOLO
import supervision as sv
import numpy as np

from filter import filter_objects, Obstacle
from notify import sort_and_trim_objects

#cell phone and bottle are here just for testing purposes
OBSTACLE_SET = {"person", "car", "bicycle", "bus", "train", "truck", "bench", "chair", "cell phone", "bottle"}

URGENT_OBSTACLE_SET = {"car", "bicycle", "bus", "train", "truck", "cellphone"}

min_x_bound = 0.3
max_x_bound = 0.7

min_y_bound = 0
max_y_bound = 1

ZONE_POLYGON = np.array([
    [min_x_bound, min_y_bound],
    [max_x_bound, min_y_bound],
    [max_x_bound, max_y_bound],
    [min_x_bound, max_y_bound]
])


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

def open_camera():

    ret, frame = cap.read()

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
    
    obstacles = sort_and_trim_objects(filter_objects(obstacles, OBSTACLE_SET))

    print(obstacles)

    '''if len(obstacles) > 0 and time.time() > timed_out:
        print(obstacles)
        timed_out = time.time() + 5'''

    zone.trigger(detections=detections)
    frame = zone_annotator.annotate(scene=frame)      
    
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

    # Capture the latest frame and transform to image 
    captured_image = Image.fromarray(opencv_image) 

    # Convert captured image to photoimage 
    photo_image = ImageTk.PhotoImage(image=captured_image) 

    # Displaying photoimage in the label 
    label_widget.photo_image = photo_image 

    # Configure image in the label 
    label_widget.configure(image=photo_image) 

    # Repeat the same process after every 10 seconds 
    label_widget.after(10, open_camera) 

    #cv2.imshow("yolov8", frame)

    #if (cv2.waitKey(30) == 27):
        #break

args = parse_arguments()
frame_width, frame_height = args.webcam_resolution

#TODO: change to 1 for webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

app = Tk() 

# Bind the app with Escape keyboard to 
# quit app whenever pressed 
app.bind('<Escape>', lambda e: app.quit()) 
app.title('Sight Sense')
app.geometry("1920x1080+10+20")

# Create a label and display it on app 
label_widget = Label(app) 
label_widget.pack() 

model = YOLO("yolov8l.pt")

box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=1
)

zone_polygon = (ZONE_POLYGON * np.array(args.webcam_resolution)).astype(int)
zone = sv.PolygonZone(polygon=zone_polygon, frame_resolution_wh=tuple(args.webcam_resolution))
zone_annotator = sv.PolygonZoneAnnotator(
    zone=zone, 
    color=sv.Color.red(),
    thickness=2,
    text_thickness=4,
    text_scale=2
)

timed_out = 0

button1 = Button(app, text="Open Camera", command=open_camera) 
button1.pack() 

app.mainloop()

'''if __name__ == "__main__":
    main()'''