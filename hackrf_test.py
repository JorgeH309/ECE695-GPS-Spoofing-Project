from python_hackrf import pyhackrf

pyhackrf.pyhackrf_init()

sdr = pyhackrf.pyhackrf_open()
print("HackRF device opened successfully.")
sdr.pyhackrf_set_sample_rate(10e6)
sdr.pyhackrf_set_antenna_enable(False)
sdr.pyhackrf_set_freq(100e6)
sdr.pyhackrf_set_amp_enable(False)
sdr.pyhackrf_set_lna_gain(30) # LNA gain - 0 to 40 dB in 8 dB steps
sdr.pyhackrf_set_vga_gain(50) # VGA gain - 0 to 62 dB in 2 dB steps
print("HackRF device configured successfully.")
sdr.pyhackrf_close()
print("HackRF device closed successfully.")