from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
class Server():

    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="*")
    
    CORS(app) 
    _camera = None
    _mutex = None
    _frames = None

    def __init__(self, camera, frames = None, frames_mutex = None) -> None:

        # Server._mutex = frames_mutex
        # Server._frames = frames
        Server._camera = camera

    @socketio.on("connect")
    def connected():
        """event listener when client connects to the server"""
        print(request.sid)
        print("client has connected")
        emit("connect",{"data":f"id: {request.sid} is connected"})

    @socketio.on('frame')
    def model_stream_connection():
        for frame in Server._camera.start_capture():
            Server.socketio.emit('frame', frame)

    
    @app.route('/status')
    def status():
        return Response(status=200)
    
    @app.route('/end_stream')
    def end_stream():
        return Response(status=200)