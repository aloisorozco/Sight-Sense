from flask import Flask, Response, render_template, request
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # Capture from the default camera

def generate_frames():
    while True:
        succ, frame = camera.read()
        if not succ:
            camera.release()
            break
        else:
            _, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)