import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt

#%matplotlib tk

CHUNK = 1024 * 4 # Audio samples per frame
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = False,
    frames_per_buffer = CHUNK
)

fig,  ax = plt.subplots()

x = np.arange(0, 2*CHUNK, 2)
line, = ax.plot(x, np.random.rand(CHUNK))

while True:
    data = stream.read(CHUNK, exception_on_overflow = False)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] 
    print(np.mean(data_int))
