import spidev
import numpy as np
import time
from collections import deque

# ---------------- SPI SETUP ----------------
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

# ---------------- FFT PARAMETERS ----------------
Fs = 4000
N = 1024

# ---------------- Siren Detection Parameters ----------------
INTENSITY_THRESHOLD = 400     # Above ~400 for ambulance siren
FREQ_LOW = 1000               # Hz
FREQ_HIGH = 1500              # Hz
DURATION_THRESHOLD = 1.0      # seconds
HISTORY_WINDOW = 4             # Number of FFT windows to confirm sustained siren

freq_history = deque(maxlen=HISTORY_WINDOW)
time_history = deque(maxlen=HISTORY_WINDOW)

def detect_siren():
    samples = []
    start_time = time.time()

    # Read N samples from ADC
    for i in range(N):
        samples.append(read_channel(0))
        while time.time() - start_time < (i + 1) / Fs:
            pass

    signal = np.array(samples) - np.mean(samples)
    intensity = np.max(signal)

    fft_values = np.fft.fft(signal)
    freqs = np.fft.fftfreq(N, 1 / Fs)
    magnitude = np.abs(fft_values)

    # Peak frequency in positive range
    peak_index = np.argmax(magnitude[:N//2])
    peak_freq = abs(freqs[peak_index])

    # Debug print
    print(f"Raw Intensity: {intensity:.2f}, Peak Frequency: {peak_freq:.1f} Hz")

    # Store in history
    current_time = time.time()
    freq_history.append(peak_freq)
    time_history.append(current_time)

    # Check intensity and frequency band
    if intensity < INTENSITY_THRESHOLD or not (FREQ_LOW <= peak_freq <= FREQ_HIGH):
        return False

    # Need enough history to check duration
    if len(freq_history) < HISTORY_WINDOW:
        return False

    # Duration check
    time_range = time_history[-1] - time_history[0]

    # Oscillation check: peak freq should stay in siren band
    freq_array = np.array(freq_history)
    if np.all((freq_array >= FREQ_LOW) & (freq_array <= FREQ_HIGH)) and time_range >= DURATION_THRESHOLD:
        print(f"🚨 Ambulance Siren Detected! Duration: {time_range:.2f}s")
        return True

    return False

# ---------------- MAIN LOOP ----------------
try:
    print("🔊 Starting emergency vehicle detection. Press Ctrl+C to exit.")
    while True:
        detect_siren()
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting program.")
    spi.close()