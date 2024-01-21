from UI import User_Interface
import time

import cv2
import argparse
from PIL import Image, ImageTk 

from ultralytics import YOLO
import supervision as sv
import numpy as np

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

args = parse_arguments()
frame_width, frame_height = args.webcam_resolution

#TODO: change to 1 for webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

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
ui = User_Interface(model, cap, zone, zone_polygon, zone_annotator, box_annotator)

while(True):
    ui.open_camera(model, cap, zone, zone_polygon, zone_annotator, box_annotator)
