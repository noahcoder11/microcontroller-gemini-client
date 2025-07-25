from serial import Serial
from serial.tools import list_ports
import numpy as np
import time
import resampy
from math import sqrt
from typing import Union
import wave

def select_serial_port(default: Union[int, None] = None):
    ports = list_ports.comports()
    if default:
        print('Using default serial port {}'.format(default))
        return ports[default]

    print('Please select a serial port:')
    
    print('\n'.join(f'{i}: {port.device} - {port.description}' for i, port in enumerate(ports)))

    return ports[int(input('Enter the number of the port you want to use: '))]

BYTES_TO_READ = 96000
BAUD_RATE = 115200

SELECTED_PORT = select_serial_port()

serial = Serial(port=SELECTED_PORT.device, baudrate=BAUD_RATE, timeout=None)
serial.flush()
serial.reset_input_buffer()

volumeFactor = 4
multiplier = pow(2, (sqrt(sqrt(sqrt(volumeFactor))) * 192 - 192)/6)

go_ahead = input('Press [ENTER] to read data')

serial.write('r'.encode('utf-8'))

# Now the device will send audio data
data = serial.read(BYTES_TO_READ)
print(f'Read {len(data)} bytes from serial port.')

if len(data) % 2 != 0:
    print('Warning: Data length is not even, last byte will be ignored.')
    data = data[:-1]

d_type = np.dtype(np.uint16).newbyteorder('<')
np_data = np.frombuffer(data, dtype=d_type).astype(np.int16)
np.multiply(np_data, multiplier, out=np_data, casting='unsafe')

np_data = np_data - (2048 - 150)
print(len(np_data), 'samples read.')
print('Data read successfully. Processing data...')

# Data seems to be around 6500 Hz, so let's upsample to 16000
new_data = resampy.resample(np_data, 6500, 16000)
np_data = new_data * 32767
np_data = np_data.astype(np.int16)

# new_data = np.array([ np.arange(len(np_data)), np_data ]).T

# np.savetxt('data.csv', new_data, delimiter=',', header='Index,Value', comments='', fmt='%d')
with wave.open('output.wav', 'wb') as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)  # 16-bit samples
    wav_file.setframerate(16000)
    wav_file.writeframes(np_data.tobytes())


serial.close()
print('Serial port closed.')
print('Done.') 