from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import socketio
import eventlet
import eventlet.wsgi
class Server():

    app = Flask(__name__)
    sio = socketio.Server(cors_allowed_origins='*')
    app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
    CORS(app)

    _camera = None
    _mutex = None
    _frames = None

    def __init__(self, camera, frames = None, frames_mutex = None) -> None:

        # Server._mutex = frames_mutex
        # Server._frames = frames
        Server._camera = camera


    def capture_and_send(self):
        for encoded_frame in Server._camera.start_capture():
            Server.sio.emit('frame', encoded_frame)
            Server.sio.sleep(0.01)

    @sio.on('connect')
    def connect(sid, environ):
        print('Client connected:', sid)

    @sio.on('disconnect')
    def disconnect(sid):
        print('Client disconnected:', sid)
        
    @app.route('/status')
    def status():
        return Response(status=200)
    
    @app.route('/end_stream')
    def end_stream():
        return Response(status=200)