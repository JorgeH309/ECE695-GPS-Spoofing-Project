import subprocess

# uses gps-sdr-sim to generate a GPS signal IQ file based on provided parameters and satellite ephemeris data
def main():
    # GPS receiver coordinates: latitude, longitude, altitude (meters)
    location = "25.544326,-80.410226,180"

    # Input GPS broadcast ephemeris file
    ephemeris = "brdc2950.26n"

    # Simulation duration (seconds)
    duration = "60"

    # Output IQ file
    output = "gpssim.bin"

    # IQ sample rate (Hz)
    sample_rate = "2500000"

    # Quantization: 8-bit I + 8-bit Q
    iq_bits = "8"

    command = [
        "./gps-sdr-sim",
        "-e", ephemeris,
        "-l", location,
        "-d", duration,
        "-s", sample_rate,
        "-b", iq_bits,
        "-o", output,
    ]

    print("Running GPS-SDR-SIM...")
    print("Command:", " ".join(command))

    subprocess.run(command, check=True)

    print(f"Generated {output}")


if __name__ == "__main__":
    main()