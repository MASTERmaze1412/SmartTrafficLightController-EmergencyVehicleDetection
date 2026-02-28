# siren_detect_two_lanes.py

import spidev
import time
from datetime import datetime

# ================= SPI SETUP =================
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# ================= CONFIG =================
THRESHOLD = 600
CONFIRM_CYCLES = 3   # prevent false trigger

# ================= STATE VARIABLES =================
sensor1_time = None
sensor2_time = None
sensor1_confirm = 0
sensor2_confirm = 0

# ================= LOW LEVEL READ =================

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def read_average(channel, samples=5):
    total = 0
    for _ in range(samples):
        total += read_channel(channel)
        time.sleep(0.002)
    return total // samples

def get_vehicle_count(lane_number):
    """
    Optional: used only if both lanes trigger at same exact time.
    Reads a file format like: lane1,7
    """
    try:
        with open("/home/pi/Desktop/traffic_result.txt", "r") as f:
            data = f.read().strip()
            lane_name, vehicle_count = data.split(",")
            return int(vehicle_count)
    except:
        return 0

# ================= MAIN CHECK FUNCTION =================

def check_emergency():
    """
    Call this function repeatedly from main.py.
    Returns:
        {
            "status": True/False,
            "priority_lane": "lane1" or "lane2" or None
        }
    """

    global sensor1_time, sensor2_time
    global sensor1_confirm, sensor2_confirm

    sensor1 = read_average(0)
    sensor2 = read_average(1)

    current_time = datetime.now()

    # ---------------- Sensor 1 ----------------
    if sensor1 > THRESHOLD:
        sensor1_confirm += 1
        if sensor1_confirm >= CONFIRM_CYCLES and sensor1_time is None:
            sensor1_time = current_time
            print("🚨 Emergency detected on Lane 1")
    else:
        sensor1_confirm = 0

    # ---------------- Sensor 2 ----------------
    if sensor2 > THRESHOLD:
        sensor2_confirm += 1
        if sensor2_confirm >= CONFIRM_CYCLES and sensor2_time is None:
            sensor2_time = current_time
            print("🚨 Emergency detected on Lane 2")
    else:
        sensor2_confirm = 0

    # ---------------- Decision Logic ----------------
    if sensor1_time or sensor2_time:

        # Only lane 1
        if sensor1_time and not sensor2_time:
            priority_lane = 1

        # Only lane 2
        elif sensor2_time and not sensor1_time:
            priority_lane = 2

        # Both lanes
        else:
            if sensor1_time < sensor2_time:
                priority_lane = 1
            elif sensor2_time < sensor1_time:
                priority_lane = 2
            else:
                # Same timestamp → compare vehicle count
                v1 = get_vehicle_count(1)
                v2 = get_vehicle_count(2)
                priority_lane = 1 if v1 < v2 else 2

        # Reset detection after decision
        sensor1_time = None
        sensor2_time = None

        return {
            "status": True,
            "priority_lane": f"lane{priority_lane}"
        }

    return {
        "status": False,
        "priority_lane": None
    }
