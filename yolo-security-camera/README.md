# YOLOv8 Security Camera - Squirrel Detection

This project sets up a security camera on my front porch to detect squirrels using YOLOv8 Nano. When a squirrel is detected, the system sounds a buzzer to scare them off. Eventually, I plan to extend this to detect people and send notifications.

![Squirrel Detection](https://example.com/security_camera_image)  <!-- Replace with a relevant image -->

## Features
- **Squirrel Detection**: Uses YOLOv8 Nano to detect squirrels in real time.
- **Action Trigger**: Sounds a loud buzzer when a squirrel is detected to deter them from damaging potted plants.
- **Expandable**: Future features will include human detection and sending notifications.

## Setup

### Requirements
- Raspberry Pi or similar
- Camera module (Logitech webcam or Arducam)
- Python with OpenCV and YOLOv8 installed (`ultralytics` package)

### Installation
1. Install the required dependencies:
   ```bash
   pip install ultralytics opencv-python
   ```
2. Run the script:
    ```bash
   python run_squirrel_detector.py
   ```

### Code Overview
The script captures frames from the camera, runs YOLOv8 Nano on each frame, and checks for squirrels.

When a squirrel is detected, the system can be configured to trigger actions such as:

Sounding an alarm.

Sending a notification (to be added later).

### Future Improvements
Implement notification system for human detection.

Add more detection classes (e.g., other animals, delivery people).
