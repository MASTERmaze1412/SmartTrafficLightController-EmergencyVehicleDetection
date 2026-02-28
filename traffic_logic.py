# traffic_logic.py

import time

def set_green(lane):
    print(f"🟢 GREEN ON: Lane {lane}")

def transition_to_yellow(lane):
    print(f"🟡 YELLOW ON: Lane {lane}")

def set_red(lane):
    print(f"🔴 RED ON: Lane {lane}")

def run_traffic_cycle(lane_counts):
    if not lane_counts:
        print("No lane data received.")
        return

    # Pick lane with highest vehicles
    priority_lane = max(lane_counts, key=lane_counts.get)

    print("\n🚦 Normal Traffic Cycle")
    print(f"Priority Lane: {priority_lane}")

    set_green(priority_lane)
    time.sleep(10)

    transition_to_yellow(priority_lane)
    time.sleep(3)

    set_red(priority_lane)
