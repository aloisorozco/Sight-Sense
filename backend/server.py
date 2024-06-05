from flask import Flask, Response
from flask_cors import CORS
import time
class Server():

    app = Flask(__name__)
    CORS(app) 
    _camera = None
    _mutex = None
    _frames = None

    def __init__(self, camera, frames, frames_mutex) -> None:

        Server._mutex = frames_mutex
        Server._frames = frames
        Server._camera = camera

    @app.route('/video_feed')
    def video_feed():
        
        if(not Server._camera.is_alive()):
            Server._camera.start()
        
        # busy wait if empty queue
        while(Server._frames.empty()):
            time.sleep(1)
        
        Server._mutex.acquire()
        frame = Server._frames.get()
        Server._mutex.release()

        return Response(frame, mimetype='multipart/x-mixed-replace; boundary=frame')
    
    @app.route('/status')
    def status():
        return Response(status=200)
    
    @app.route('/end_stream')
    def end_stream():
        return Response(status=200)