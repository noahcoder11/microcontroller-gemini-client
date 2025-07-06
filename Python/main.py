from serial import Serial
from serial.tools import list_ports
import numpy as np
import time
import wave

BYTES_TO_READ = 96000
BAUD_RATE = 115200

print('Please select a serial port:')
ports = list_ports.comports()
print('\n'.join(f'{i}: {port.device} - {port.description}' for i, port in enumerate(ports)))

selected_port = int(input('Enter the number of the port you want to use: '))

serial = Serial(port=ports[selected_port].device, baudrate=BAUD_RATE, timeout=10)
serial.flush()
serial.reset_input_buffer()
time.sleep(5)
print('Reading serial data...')

data = serial.read(BYTES_TO_READ)
print(f'Read {len(data)} bytes from serial port.')
d_type = np.dtype(np.uint16).newbyteorder('<')
np_data = np.frombuffer(data, dtype=d_type).astype(np.int16)

np_data = np_data - (2048 - 150)
print(len(np_data), 'samples read.')
print('Data read successfully. Processing data...')

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