# ECE 69500 Hardware-Software Security Semester Project: GPS Spoofing

We will use a HackRF One to spoof GPS signals.

# Tool Setup
The following commands are meant for MacOS. Follow the instructions to set up the required dependencies to run our project scripts.

Install the Hack RF Tools software package that provides commandline-utilities.

```sh
brew install hackrf
```

Run the following using pip to install a Cython wrapper for the HackRF.
```sh
python3 -m pip install python_hackrf
```

The GPS-SDR-SIM open-source tool is used to generated a binary file of 8-bit IQ samples based on a given CSV file of latitude, longitude, altitude coordinates. The GNSS-SDR open-source tool is used to verify the IQ binary files, output on the terminal the coordinates it is receiving. The /Executables folder contains the executables to run these two pieces of software without needing to downloading the entire repository and its dependencies.

The satellite ephemeris data binary file contains a days worth of GPS satellite position and velocity data, which is used by GPS-SDR-SIM to compute the simulated GPS signals received at a given coordinate on Earth.

Once you have a CSV with coordinates you want to generate IQ samples for and begin delivering on the HackRF, run the following command:
```sh
python3 full_tx_pipeline.py CSV_FILE_PATH
```

The IQ binary file will be generated, and you will be prompted on whether you want to transfer those IQ samples to the HackRF for transmission. 

# Interfacing with Paper's Algorithm
Download original route from Google Maps or similar direction service. Decide on a spoofed route. Generate coordinates necessary to spoof receiver into taking the spoofed route. Place these coordinates into a CSV. 

# Resources
Hack RF One: https://greatscottgadgets.com/hackrf/one/

HackRF One Hardware and Software Repo: https://github.com/greatscottgadgets/hackrf

HackRF Documentation: https://hackrf.readthedocs.io/en/latest/index.html

Cython wrapper for HackRF: https://github.com/GvozdevLeonid/python_hackrf

Using HackRF One with Python API: https://pysdr.org/content/hackrf

Paper using GPS-SDR-SIM: https://ieeexplore.ieee.org/document/11031326

GPS-SDR-SIM Repo and Instructions: https://github.com/osqzss/gps-sdr-sim/tree/master

Instructions to download dependencies for GNSS-SDR: https://github.com/gnss-sdr/gnss-sdr#homebrew

Instructions to seting up GNSS-SDR by cloning repo: https://gnss-sdr.org/build-and-install/


