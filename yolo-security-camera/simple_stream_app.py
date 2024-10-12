from flask import Flask, Response, render_template
import cv2
import threading
import sys

app = Flask(__name__)

# Global variables
output_frame = None
lock = threading.Lock()

# Check if the device is a Raspberry Pi
def is_raspberry_pi():
    try:
        with open('/proc/cpuinfo', 'r') as f:
            return 'raspberry pi' in f.read().lower()
    except:
        return False

# Initialize the camera
if is_raspberry_pi():
    from picamera2 import Picamera2
    sys.path.append('/usr/lib/python3/dist-packages')
    camera = Picamera2()
    camera.configure(camera.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
    camera.start()
else:
    camera = cv2.VideoCapture(0)

def generate_frames():
    global output_frame, lock
    while True:
        with lock:
            if output_frame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", output_frame)
            if not flag:
                continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
              bytearray(encodedImage) + b'\r\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(),
                    mimetype = "multipart/x-mixed-replace; boundary=frame")

def capture_frames():
    global output_frame, lock
    while True:
        if is_raspberry_pi():
            frame = camera.capture_array()
        else:
            ret, frame = camera.read()
            if not ret:
                continue
        
        with lock:
            output_frame = frame.copy()

if __name__ == '__main__':
    t = threading.Thread(target=capture_frames)
    t.daemon = True
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=True,
            threaded=True, use_reloader=False)