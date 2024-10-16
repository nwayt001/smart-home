import cv2
from ultralytics import YOLO
import os
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import time


class SendEmail():
    def __init__(self):
        self.email = 'nick.waytowich2@gmail.com'
        self.password = 'udwu lize vcvf oauc'
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.email, self.password)

        self.subject =  "Squirrel Alert: Squirrel Detected!"
        self.message = "Alert! A squirrel has been detected on your porch."

        self.last_email_time = 0
        self.min_interval = 45  # Minimum interval between emails (in seconds)


    def send(self, image = None):
        try:
            # Check if the minimum interval has passed
            current_time = time.time()
            if current_time - self.last_email_time < self.min_interval:
                return
            self.last_email_time = current_time

            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.email, self.password)
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = self.email
            msg['Subject'] = self.subject
            msg.attach(MIMEText(self.message, 'plain'))

            # attach image
            # Attach the image
            if image is not None:
                image_bytes = cv2.imencode('.jpg', image)[1].tobytes()
                image_mime = MIMEImage(image_bytes, name="squirrel_detected.jpg")
                msg.attach(image_mime)

            self.server.send_message(msg)
            print("Email alert sent!")  # Print a message to the console
            del msg
        except Exception as e:
            print(f"Error: {e}")

    def __del__(self):
        self.server.quit()


class SquirrelDecetor():
    def __init__(self, model_path='yolo_squirrel.pt', visualize=None, confidence_threshold=0.5):    

        # load yolo model
        self.model = YOLO(model_path, verbose=False)

        # check if the device is a Raspberry Pi
        self.RASPI = self.is_raspberry_pi()

        # initialize the camera (depdending on the device)
        self.init_camera()

        if visualize is not None:
            self.visualize = visualize
        
        # Setup email alert
        self.email = SendEmail()

        # Confidence threshold for detection
        self.confidence_threshold = confidence_threshold

    # Check if the device is a Raspberry Pi by inspecting the hardware info
    def is_raspberry_pi(self):
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read().lower()
                if 'raspberry pi' in cpuinfo or 'bcm' in cpuinfo:
                    import sys
                    sys.path.append('/usr/lib/python3/dist-packages')
                    print("Running on a Raspberry Pi")
                    self.visualize = False  # don't visualize stream on the pi
                    return True
        except FileNotFoundError:
            pass
        print("Running on a standard Linux desktop")
        self.visualize = True # visualize stream on the desktop
        return False

    # Initialize the camera
    def init_camera(self):
        # check if the device is a Raspberry Pi
        if self.RASPI:
            from picamera2 import Picamera2
            self.camera = Picamera2()
            self.camera.configure(self.camera.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
            self.camera.start()
        else:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                print("Error: Could not open camera.")
                exit()


    def get_frame(self):
        if self.RASPI:
            return self.camera.capture_array()
        else:
            ret, frame = self.camera.read()
            return frame
        

    def run(self):
        while True:

            # Read frame from the camera
            frame = self.get_frame()

            # Run YOLOv8 on the current frame
            results = self.model(frame, verbose=False)

            # Check if a squirrel is detected 
            for r in results[0].boxes:
                if int(r.cls) == 0 and r.conf.item() > self.confidence_threshold:
                    print("Squirrel detected!")
                    print('\a')  # Plays a simple beep sound (on some systems)
                    annotated_frame = results[0].plot()
                    self.email.send(image = annotated_frame) # Send an email alert


            # Draw bounding boxes on the detected objects and visualize the frame
            if self.visualize:
                annotated_frame = results[0].plot()
                cv2.imshow('YOLO Squirrel Detection', annotated_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def __del__(self):
        self.camera.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='yolo_squirrel.pt', help='Path to the YOLO model')
    parser.add_argument('--visualize', action='store_true', help='Visualize the stream')    
    parser.add_argument('--confidence', type=float, default=0.7, help='Confidence threshold for detection')

    args = parser.parse_args()
    
    visualize = None
    if args.visualize:
        print("Visualizing the stream")
        visualize = True

    # Run the squirrel detector
    detector = SquirrelDecetor(visualize=visualize, confidence_threshold=args.confidence)
    detector.run()
