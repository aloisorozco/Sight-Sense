import argparse
import eventlet
import eventlet.wsgi
from detection.cv_capture import Capture
# from waitress import serve
from server import Server
import threading

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

if __name__ == "__main__":
    # frames = queue.Queue()
    # frames_mutex = threading.Semaphore()

    PORT = 5500
    IP = '127.0.0.1'

    args = parse_arguments()

    camera = Capture(args)
    flask_server = Server(camera)

    app = flask_server.app
    sio = flask_server.sio
    
    capure_thread = sio.start_background_task(flask_server.capture_and_send)
    
    print(f' ------------- Staring Server ------------- PORT: {PORT}')
    eventlet.wsgi.server(eventlet.listen((IP, PORT)), app)