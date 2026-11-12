
import subprocess
from pathlib import Path

# -----------------------------
# Capture configuration
# -----------------------------
CENTER_FREQ = 1_575_420_000  # GPS L1 (Hz)
SAMPLE_RATE = 2_500_000      # 2.5 MS/s
DURATION = 60                # seconds 
GAIN = 1                    # dB; adjust to supported tuner gain
FREQ_CORRECTION = -2          # PPM
OUTPUT_FILE = Path("rtl_gps_l1.bin")


def main():
    total_samples = SAMPLE_RATE * DURATION

    command = [
        "rtl_sdr",
        "-f", str(CENTER_FREQ),
        "-s", str(SAMPLE_RATE),
        "-g", str(GAIN),
        "-p", str(FREQ_CORRECTION),
        "-n", str(total_samples),
        str(OUTPUT_FILE),
    ]

    print("Starting RTL-SDR capture...")
    print(f"Frequency:   {CENTER_FREQ / 1e6:.3f} MHz")
    print(f"Sample rate: {SAMPLE_RATE / 1e6:.2f} MS/s")
    print(f"Duration:    {DURATION} seconds")
    print(f"Output:      {OUTPUT_FILE}")

    try:
        subprocess.run(command, check=True)

    except FileNotFoundError:
        raise RuntimeError(
            "rtl_sdr was not found. Install it with: brew install librtlsdr"
        )

    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"RTL-SDR capture failed: exit code {exc.returncode}"
        ) from exc

    print("\nCapture complete.")
    print(f"File size: {OUTPUT_FILE.stat().st_size:,} bytes")
    print(f"Expected size: {2 * total_samples:,} bytes")


if __name__ == "__main__":
    main()
