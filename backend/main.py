import argparse
import server
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

args = parse_arguments()

camera = Capture(args)
flask_server = server.Server(camera)

print("Starting Server")
flask_server.app.run(host='0.0.0.0', port=5500)

# Remove local UI - replacing it with react app
# ui = User_Interface(args)
