import time
from matplotlib import pyplot as plt
import numpy as np
import pyaudio
import struct

def live_update_demo():
    CHUNK = 1024*4
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    x = np.linspace(0,CHUNK, CHUNK)
    # X,Y = np.meshgrid(x,x)
    fig = plt.figure()
    # ax1 = fig.add_subplot(1, 1, 1)
    ax = fig.add_subplot(1, 1, 1)

    fig.canvas.draw()   # note that the first draw comes before setting data 

    # h1 = ax1.imshow(X, vmin=-1, vmax=1, interpolation="None", cmap="RdBu")

    h2, = ax.plot(x, lw=3)
    text = ax.text(0.8,1.5, "")
    ax.set_ylim([-1,1])

    t_start = time.time()
    k=0.

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

    # x = np.arange(0, 2*CHUNK, 2)

    data = stream.read(CHUNK, exception_on_overflow = False)
    data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] +127
    for i in np.arange(1000):
        data = stream.read(CHUNK, exception_on_overflow = False)
        data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] +127
        # print(data_int.shape)
        # print(x.shape)
        # h2.set_ydata(np.sin(x/3.+k))
        h2.set_ydata(data_int)
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - t_start)) ) 
        text.set_text(tx)

        k+=0.11

        fig.canvas.draw()
        fig.canvas.flush_events()


        plt.pause(0.000000000001) 
        #plt.pause calls canvas.draw(), as can be read here:
        #http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
        #however with Qt4 (and TkAgg??) this is needed. It seems,using a different backend, 
        #one can avoid plt.pause() and gain even more speed.


live_update_demo() # 28 fps
#live_update_demo(False) # 18 fps

