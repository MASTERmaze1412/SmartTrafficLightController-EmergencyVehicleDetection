# main.py

import time
import signal

from capture_images import run_capture, cleanup_capture
from analyze_captured_images import run_analysis
from traffic_logic import run_traffic_cycle, set_green, transition_to_yellow, set_red
from siren_detect_two_lanes import check_emergency

running = True

def shutdown(sig, frame):
    global running
    print("\nShutting down safely...")
    running = False

signal.signal(signal.SIGINT, shutdown)

print("Smart Traffic System Started")

try:
    while running:
        # 1️⃣ Check Emergency First
        emergency = check_emergency()

        if emergency["status"]:
            print("\n🚨 Emergency Override Activated")

            lane = emergency["priority_lane"]  # e.g. "lane1" or "lane2"

            set_green(lane)
            time.sleep(20)

            transition_to_yellow(lane)
            time.sleep(3)

            set_red(lane)

        else:
            # 2️⃣ Normal Cycle
            run_capture()
            lane_data = run_analysis()
            run_traffic_cycle(lane_data)

        time.sleep(1)

except Exception as e:
    print("System Error:", e)

finally:
    cleanup_capture()
    print("System Stopped")
