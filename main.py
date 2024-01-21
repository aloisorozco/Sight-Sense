'''from ultralytics import YOLO
#from ultralytics.yolo.v8.detect.predict import DetectionPredictor
import cv2

model = YOLO("yolov8x.pt")

results = model.predict(source="0", show=True)

print(results)'''

import time

import cv2
import argparse

from ultralytics import YOLO
import supervision as sv
import numpy as np

from filter import filter_objects, Obstacle
from notify import sort_and_trim_objects

#cell phone and bottle are here just for testing purposes
OBSTACLE_SET = {"person", "car", "bicycle", "bus", "train", "truck", "bench", "chair", "cell phone", "bottle"}

URGENT_OBSTACLE_SET = {"car", "bicycle", "bus", "train", "truck", "cellphone"}

min_bound = 0.5
max_bound = 1

ZONE_POLYGON = np.array([
    [min_bound, min_bound],
    [max_bound, min_bound],
    [max_bound, max_bound],
    [min_bound, max_bound]
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


def main():
    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

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
        
        cv2.imshow("yolov8", frame)

        if (cv2.waitKey(30) == 27):
            break


if __name__ == "__main__":
    main()