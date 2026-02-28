import os
from ultralytics import YOLO

SAVE_DIR = "/home/pi/Pictures/pi_dual_camera"
MODEL_PATH = "/home/pi/Desktop/model.pt"
RESULT_FILE = "/home/pi/Desktop/traffic_result.txt"

print("Loading YOLO model...")
model = YOLO(MODEL_PATH)

def count_vehicles(img_path):
    results = model(img_path, conf=0.4, device="cpu", verbose=False)
    return len(results[0].boxes)

# Get captured images
images = sorted([f for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")])

if len(images) < 4:
    print("Not enough images found. Run capture script first.")
    exit()

lane_counts = {}

print("\nAnalyzing images...\n")

for img in images[:4]:
    img_path = os.path.join(SAVE_DIR, img)
    lane_name = img.split("_")[0]   # lane1, lane2, etc.

    count = count_vehicles(img_path)
    lane_counts[lane_name] = count

    print(f"{lane_name}: {count}")

    # Delete image after processing
    os.remove(img_path)

# Save ALL lane results to file
with open(RESULT_FILE, "w") as f:
    for lane, count in lane_counts.items():
        f.write(f"{lane},{count}\n")

print("\nResults saved to traffic_result.txt")

# Show highest lane (for display only)
max_lane = max(lane_counts, key=lane_counts.get)
max_count = lane_counts[max_lane]

print("\nHIGHEST:", max_lane)
print("COUNT:", max_count)