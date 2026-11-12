import numpy as np
from pathlib import Path
# RTLSDR reads unsigned 8-bit interleaved IQ data
input_file = Path("./IQFiles/rtl_gps_l1.bin")
output_file = Path("./IQFiles/rtl_gps_l1_signed.bin")

# Read unsigned 8-bit interleaved IQ
iq_unsigned = np.fromfile(input_file, dtype=np.uint8)

# Convert unsigned [0, 255] to signed [-128, 127]
iq_signed = (iq_unsigned.astype(np.int16) - 128).astype(np.int8)

# Save signed interleaved IQ
iq_signed.tofile(output_file)

print(f"Converted {len(iq_signed):,} bytes")
print(f"Output: {output_file}")