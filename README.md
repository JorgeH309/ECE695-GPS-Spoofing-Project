



brew install hackrf for CLI, also dependency for HackRF cython wrapper
pip instal python_hackrf




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
