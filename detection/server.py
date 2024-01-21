import socket, pickle
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

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

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

    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        '''data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))'''
        #data = input(' -> ')

        
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

        print(frame) 

        # Pickle the object and send it to the server
        data_string = pickle.dumps(frame)
        conn.send(data_string)

        #conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


if __name__ == '__main__':
    server_program()