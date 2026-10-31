
import time
import numpy as np
from rtlsdr import RtlSdr

# -----------------------------
# Capture configuration
# -----------------------------
CENTER_FREQ = 1575.42e6  # GPS L1 frequency (Hz)
SAMPLE_RATE = 2.5e6      # 2.5 MS/s
DURATION = 60            # Capture duration (seconds)
OUTPUT_FILE = "rtl_gps_l1.bin"
FREQ_CORRECTION = 0      # RTL-SDR frequency correction (PPM)

# Number of complex samples per read
CHUNK_SAMPLES = 256_000


def main():
    sdr = RtlSdr()

    try:
        # Configure RTL-SDR
        sdr.sample_rate = SAMPLE_RATE
        sdr.center_freq = CENTER_FREQ
        sdr.freq_correction = FREQ_CORRECTION

        # Choose a supported manual gain near 40 dB
        available_gains = sdr.get_gains()
        gain = min(available_gains, key=lambda g: abs(g - 40.0))
        sdr.gain = gain

        print("RTL-SDR configured:")
        print(f"  Center frequency: {CENTER_FREQ / 1e6:.3f} MHz")
        print(f"  Sample rate:      {SAMPLE_RATE / 1e6:.2f} MS/s")
        print(f"  Gain:             {gain} dB")
        print(f"  Duration:         {DURATION} seconds")
        print(f"  Output:           {OUTPUT_FILE}")

        total_samples = int(SAMPLE_RATE * DURATION)
        samples_written = 0

        start_time = time.time()

        with open(OUTPUT_FILE, "wb") as file:
            while samples_written < total_samples:
                count = min(
                    CHUNK_SAMPLES,
                    total_samples - samples_written
                )

                # Read unsigned 8-bit interleaved I/Q bytes
                raw = sdr.read_bytes(2 * count)
                raw = np.frombuffer(raw, dtype=np.uint8)

                # Convert unsigned [0, 255] to signed [-128, 127]
                iq = np.rint(
                    raw.astype(np.float32) - 127.5
                ).astype(np.int8)

                file.write(iq.tobytes())
                samples_written += len(iq) // 2

                progress = 100 * samples_written / total_samples
                print(
                    f"\rProgress: {progress:6.2f}%",
                    end="",
                    flush=True
                )

        elapsed = time.time() - start_time

        print("\n\nCapture complete.")
        print(f"Samples captured: {samples_written:,}")
        print(f"Elapsed time:     {elapsed:.2f} seconds")
        print(f"File size:        {2 * samples_written:,} bytes")

    except KeyboardInterrupt:
        print("\nCapture interrupted.")

    finally:
        sdr.close()


if __name__ == "__main__":
    main()

