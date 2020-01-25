import serial
import time
import struct

# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
ser = serial.Serial('/dev/ttyACM0', 9600)

def led_on_off(numDegrees):
    if numDegrees <= 0:
        numDegrees = 1
    elif numDegrees >= 170:
        numDegrees = 170

    asBytes = bytearray(str(numDegrees), 'utf-8')

    print('Bytes being written are: {}'.format(asBytes))
    ser.write(asBytes)

# time.sleep(2) # wait for the serial connection to initialize
#
# while True:
#     user_input = int(input("\n Type some number of degrees : "))
#     led_on_off(user_input)
