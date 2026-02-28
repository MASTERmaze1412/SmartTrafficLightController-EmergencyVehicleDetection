from picamera2 import Picamera2
from gpiozero import Servo
from time import sleep
from datetime import datetime
import os

SAVE_DIR = "/home/pi/Pictures/pi_dual_camera"
os.makedirs(SAVE_DIR, exist_ok=True)

# Init cameras
cam0 = Picamera2(camera_num=0)
cam1 = Picamera2(camera_num=1)

cam0.configure(cam0.create_still_configuration())
cam1.configure(cam1.create_still_configuration())

cam0.start()
cam1.start()
sleep(2)

# Init servo
servo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)
sleep(1)

def move_servo(value):
    servo.value = value
    sleep(2)

def capture(cam, filename):
    cam.capture_file(filename)
    sleep(1)

print("Capturing Images...")

# ----------- 0 DEGREE -----------
move_servo(-1)
sleep(3)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
capture(cam0, f"{SAVE_DIR}/lane1_{ts}.jpg")
capture(cam1, f"{SAVE_DIR}/lane2_{ts}.jpg")

# ----------- 120 DEGREE ----------
move_servo(0.33)
sleep(3)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
capture(cam0, f"{SAVE_DIR}/lane3_{ts}.jpg")
capture(cam1, f"{SAVE_DIR}/lane4_{ts}.jpg")

print("Capture completed successfully.")

cam0.stop()
cam1.stop()