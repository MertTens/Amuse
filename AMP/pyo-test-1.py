from pyo import *
import time
s = Server(nchnls=1).boot()
a = Sine(440, 0, 0.1).out()
s.start()
time.sleep(1)
# s.stop()