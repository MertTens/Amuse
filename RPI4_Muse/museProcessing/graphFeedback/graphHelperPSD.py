# Basically graphHelper.py, but tweaked for Power Spectral Density

import matplotlib.animation as animation
import matplotlib.pyplot as plt

channels = ["TP9", "AF7", "AF8", "TP10", "Oz"];


# Initialize communication with TMP102
# This function is called periodically from FuncAnimation
def animatePSD(i, xdata, ydata, axis):
    eegName = channels[4]
    # print("Freq = {0}-{1}Hz".format(xdata[0],xdata[-1]))
    plotSubPlot(axis, xdata, ydata, eegName);


def plotSubPlot(axis, xdata, ydata, eegName):
    axis.clear()
    axis.set_ylabel('EEG: ' + channels[4]);
    axis.set_xlabel('Frequency (Hz)');
    axis.plot(xdata, ydata)
    if (all(i > 0 for i in ydata)):  # log scale only if there are no negatives & zeroes
        axis.set_yscale('log')
        axis.set_ylim([10 ** 1, 10 ** 11]);


def initAnim(xdata, ydata):
    # Set up plot to call animate() function periodically
    figPSD, axisPSD = plt.subplots(1, 1, sharex=True, num="EEG Plots")
    ani = animation.FuncAnimation(figPSD, animatePSD, fargs=([xdata, ydata, axisPSD]),
                                  interval=100)
    plt.show()
