
import numpy as np

FILES = [
    "known_tone.iq",
    "./IQFiles/50gain_signed.bin"
]

for filename in FILES:
    data = np.fromfile(filename, dtype=np.int8)

    I = data[0::2].astype(np.float64)
    Q = data[1::2].astype(np.float64)

    print(f"\n{filename}")
    print(f"I mean:       {np.mean(I):.3f}")
    print(f"Q mean:       {np.mean(Q):.3f}")
    print(f"I RMS:        {np.sqrt(np.mean(I**2)):.3f}")
    print(f"Q RMS:        {np.sqrt(np.mean(Q**2)):.3f}")
    print(f"I peak:       {np.max(np.abs(I)):.0f}")
    print(f"Q peak:       {np.max(np.abs(Q)):.0f}")
    print(f"Clipped I:    {np.sum(np.abs(I) >= 127):,}")
    print(f"Clipped Q:    {np.sum(np.abs(Q) >= 127):,}")
    print(f"IQ power:     {np.mean(I**2 + Q**2):.3f}")



import matplotlib.pyplot as plt

data = np.fromfile(
    "./IQFiles/evenlargergain_signed.bin",
    dtype=np.int8
)

I = data[0::2].astype(np.float32)
Q = data[1::2].astype(np.float32)

iq = I + 1j * Q

# Remove DC
iq -= np.mean(iq)

# FFT
N = min(len(iq), 250000)
spectrum = np.fft.fftshift(np.fft.fft(iq[:N] * np.hanning(N)))
freq = np.fft.fftshift(np.fft.fftfreq(N, d=1/2_500_000))

power_db = 20 * np.log10(np.abs(spectrum) + 1e-12)

plt.figure(figsize=(10, 5))
plt.plot(freq / 1e3, power_db)
plt.xlabel("Frequency (kHz)")
plt.ylabel("Magnitude (dB)")
plt.title("RTL-SDR Received Tone Spectrum")
plt.grid()
plt.show()

