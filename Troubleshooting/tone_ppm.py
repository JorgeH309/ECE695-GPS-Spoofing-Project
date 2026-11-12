#!/usr/bin/env python3
"""
Generates a pure continuous-wave (CW) tone as a HackRF-compatible
signed 8-bit interleaved IQ file. Transmitting a constant (I, Q) value
puts all the transmitted energy exactly at the HackRF's tuned center
frequency -- which is what makes this a clean calibration reference.
"""
import numpy as np

NUM_SAMPLES = 1_000_000   # repeated via hackrf_transfer -R, so length just sets loop granularity
AMPLITUDE = 80            # keep well under full-scale (127) to avoid clipping/distortion
SAMPLE_RATE = 8_000_000   # must match HACKRF_SAMPLE_RATE in calibrate_ppm.sh
TONE_OFFSET_HZ = 100_000  # offset from center -- keeps the tone clear of the RTL-SDR's DC spike
OUT_FILE = "cw_tone.iq8"

t = np.arange(NUM_SAMPLES) / SAMPLE_RATE
phase = 2 * np.pi * TONE_OFFSET_HZ * t
i = (AMPLITUDE * np.cos(phase)).astype(np.int8)
q = (AMPLITUDE * np.sin(phase)).astype(np.int8)

iq = np.empty(NUM_SAMPLES * 2, dtype=np.int8)
iq[0::2] = i
iq[1::2] = q

iq.tofile(OUT_FILE)
print(f"Wrote {len(iq)} bytes ({NUM_SAMPLES} samples) to {OUT_FILE}")