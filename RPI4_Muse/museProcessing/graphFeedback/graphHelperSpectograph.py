# Basically graphHelper.py, but tweaked for Power Spectral Density

import matplotlib.animation as animation
import matplotlib.pyplot as plt

figPSD, axisPSD = plt.subplots(1, 1, sharex=True, num="EEG Plots")


def animateSpectrograph(i):
    line = PSDs[4]
    row = np.array([float(i) for i in line])
    row = np.log10(row)
    pic.append(row)
    if len(pic) > 128:
        pic.pop(0)
    axisSpectro.clear()
    axisSpectro.imshow(np.transpose(pic))
    axisSpectro.grid(False)
    axisSpectro.set_ylabel('Frequency (Hz)')
    axisSpectro.set_xlabel('Time (s)')
    locs, labels = plt.yticks()
    plt.yticks(locs, np.round(np.array(locs) / len(PSDs[4]) * FREQ_CUTOFF, 2).tolist())


def initAnim(ydata):
    # style.use('fivethirtyeight')
    figSpectro, axisSpectro = plt.subplots(1, 1, sharex=True, num="Spectrograph")
    pic = []
    ani = animation.FuncAnimation(figSpectro, animate, interval=100)


def showAnim():
    plt.show()
