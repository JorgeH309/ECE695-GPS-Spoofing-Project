import numpy as np
import matplotlib.pyplot as plt

samples = np.fromfile("received.iq", dtype=np.uint8)
iq = (samples[0::2].astype(float) - 127.5) + \
     1j * (samples[1::2].astype(float) - 127.5)

N = len(iq)
spectrum = np.fft.fftshift(np.fft.fft(iq * np.hanning(N)))

freq = np.fft.fftshift(np.fft.fftfreq(N, d=1/2e6))

spectrum_db = 20 * np.log10(
    np.abs(spectrum) / np.max(np.abs(spectrum)) + 1e-12
)

plt.plot(freq / 1e3, spectrum_db)
plt.ylim(-100, 5)
plt.xlabel("Frequency offset (kHz)")
plt.ylabel("Relative magnitude (dB)")
plt.grid()
plt.show()