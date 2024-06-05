import argparse
import server
import queue
import threading
from detection.cv_capture import Capture

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


frames = queue.Queue()
frames_mutex = threading.Semaphore()

args = parse_arguments()

camera = Capture(args, frames, frames_mutex)
flask_server = server.Server(camera, frames, frames_mutex)

print("Starting Server")
flask_server.app.run(host='0.0.0.0', port=5500)

