# 🚦 Smart Traffic Light Controller & Emergency Vehicle Detection

An AI-powered traffic management prototype built with Raspberry Pi 5, YOLOv8, and audio signal processing. The system analyzes vehicle density at a miniature four-way intersection and prioritizes emergency detection over normal traffic processing.

### 🛠️ Technologies

- `Python`
- `Raspberry Pi 5`
- `YOLOv8` — Vehicle detection
- `OpenCV / Picamera2` — Image capture and processing
- `NumPy` — Numerical operations and FFT
- `MCP3008 ADC` — Analog audio acquisition
- `MAX4466` — Microphone amplification
- `gpiozero` — Servo control
- `SPI` — Communication with the ADC

### 🚀 Features

- Adaptive traffic signaling based on detected vehicle counts
- YOLOv8-based vehicle detection from camera images
- Two-camera setup for capturing four lanes
- Servo-assisted camera positioning
- Frequency-based emergency siren detection using FFT
- Emergency-priority logic that takes precedence over normal traffic processing
- Configurable detection thresholds and signal timings
- Modular Python implementation separating capture, analysis, audio detection, and traffic logic

### 📌 The Process

Me and team wanted to explore how computer vision and embedded systems could make traffic management more adaptive than a conventional fixed-timing approach.

The project combines two sensing methods. First, cameras capture images of the miniature intersection, and a YOLOv8 model analyzes the images to estimate vehicle counts for individual lanes. The controller then selects the lane with the highest detected count for the normal traffic cycle.

At the same time, an acoustic detection module samples microphone input through an MCP3008 ADC. FFT-based frequency analysis evaluates sound activity within a configured frequency range to identify potential emergency siren signals.

The main controller checks the emergency detection result before proceeding with normal traffic processing. This brings together computer vision, digital signal processing, and hardware integration in one prototype.

### ⏱️ Traffic Logic

| Mode | Green | Yellow |
|---|---:|---:|
| Normal traffic | 10 seconds | 3 seconds |
| Emergency priority | 20 seconds | 3 seconds |

These are prototype timing values, not validated timings for real-world intersections.

### 📂 Project Structure

```text
SmartTrafficLightController-EmergencyVehicleDetection/
├── main.py
├── capture_images.py
├── analyze_captured_images.py
├── traffic_logic.py
├── siren_detect_one_lane.py
├── siren_detect_two_lanes.py
├── proxy_traffic_logic.txt
└── README.md
```

- `main.py` — Coordinates emergency detection and normal traffic processing.
- `capture_images.py` — Captures lane images using the cameras and servo.
- `analyze_captured_images.py` — Runs YOLOv8 and calculates lane-wise detection counts.
- `traffic_logic.py` — Implements the prototype traffic-cycle logic.
- `siren_detect_one_lane.py` — Standalone single-lane audio detection.
- `siren_detect_two_lanes.py` — Two-lane audio detection interface used by the main controller.

### 📱 Running the Project

**Prerequisites**

- Raspberry Pi 5 with compatible Raspberry Pi OS
- Python 3
- Two compatible cameras
- MAX4466 microphone amplifier and MCP3008 ADC
- Servo motor and required connections
- Trained YOLOv8 model (`.pt`)

**1. Clone the repository**

```bash
git clone https://github.com/MASTERmaze1412/SmartTrafficLightController-EmergencyVehicleDetection.git

cd SmartTrafficLightController-EmergencyVehicleDetection
```

**2. Install dependencies**

Install the required system packages and Python libraries:

```bash
sudo apt update

sudo apt install python3-venv python3-picamera2 python3-gpiozero python3-numpy python3-spidev

python3 -m venv --system-site-packages .venv

source .venv/bin/activate

python -m pip install ultralytics
```

**3. Configure the model and image paths**

The image-analysis script expects a trained model at:

```text
/home/pi/Desktop/model.pt
```

The capture and analysis scripts use this image directory:

```text
/home/pi/Pictures/pi_dual_camera
```

Update these paths in the relevant Python files if your environment uses different locations.

**4. Enable SPI**

Enable SPI using the Raspberry Pi configuration utility:

```bash
sudo raspi-config
```

Verify the camera connections, servo control pin, MCP3008 wiring, and microphone input before proceeding.

**5. Run the controller**

```bash
python main.py
```

The application checks for emergency conditions before executing the normal camera-capture, vehicle-analysis, and traffic-cycle workflow.

*Note: The integrated application requires the configured hardware and trained model. It is not a standalone desktop simulation.*

### 🧪 Testing & Validation

The following scenarios can be used to evaluate the prototype:

- **Normal traffic:** Place toy vehicles in different lanes and verify the detected counts and selected lane.
- **Changing traffic density:** Change the number of vehicles in each lane and check whether the selected lane follows the highest detected count.
- **Emergency detection:** Use controlled audio test signals to evaluate the configured frequency and intensity thresholds.
- **Background noise:** Test non-siren sounds to identify false emergency detections.
- **Lighting conditions:** Evaluate vehicle detection under different lighting and occlusion conditions.
- **System stability:** Monitor processing delays, camera behavior, and resource usage during repeated cycles.

Useful evaluation metrics include vehicle-count error, lane-selection accuracy, emergency false-positive and false-negative rates, and end-to-end processing latency.

### 🔧 Hardware Considerations

- The Raspberry Pi 5 performs camera acquisition, model inference, and control logic.
- The MCP3008 communicates with the Raspberry Pi through SPI.
- The MAX4466 amplifies the analog microphone signal.
- The servo repositions the camera setup between capture positions.
- Hardware connections must respect GPIO and ADC voltage limits.

The current traffic-logic module prints signal-state transitions rather than directly driving physical traffic-light GPIO outputs. Physical signal control would require additional output circuitry, conflict prevention, and independent fail-safe mechanisms.
### 🖼️ Review




### 💡 Future Enhancements

- Improve siren recognition using trained audio classification models.
- Add emergency direction estimation to identify the approaching lane.
- Implement vehicle tracking to avoid duplicate counts.
- Optimize YOLOv8 inference for lower processing latency.
- Add a dedicated traffic simulator for hardware-independent testing.
- Implement a complete signal state machine with conflict-free transitions.
- Add automated unit, integration, and regression tests.
- Introduce structured configuration, logging, and performance monitoring.
- Develop a tested physical signal-output interface with independent safety controls.

### 📖 References

- [YOLO Documentation](https://docs.ultralytics.com/)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [Picamera2 Manual](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)
- [NumPy FFT Documentation](https://numpy.org/doc/stable/reference/routines.fft.html)
- [gpiozero Documentation](https://gpiozero.readthedocs.io/)
- [MCP3008 Documentation](https://www.microchip.com/en-us/product/MCP3008)

### ⚠️ Safety Notice

This project is an academic prototype intended for experimentation and demonstration. Frequency-based siren detection can produce false positives and missed detections, and vehicle counts may be inaccurate. The current traffic logic is not a certified traffic controller and must not be used to operate public-road signals.

### 👨‍💻 Author

Developed as an engineering project exploring **computer vision, embedded systems, digital signal processing, and adaptive traffic management**.

**Repository:** [Smart Traffic Light Controller & Emergency Vehicle Detection](https://github.com/MASTERmaze1412/SmartTrafficLightController-EmergencyVehicleDetection)
