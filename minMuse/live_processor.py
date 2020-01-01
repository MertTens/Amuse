import time
from datetime import datetime
from muse import Muse
from bluepy.btle import Scanner, DefaultDelegate
import sys
import numpy as np

# from datetime import timezone

# myaddress = '00:55:DA:B5:0D:7A' #Tamer's Muse
csv = open("data/muse-recording_{0}.csv".format(datetime.now().strftime('%Y%m%dT%H%M%S')), 'w')
csv.write("timestamp,eeg1,eeg2,eeg3,eeg4,eeg5(aux)\n")

cnt = 0 # variable to keep track of how many samples have passed
        # since the last time we took the FFT (every 256 samples)
transient_matrix = [[], [], [], [], []]
for i in range(len(transient_matrix)):
    for j in range(512):
        transient_matrix[i].push(0)

def eeg(data, time):
    cnt += 1
    for j in range(12):
        for i in range(len(transient_matrix)):
            transient_matrix[i].pop()

    eeg1 = data[0]
    eeg2 = data[1]
    eeg3 = data[2]
    eeg4 = data[3]
    eeg5 = data[4]

    transient_matrix[0] = [eeg1] + transient_matrix[0]
    transient_matrix[1] = [eeg2] + transient_matrix[1]
    transient_matrix[2] = [eeg3] + transient_matrix[2]
    transient_matrix[3] = [eeg4] + transient_matrix[3]
    transient_matrix[4] = [eeg5] + transient_matrix[4]

    if cnt == 256:
        cnt = 0
        print('256 has been reached. Transient matrix is {} long.'.format(len(transient_matrix[0])))

    timestamp = time[0]
    for i in range(12):
        csv.write("{0},{1},{2},{3},{4},{5}\n".format(timestamp, eeg1[i], eeg2[i], eeg3[i], eeg4[i], eeg5[i]))
    # print( "EEG:",data[4])
        #print("Time:",time[0])


# Function to get all acc data
def acc(data):
    pass


# Function to get all gyro data
def gyro(data):
    pass


def findMuse():
        scanner = Scanner()
        devices = scanner.scan(10.0)

        for dev in devices:
            # print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                if ("Muse" in value) or ("muse" in value):
                    return dev.addr  # returns the mac address of the first muse found
                # if no muse found
                print("No Muses found!")

#Iniciamos Clase Muse
muse = Muse(address=findMuse(),eeg=True,callback=eeg,accelero=False,giro=False)
#muse = Muse(address="00:55:DA:B7:0B:E9",eeg=True,callback=eeg,accelero=False,giro=False)
#muse = Muse(address="00:06:66:6C:05:91", eeg=True, callback=eeg, accelero=False, giro=False)


def runListener():
    try:
        print("Connecting to Muse ...")
        muse.connect()
        print("Muse connected")

        muse.start()
        print("Starting streaming")

        while True:
            time.sleep(1)

    except Exception as e:
        print("Killing program")
        print(e)

    finally:
        print("Killing Muse Connection")
        # muse.stop()
        print("Muse stopped")
        # muse.disconnect()
        print("Muse disconnected")


if __name__=="__main__":
    runListener()
# def killListener():
#     print("Disconnecting Muse")
#     #muse.stop()
#     muse.disconnect()
