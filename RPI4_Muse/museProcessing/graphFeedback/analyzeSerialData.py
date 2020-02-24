import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import serial
from matplotlib import style

serialCom = serial.Serial('/dev/cu.usbmodem14201')

style.use('fivethirtyeight')
fig = plt.figure()

ax1 = fig.add_subplot(1, 1, 1)

# xs = list(range(64))
# ys = []
# x = 0
pic = []


def animate(i):
    line = serialCom.readline().decode('utf-8').split(',')
    line.pop()
    row = np.array([float(i) for i in line])
    #    print(row)
    if len(row) == 64:
        row = np.log10(row)
        pic.append(row)
        if len(pic) > 128:
            pic.pop(0)
        ax1.clear()
        ax1.imshow(np.transpose(pic))
        ax1.grid(False)


#        ax1.set_ylim([0.1, 100000])
#        ax1.set_yscale('log')

ani = animation.FuncAnimation(fig, animate, interval=1)
plt.show()
