# capture_images.py

from picamera2 import Picamera2
from gpiozero import Servo
from time import sleep
from datetime import datetime
import os

SAVE_DIR = "/home/pi/Pictures/pi_dual_camera"
os.makedirs(SAVE_DIR, exist_ok=True)

_cam0 = None
_cam1 = None
_servo = None
_initialized = False

def init_capture():
    """Initialize cameras + servo ONCE and reuse them."""
    global _cam0, _cam1, _servo, _initialized
    if _initialized:
        return

    _cam0 = Picamera2(camera_num=0)
    _cam1 = Picamera2(camera_num=1)

    _cam0.configure(_cam0.create_still_configuration())
    _cam1.configure(_cam1.create_still_configuration())

    _cam0.start()
    _cam1.start()
    sleep(2)

    _servo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)
    sleep(1)

    _initialized = True

def run_capture():
    """Capture four images (lane1..lane4) using the already-initialized cameras."""
    global _cam0, _cam1, _servo, _initialized

    if not _initialized:
        init_capture()

    def move_servo(value):
        _servo.value = value
        sleep(2)

    def capture(cam, filename):
        cam.capture_file(filename)
        sleep(0.5)

    print("\n📷 Capturing Images...")

    # 0 Degree
    move_servo(-1)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    capture(_cam0, f"{SAVE_DIR}/lane1_{ts}.jpg")
    capture(_cam1, f"{SAVE_DIR}/lane2_{ts}.jpg")

    # 120 Degree
    move_servo(0.33)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    capture(_cam0, f"{SAVE_DIR}/lane3_{ts}.jpg")
    capture(_cam1, f"{SAVE_DIR}/lane4_{ts}.jpg")

    print("✅ Capture completed.")

def cleanup_capture():
    """Stop + close cameras and detach servo safely."""
    global _cam0, _cam1, _servo, _initialized

    if _cam0:
        try:
            _cam0.stop()
        except:
            pass
        try:
            _cam0.close()
        except:
            pass

    if _cam1:
        try:
            _cam1.stop()
        except:
            pass
        try:
            _cam1.close()
        except:
            pass

    if _servo:
        try:
            _servo.detach()
        except:
            pass

    _cam0 = None
    _cam1 = None
    _servo = None
    _initialized = False

    # Give libcamera a moment to release hardware fully
    sleep(0.5)
