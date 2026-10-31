
import subprocess
from pathlib import Path


class HackRFTransmitter:
    def __init__(
        self,
        sample_rate=2_500_000,
        frequency=1_575_420_000,
        tx_gain=0,
        amp_enable=False,
        antenna_enable=False,
    ):
        self.sample_rate = sample_rate
        self.frequency = frequency
        self.tx_gain = tx_gain
        self.amp_enable = amp_enable
        self.antenna_enable = antenna_enable

    def transmit_file(self, bin_path):
        """Transmit an IQ file using hackrf_transfer."""
        bin_path = Path(bin_path)

        if not bin_path.is_file():
            raise FileNotFoundError(f"IQ file not found: {bin_path}")

        if bin_path.stat().st_size == 0:
            raise ValueError("IQ file is empty.")

        command = [
            "hackrf_transfer",
            "-t", str(bin_path),
            "-f", str(self.frequency),
            "-s", str(self.sample_rate),
            "-x", str(self.tx_gain),
            "-a", "1" if self.amp_enable else "0",
            "-p", "1" if self.antenna_enable else "0",
        ]

        print("Starting HackRF transmission...")
        print(f"File: {bin_path}")
        print(f"Frequency: {self.frequency / 1e6:.3f} MHz")
        print(f"Sample rate: {self.sample_rate / 1e6:.1f} MS/s")

        try:
            subprocess.run(command, check=True)
        except FileNotFoundError:
            raise RuntimeError(
                "hackrf_transfer was not found. "
                "Make sure HackRF tools are installed and in PATH."
            )
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                f"hackrf_transfer failed with exit code {exc.returncode}"
            ) from exc

        print("HackRF transmission finished.")

    def close(self):
        """No persistent Python device handle needs closing."""
        print("No Python-managed HackRF instance is open.")


if __name__ == "__main__":
    transmitter = HackRFTransmitter(
        sample_rate=2_500_000,
        frequency=1_575_420_000,
        tx_gain=0,
    )

    try:
        transmitter.transmit_file("gpssim.bin")
    finally:
        transmitter.close()
