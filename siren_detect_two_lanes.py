import spidev
import time
from datetime import datetime

# ================= SPI SETUP =================
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# ================= CONFIG =================
THRESHOLD = 600
CHECK_INTERVAL = 0.2

sensor1_time = None
sensor2_time = None

# ================= FUNCTIONS =================

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def read_average(channel, samples=5):
    total = 0
    for _ in range(samples):
        total += read_channel(channel)
    return total // samples

def get_vehicle_count(lane_number):
    try:
        with open("/home/pi/Desktop/traffic_result.txt", "r") as f:
            data = f.read().strip()
            lane_name, vehicle_count = data.split(",")
            return int(vehicle_count)
    except:
        return 0

# ================= MAIN LOOP =================

print("Monitoring for Emergency Sirens...")

while True:

    sensor1 = read_average(0)
    sensor2 = read_average(1)

    current_time = datetime.now()

    # Detect Sensor 1
    if sensor1 > THRESHOLD and sensor1_time is None:
        sensor1_time = current_time
        print("Emergency detected on Lane 1 at", sensor1_time)

    # Detect Sensor 2
    if sensor2 > THRESHOLD and sensor2_time is None:
        sensor2_time = current_time
        print("Emergency detected on Lane 2 at", sensor2_time)

    # If any emergency detected
    if sensor1_time or sensor2_time:

        # Only Lane 1 detected
        if sensor1_time and not sensor2_time:
            priority_lane = 1

        # Only Lane 2 detected
        elif sensor2_time and not sensor1_time:
            priority_lane = 2

        # Both detected
        else:
            if sensor1_time < sensor2_time:
                priority_lane = 1
            elif sensor2_time < sensor1_time:
                priority_lane = 2
            else:
                # Same timestamp → compare vehicle count
                v1 = get_vehicle_count(1)
                v2 = get_vehicle_count(2)

                if v1 < v2:
                    priority_lane = 1
                else:
                    priority_lane = 2

        print(f"Priority given to Lane {priority_lane}")

        # Reset after handling
        sensor1_time = None
        sensor2_time = None

        # Here you call your traffic control logic
        # Example:
        # set_green(priority_lane)

    time.sleep(CHECK_INTERVAL)