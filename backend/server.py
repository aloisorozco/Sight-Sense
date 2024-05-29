from flask import Flask, Response

class Server():

    app = Flask(__name__)
    _camera = None

    def __init__(self, camera) -> None:
        Server._camera = camera

    @app.route('/video_feed')
    def video_feed():
        return Response(Server._camera.start_capture(), mimetype='multipart/x-mixed-replace; boundary=frame')