#!/usr/bin/env python3
"""
Loads an rtl_sdr capture of a known CW tone, finds its actual frequency
via FFT, and reports how far off it landed from the tuned center frequency --
this is the COMBINED HackRF + RTL-SDR residual oscillator error.
"""
import sys
import numpy as np


def main():
    if len(sys.argv) != 4:
        print("usage: analyze_offset.py <capture_file> <sample_rate> <center_freq>")
        sys.exit(1)

    capture_file = sys.argv[1]
    fs = float(sys.argv[2])
    center_freq = float(sys.argv[3])
    tone_offset_hz = 100_000.0  # must match TONE_OFFSET_HZ in gen_cw.py

    raw = np.fromfile(capture_file, dtype=np.uint8)
    if len(raw) == 0:
        print("ERROR: capture file is empty -- did rtl_sdr actually run?")
        sys.exit(1)

    # rtl_sdr output is unsigned 8-bit, centered at 127.5
    iq = raw.astype(np.float32) - 127.5
    i = iq[0::2]
    q = iq[1::2]
    samples = i + 1j * q

    # quick clipping sanity check
    clipped = np.sum((raw == 0) | (raw == 255))
    clip_pct = 100 * clipped / len(raw)
    if clip_pct > 0.1:
        print(f"WARNING: {clip_pct:.2f}% of samples sit at rail values (0 or 255).")
        print("          Signal may be clipping -- reduce HACKRF_TX_GAIN or add attenuation.")
        print()

    n = len(samples)
    window = np.hanning(n)
    spectrum = np.fft.fftshift(np.fft.fft(samples * window))
    freqs = np.fft.fftshift(np.fft.fftfreq(n, d=1 / fs))

    # Exclude a window around 0 Hz: RTL-SDR/R820T direct-conversion tuners commonly
    # show a spurious DC/LO-leakage spike there, unrelated to any real signal.
    # Our deliberate tone sits near +tone_offset_hz, so we search near there instead.
    search_mask = np.abs(freqs - tone_offset_hz) < (fs * 0.05)
    if not np.any(search_mask):
        print(f"ERROR: expected tone near +{tone_offset_hz / 1e3:.0f} kHz is outside this "
              f"capture's frequency span -- check sample rate / tone_offset_hz match.")
        sys.exit(1)

    dc_exclude = np.abs(freqs) < 2000  # mask out +/-2 kHz around DC
    search_spectrum = np.where(search_mask & ~dc_exclude, np.abs(spectrum), 0)

    peak_idx = np.argmax(search_spectrum)
    peak_freq_found = freqs[peak_idx]
    offset_hz = peak_freq_found - tone_offset_hz  # deviation from where the tone SHOULD be
    peak_mag = np.abs(spectrum[peak_idx])
    noise_floor = np.median(np.abs(spectrum[~dc_exclude]))
    snr_db = 20 * np.log10((peak_mag + 1e-12) / (noise_floor + 1e-12))

    dc_spike_mag = np.max(np.abs(spectrum[dc_exclude]))
    dc_spike_db = 20 * np.log10((dc_spike_mag + 1e-12) / (noise_floor + 1e-12))
    if dc_spike_db > 20:
        print(f"NOTE: a DC spike was seen at 0 Hz ({dc_spike_db:.1f} dB above noise) -- "
              f"this is normal RTL-SDR/R820T behavior and has been excluded from the result below.")
        print()

    ppm_equivalent = (offset_hz / center_freq) * 1e6

    print(f"Tone expected at +{tone_offset_hz / 1e3:.0f} kHz, found at "
          f"{peak_freq_found / 1e3:+.3f} kHz -- deviation: {offset_hz:+.1f} Hz")
    print(f"(This deviation is what reflects tuned center {center_freq / 1e6:.6f} MHz error.)")
    print(f"Peak SNR above noise floor: {snr_db:.1f} dB")
    print(f"Equivalent combined TX+RX ppm error: {ppm_equivalent:+.2f} ppm")
    print()
    if snr_db < 15:
        print("NOTE: low SNR -- tone may be too weak/strong or buried in noise.")
        print("      Check your coax connection, attenuation, and HACKRF_TX_GAIN.")
    print("Add this offset (in ppm) to your current RTL-SDR -p value and re-test")
    print("your real GNSS-SDR capture to see if the discriminator cleans up.")


if __name__ == "__main__":
    main()