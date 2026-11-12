
import numpy as np
import subprocess
from pathlib import Path

# -----------------------------
# Transmission configuration
# -----------------------------
CENTER_FREQ = 915_000_000   # 915 MHz
SAMPLE_RATE = 2_500_000     # 2.5 MS/s
TONE_FREQ = 100_000         # +100 kHz baseband offset
DURATION = 20               # seconds
AMPLITUDE = 30           # int8 amplitude; maximum is 127

OUTPUT_FILE = Path("known_tone.iq")

# -----------------------------
# Generate complex sinusoid
# -----------------------------
num_samples = int(SAMPLE_RATE * DURATION)

t = np.arange(num_samples) / SAMPLE_RATE

iq = AMPLITUDE * np.exp(1j * 2 * np.pi * TONE_FREQ * t)

# HackRF expects signed 8-bit interleaved I/Q
I = np.clip(np.real(iq), -127, 127).astype(np.int8)
Q = np.clip(np.imag(iq), -127, 127).astype(np.int8)

interleaved = np.empty(2 * num_samples, dtype=np.int8)
interleaved[0::2] = I
interleaved[1::2] = Q

interleaved.tofile(OUTPUT_FILE)

print(f"Generated: {OUTPUT_FILE}")
print(f"Samples: {num_samples:,}")
print(f"Duration: {DURATION} seconds")
print(f"Center frequency: {CENTER_FREQ / 1e6} MHz")
print(f"Tone frequency: {(CENTER_FREQ + TONE_FREQ) / 1e6} MHz")

# -----------------------------
# Transmit with HackRF
# -----------------------------
command = [
    "hackrf_transfer",
    "-t", str(OUTPUT_FILE),
    "-f", str(CENTER_FREQ),
    "-s", str(SAMPLE_RATE),
    "-x", "10",       # TX VGA gain: 0 dB
    "-a", "0",       # TX amplifier disabled
]

print("\nStarting HackRF transmission...")
subprocess.run(command, check=True)
