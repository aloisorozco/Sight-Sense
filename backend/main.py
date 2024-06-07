import argparse
from detection.cv_capture import Capture
# from waitress import serve
from server import Server

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

    args = parse_arguments()

    camera = Capture(args)
    flask_server = Server(camera)

    app = flask_server.app

    print("Starting Server")

    app.run(host='0.0.0.0', port=5500)