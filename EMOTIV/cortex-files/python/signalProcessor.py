import sys
import os
import numpy as np
import pandas as pd
import serial
import struct
import time
import json



ser = serial.Serial('/dev/cu.usbmodem144401', 9600)

last_time = 0
this_time = time.time()

def process_eeg(eeg_in):
    """Takes in EEG power subscription string, processes it, and sends it to an arduino servo"""

    # Note to self: Ordering of bands is alpha, low beta, high beta, gamma, and theta (5) 

    global last_time
    global this_time
    
    this_time = time.time()

    power = json.loads(eeg_in)
    power = power['pow']
    print(type(power))
    if this_time - last_time > 1:
        avg_value = 0       

        

        ind = 0 
        num_things = 0
        for i in power:
            if ind % 5 == 0:
                avg_value += i
                num_things += 1
            ind+=1

        avg_value /= num_things

        # xs.append(this_time)
        # ys.append(avg_value)

        file1 = open("example.txt","a") 
         

        str1 = str(this_time)+','+str(avg_value)
        str1 += '\n'
        file1.write(str1)
        file1.close()  



        print('\n')
        print(avg_value)
        print('\n')

        send_servo(int(avg_value))
        last_time = time.time()   
    
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


