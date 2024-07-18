import socketio
from aiohttp import web
import aiohttp_cors
from detection.cv_capture import Capture

class Server():

    app = web.Application()
    sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='aiohttp', async_handlers=True)

    sio.attach(app)

    # Set up CORS for aiohttp
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    _camera = None

    def __init__(self, camera) -> None:
        Server._camera = camera
    

    async def capture_and_send(self):
        for encoded_frame in Server._camera.start_capture():
            await Server.sio.emit('frame', encoded_frame, room='super_secret_security_camera_broadcast')
            await Server.sio.sleep(0.01)


    async def lock_in_face(id):
        Capture.update_auth_target(id)
    

    async def check_face_existance(id):
        # TODO: secutirey check if face exists - future Daniel problem
        return True
    

    # this is not a socket opperation - just a standard HTTP request to see if server is alive
    async def status(request):
        return web.Response(status=200)
    

    @sio.on('authenticate') # TODO: Connect on the frontend
    async def join_stream(sid, data):
        if len(Server.sio.rooms(sid)) == 0:
            await Server.sio.emit('user_in_no_rooms', 401, sid)

        elif (await Server.check_face_existance(data)):
            Server.sio.start_background_task(Server.lock_in_face, data)
            await Server.sio.emit('auth_started', 200, sid)

        else:
            await Server.sio.emit('face_not_found', 402, sid)
            

    @sio.on('join_stream')
    async def join_stream(sid):
        print(f'----- {sid} joined security broadcast stream -----')
        await Server.sio.enter_room(sid, 'super_secret_security_camera_broadcast')
        await Server.sio.emit('join_stream_confirmation', 200, sid)


    @sio.on('connect')
    async def connect(sid, environ):
        print('Client connected:', sid)
        await Server.sio.emit('reply', f"status: 200")


    @sio.on('disconnect')
    async def disconnect(sid):
        print('Client disconnected:', sid)
        
    
    @sio.on('end_stream')
    async def end_stream(sid):
        # Server._camera.set_end_stream(True) # Ends stream for everyone by killing model - idealy we will have model run all the time and broadcast video to a cloud server
        print(f'Ending Stream for {sid}')
        await Server.sio.leave_room(sid, 'super_secret_security_camera_broadcast')
        await Server.sio.emit('stream_exit_res', 200, sid)


    # Factory app init to start backround process
    async def init_app(self):
        Server.sio.start_background_task(Server.capture_and_send, self)
        return Server.app

    # Add route to CORS
    status_route = app.router.add_get('/status', status)
    cors.add(status_route)