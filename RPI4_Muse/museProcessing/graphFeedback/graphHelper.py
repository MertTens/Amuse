import matplotlib.pyplot as plt

channels = ["TP9", "AF7", "AF8", "TP10", "Oz"];

samplingFreq = 256;
samplingTimeStep = 1 / samplingFreq;
figPSD, axes = plt.subplots(5, 1, sharex=True, num="EEG Plots")
timeInterval = 2000;
arrayLen = samplingFreq * 10;


# Initialize communication with TMP102
# This function is called periodically from FuncAnimation
def animatePSD(i, ys1, ys2, ys3, ys4, ys5):
    # Limit x and y lists to 20 items
    ys1 = ys1[-arrayLen:]
    ys2 = ys2[-arrayLen:]
    ys3 = ys3[-arrayLen:]
    ys4 = ys4[-arrayLen:]
    ys5 = ys5[-arrayLen:]
    ys = [ys1, ys2, ys3, ys4, ys5];

    for k in range(len(axes)):
        plotSubPlot(axes[k], ys[k], channels[k]);

    # fig.align_ylabels()


def plotSubPlot(axis, ys, eegName):
    axis.clear();
    # axis.set_ylim([0,1600]);
    axis.plot(ys);
    # axis.set_ylabel('EEG: '+eegName);
    # axis.set_xlabel('time interval ');


def startAnim(ys1, ys2, ys3, ys4, ys5):
    # Set up plot to call animate() function periodically
    # Create figure for plotting

    for k in range(len(axes)):
        axes[k].set_ylim([0, 1600]);
        axes[k].set_ylabel('EEG: ' + channels[k]);
        axes[k].set_xlabel('time interval ');

    ani = animation.FuncAnimation(figPSD, animatePSD, fargs=(ys1, ys2, ys3, ys4, ys5),
                                  interval=1000)
    plt.show()
