import socketio
from aiohttp import web
import aiohttp_cors
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
    

    async def status(request):
        return web.Response(status=200)


    async def capture_and_send(self):
        for encoded_frame in Server._camera.start_capture():
            await Server.sio.emit('frame', encoded_frame)
            await Server.sio.sleep(0.01)

            
    @sio.on('connect')
    async def connect(sid, environ):
        print('Client connected:', sid)
        await Server.sio.emit('reply', f"status: 200")

    @sio.on('disconnect')
    async def disconnect(sid):
        print('Client disconnected:', sid)
        
    
    @sio.on('end_stream')
    async def end_stream(sid):
        Server._camera.set_end_stream(True)
        print("Ending Stream for all connected clients")
        await Server.sio.emit('reply', f"status: 200")

    
    # Factory app init to start backround process
    async def init_app(self):
        Server.sio.start_background_task(Server.capture_and_send, self)
        return Server.app

    # Add route to CORS
    status_route = app.router.add_get('/status', status)
    cors.add(status_route)