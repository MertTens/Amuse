import sys
import os
import numpy as np
import pandas as pd
import serial
import struct
import time

ser = serial.Serial('/dev/cu.usbmodem144401', 9600)

def process_eeg(eeg_in):
    """Takes in ___, processes it, and sends it to an arduino servo"""

    print(eeg_in)
    
def send_servo(num_degrees):
    """Takes in an integer between 0 and 180 and sends it to the motor via the arduino."""
    if num_degrees < 0 or num_degrees > 180:
        return False

    asBytes = bytearray(str(num_degrees), 'utf-8')

    ser.write(asBytes)


if __name__ == "__main__":
    while True:
        send_servo(10)
        time.sleep(2)
        send_servo(150)
        time.sleep(2)


