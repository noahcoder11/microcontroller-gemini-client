from serial import Serial
from serial.tools import list_ports
import numpy as np
import time

BYTES_TO_READ = 20
BAUD_RATE = 115200

print('Please select a serial port:')
ports = list_ports.comports()
print('\n'.join(f'{i}: {port.device} - {port.description}' for i, port in enumerate(ports)))

selected_port = int(input('Enter the number of the port you want to use: '))

serial = Serial(port=ports[selected_port].device, baudrate=BAUD_RATE, timeout=1)
serial.reset_input_buffer()
time.sleep(1)
print('Reading serial data...')

data = serial.read(BYTES_TO_READ)
d_type = np.dtype(np.uint16).newbyteorder('<')
np_data = np.frombuffer(data, dtype=d_type).astype(np.int16)

np_data = np_data - 2048

print('Number of bytes read:', len(data))
print('Numpy format: ', len(np_data))
print('Numpy data:', np_data)

print('BYTES:')
print('\n'.join([f'{byte:08b}' for byte in data]))

with open('output.bin', 'w') as f:
    out_string = '\n'.join([np.binary_repr(byte, width=16) for byte in np_data])
    f.write(out_string)

serial.close()
print('Serial port closed.')
print('Done.') 