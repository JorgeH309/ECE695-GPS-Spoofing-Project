
import numpy as np

FS = 2_000_000
N = 20_000_000

def save_iq(filename, signal):
    # Normalize to avoid clipping
    signal = signal / np.max(np.abs(signal)) * 0.6

    iq = np.empty(2 * len(signal), dtype=np.int8)
    iq[0::2] = np.round(signal.real * 127).astype(np.int8)
    iq[1::2] = np.round(signal.imag * 127).astype(np.int8)

    iq.tofile(filename)


# --------------------------------
# Signal 1: Five simultaneous tones
# --------------------------------

t = np.arange(N) / FS

frequencies = [-200e3, -100e3, 0, 100e3, 200e3]

multitone = sum(
    np.exp(2j * np.pi * f * t)
    for f in frequencies
)

save_iq("multitone.iq", multitone)


# --------------------------------
# Signal 2: Band-limited noise
# --------------------------------

freq = np.fft.fftfreq(N, d=1/FS)

spectrum = np.zeros(N, dtype=complex)
mask = np.abs(freq) <= 400e3

rng = np.random.default_rng(42)
spectrum[mask] = (
    rng.normal(size=np.sum(mask))
    + 1j * rng.normal(size=np.sum(mask))
)

wideband = np.fft.ifft(spectrum)

save_iq("wideband.iq", wideband)

print("Generated multitone.iq and wideband.iq")
