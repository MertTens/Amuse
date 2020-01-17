import numpy as np
from scipy.io.wavfile import write

sps = 44100 # samples per second

freq_hz = 440.0

duration_s = 5.0

each_sample_number = np.arange(duration_s * sps)
waveform = np.sin(2*np.pi * each_sample_number * freq_hz / sps)
waveform_quiet = waveform * 0.3
waveform_integers = np.int16(waveform_quiet * 32767)
write('first_sine_wave.wav', sps, waveform_integers)
