import argparse
from aiohttp import web
from detection.cv_capture import Capture
from server import Server

# TODO: use mediapipe to render face mesh - but only fire the model when YOLO detects a person (no wasting resources). Then, ask the user to move the face around to make sure the person is real and not a photo.

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

    PORT = 5500
    IP = '127.0.0.1'

    args = parse_arguments()

    camera = Capture(args)
    server = Server(camera)

    sio = server.sio

    print(f' ------------- Staring Server ------------- PORT: {PORT}')
    web.run_app(server.init_app(), host=IP, port=PORT)