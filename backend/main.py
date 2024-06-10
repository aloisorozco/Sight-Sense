import argparse
from aiohttp import web
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

    PORT = 5500
    IP = '127.0.0.1'

    args = parse_arguments()

    camera = Capture(args)
    server = Server(camera)

    app = server.app
    sio = server.sio

    print(f' ------------- Staring Server ------------- PORT: {PORT}')
    web.run_app(server.init_app(), host=IP, port=PORT)