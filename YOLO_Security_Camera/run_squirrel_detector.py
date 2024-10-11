import cv2
from ultralytics import YOLO

# Load YOLOv8 Nano model
model = YOLO("yolov8n.pt")  

# Open the camera feed (0 is the default camera)
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Read frame from the camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    # Run YOLOv8 on the current frame
    results = model(frame)

    # Draw bounding boxes on the detected objects
    annotated_frame = results[0].plot()

    # Check if a squirrel is detected (replace 'squirrel' with the appropriate class name if needed)
    for r in results[0].boxes:
        # Assuming 'squirrel' is the label assigned during training
        if r.cls == 'squirrel':
            print("Squirrel detected!")
            # Here, you can add your custom action, for example:
            # - Sound an alarm
            # - Send a notification
            # - Trigger a deterrent device, etc.
            # Example: Sound a beep
            print('\a')  # Plays a simple beep sound (on some systems)

    # Display the frame with detections
    cv2.imshow('YOLO Squirrel Detection', annotated_frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
