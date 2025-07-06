from serial import Serial
from serial.tools import list_ports
import numpy as np

BYTES_TO_READ = 20
BAUD_RATE = 115200

print('Please select a serial port:')
ports = list_ports.comports()
print('\n'.join(f'{i}: {port.device} - {port.description}' for i, port in enumerate(ports)))

selected_port = int(input('Enter the number of the port you want to use: '))

serial = Serial(port=ports[selected_port].device, baudrate=BAUD_RATE, timeout=1)

print('Reading serial data...')

data = serial.read(BYTES_TO_READ)
np_data = np.frombuffer(data, dtype=np.uint16)

print('Number of bytes read:', len(data))
print('Numpy format: ', len(np_data))

with open('output.bin', 'wb') as f:
    f.write(data)

serial.close()
print('Serial port closed.')
print('Done.') 