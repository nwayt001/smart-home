import cv2
from ultralytics import YOLO
import os
import argparse

class SquirrelDecetor():
    def __init__(self, model_path='yolo_squirrel.pt', visualize=None):

        # load yolo model
        self.model = YOLO(model_path, verbose=False)

        # check if the device is a Raspberry Pi
        self.RASPI = self.is_raspberry_pi()

        # initialize the camera (depdending on the device)
        self.init_camera()

        if visualize is not None:
            self.visualize = visualize
        
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
                if int(r.cls) == 0:
                    print("Squirrel detected!")
                    print('\a')  # Plays a simple beep sound (on some systems)


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

    args = parser.parse_args()
    
    visualize = None
    if args.visualize:
        print("Visualizing the stream")
        visualize = True

    # Run the squirrel detector
    detector = SquirrelDecetor(visualize=visualize)
    detector.run()
