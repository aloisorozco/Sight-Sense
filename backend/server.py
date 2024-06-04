from flask import Flask, Response
from flask_cors import CORS
class Server():

    app = Flask(__name__)
    CORS(app) 
    _camera = None

    def __init__(self, camera) -> None:
        Server._camera = camera

    @app.route('/video_feed')
    def video_feed():
        return Response(Server._camera.start_capture(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/end_capture')
    def status():
        return Response(status=200)
    
    @app.route('/status')
    def status():
        return Response(status=200)