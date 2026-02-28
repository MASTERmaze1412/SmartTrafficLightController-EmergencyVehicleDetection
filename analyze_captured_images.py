# analyze_captured_images.py

import os
from ultralytics import YOLO

SAVE_DIR = "/home/pi/Pictures/pi_dual_camera"
MODEL_PATH = "/home/pi/Desktop/model.pt"

_model = None

def _get_model():
    global _model
    if _model is None:
        print("🔍 Loading YOLO model...")
        _model = YOLO(MODEL_PATH)
    return _model

def run_analysis():
    model = _get_model()

    def count_vehicles(img_path):
        results = model(img_path, conf=0.4, device="cpu", verbose=False)
        return len(results[0].boxes)

    images = sorted([f for f in os.listdir(SAVE_DIR) if f.endswith(".jpg")])

    if len(images) < 4:
        print("⚠ Not enough images found.")
        return {}

    lane_counts = {}

    print("\n🚗 Analyzing images...\n")

    # Only process the newest 4 images (recommended)
    # If you want oldest 4, keep images[:4]
    images_to_process = images[-4:]

    for img in images_to_process:
        img_path = os.path.join(SAVE_DIR, img)
        lane_name = img.split("_")[0]

        count = count_vehicles(img_path)
        lane_counts[lane_name] = count

        print(f"{lane_name}: {count}")

        # delete after analysis
        try:
            os.remove(img_path)
        except:
            pass

    max_lane = max(lane_counts, key=lane_counts.get)
    max_count = lane_counts[max_lane]

    print("\n🏆 HIGHEST:", max_lane)
    print("COUNT:", max_count)

    return lane_counts
