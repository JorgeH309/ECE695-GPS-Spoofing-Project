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


