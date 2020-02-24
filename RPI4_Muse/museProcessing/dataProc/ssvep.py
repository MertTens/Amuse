import numpy as np

from museProcessing.dataProc.psd import calculatePSD


def getSSVEPPower(array, sample_f, ssvepFreq):
    # Get the Power Spectral Density
    # freq,psd=welchPSD(array, sample_f=sample_f);
    freq, psd = calculatePSD(np.array(array), sample_f=int(sample_f));
    psd = psd[(freq > 1) & (freq < 30)]
    freq = freq[(freq > 1) & (freq < 30)]

    # Calculate the power at our desired SSVEP Frequency (ssvepFreq)
    avg = np.average(psd)
    id1 = np.where(freq > ssvepFreq - .25)
    id2 = np.where(freq > ssvepFreq + .25)
    psdband = psd[id1[0][0]:id2[0][0]]
    maxval = np.max(psdband)
    maxindex = np.where(psd == maxval);
    avg -= (maxval / len(freq))
    divide = maxval / avg
    return divide


def processSSVEP(d5, samplingFreq, SSVEPFreq):
    ssvepValue = getSSVEPPower(d5, samplingFreq, SSVEPFreq)
    # print("ssvep Value at 15 hz:",ssvepValue)
    return ssvepValue
