import sys

import numpy as np
from scipy.signal import get_window, welch


def welchPSD(array, sample_f):
    f, psd = welch(array, fs=sample_f, window=get_window('hamming', 1024), nperseg=1024,
                   detrend='constant')
    return f, psd


def getstats(array, sample_f, ssvepFreq):
    freq, psd = welchPSD(array, sample_f=sample_f);
    psd = psd[(freq > 1) & (freq < 50)]
    freq = freq[(freq > 1) & (freq < 50)]
    avg = np.average(psd)
    id1 = np.where(freq > ssvepFreq - .2);
    id2 = np.where(freq > ssvepFreq + .2);
    sys.stdout.write("test" + id1 + id2)
    psdband = psd[id1[0][0]:id2[0][0]]
    maxval = np.max(psdband)
    maxindex = np.where(psd == maxval);
    divide = maxval / avg
    return divide


def calculatePSD(array, sample_f):
    ps = np.abs(np.fft.fft(array)) ** 2
    time_step = 1 / sample_f
    freqs = np.fft.fftfreq(len(array), time_step)
    idx = np.argsort(freqs)
    return freqs[idx], ps[idx]


def welchPSD(array, sample_f):
    f, psd = welch(array, fs=sample_f, window=get_window('hamming', 1024), nperseg=1024,
                   detrend='constant')
    return f, psd


# Calculate PSD using FFT
def fftPSDBands(array, sample_f):
    ps = np.abs(np.fft.fft(array)) ** 2
    time_step = 1 / sample_f
    freqs = np.fft.fftfreq(len(array), time_step)
    idx = np.argsort(freqs)
    betaSum = 0
    smrSum = 0
    thetaSum = 0
    for i in range(len(freqs)):
        if ((freqs[i] > 15) and (freqs[i] < 20)):
            # print("psd is ",ps[i],freqs[i])
            betaSum += ps[i]

    for i in range(len(freqs)):
        if ((freqs[i] > 12) and (freqs[i] < 15)):
            smrSum += ps[i]

    for i in range(len(freqs)):
        if ((freqs[i] > 4) and (freqs[i] < 7)):
            thetaSum += ps[i]

    return freqs[idx], ps[idx], betaSum, smrSum, thetaSum
