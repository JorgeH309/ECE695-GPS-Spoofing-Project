import argparse
import subprocess
from pathlib import Path
from hackrf_tx import HackRFTransmitter

# Configuration
GPS_SDR_SIM = "./Executables/gps-sdr-sim"
EPHEMERIS_FILE = "SatEphemerisData/brdc2950.26n"
SAMPLE_RATE = 2_500_000  # Samples per second
OUTPUT_IQ_FILE = "IQFiles/gpssim.bin"


def main():
    parser = argparse.ArgumentParser(
            description="Generate GPS IQ samples from a trajectory CSV."
        )
    parser.add_argument("csv", help="Path to the trajectory CSV file")
    args = parser.parse_args()

    csv_path = Path(args.csv)

    if not csv_path.is_file():
        print(f"Error: CSV file not found: {csv_path}")
        return

    # 2. Check required files
    if not Path(GPS_SDR_SIM).is_file():
        print(f"Error: gps-sdr-sim executable not found: {GPS_SDR_SIM}")
        return

    if not Path(EPHEMERIS_FILE).is_file():
        print(f"Error: ephemeris file not found: {EPHEMERIS_FILE}")
        return

    # 3. Generate the IQ file
    command = [
        GPS_SDR_SIM,
        "-e", EPHEMERIS_FILE,
        "-x", str(csv_path),
        "-s", str(SAMPLE_RATE),
        "-b", "8",
        "-o", OUTPUT_IQ_FILE,
    ]

    print("Generating IQ file...")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"gps-sdr-sim failed with exit code {exc.returncode}")
        return
    except OSError as exc:
        print(f"Could not run gps-sdr-sim: {exc}")
        return

    if not Path(OUTPUT_IQ_FILE).is_file():
        print("Error: IQ output file was not created.")
        return

    print(f"IQ file generated: {OUTPUT_IQ_FILE}")

    # 4. Ask whether to proceed to transmission
    answer = input(
        "Proceed with HackRF transmission in an authorized, "
        "shielded test setup? (yes/no): "
    ).strip().lower()

    if answer in ("yes", "y"):
        print(
            "Transmission requested. Before transmitting, verify that "
            "the RF output is contained in a properly shielded or "
            "conducted test setup. No transmission has been started."
        )
        hackrf = HackRFTransmitter()
        hackrf.transmit_file(OUTPUT_IQ_FILE)
    else:
        print("Transmission skipped.")


if __name__ == "__main__":
    main()