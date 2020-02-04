import time
from datetime import datetime
from muse import Muse
from bluepy.btle import Scanner, DefaultDelegate
import sys
import numpy as np

### Serial Connection Functions ###
import serial
import time
import struct

# Define the serial port and baud rate.
# Ensure the 'COM#' corresponds to what was seen in the Windows Device Manager
ser = serial.Serial('/dev/ttyACM1', 115200)

def send_servo(numDegrees):
    if numDegrees <= 0:
        numDegrees = 1
    elif numDegrees >= 170:
        numDegrees = 170

    asBytes = bytearray(str(numDegrees), 'utf-8')

    print('Bytes being written are: {}'.format(asBytes))
    ser.write(asBytes)

### ANALYSIS FUNCTIONS ####

# Fourier Transformation Functions

# Constants:
sample_rate = 256 # Hz

def getLabeledFFT(col):
    len_seconds = len(col)/sample_rate;
    fft = np.fft.fft(col);
    fft = np.abs(fft)**2 # Getting power spectrum of EEG
    fft = fft[:(len(fft)//2)];

    freqs = [];

    for ind in range(0, len(fft)):
        freqs.append(ind*1/len_seconds)

    list_out = [freqs, fft];

    return list_out

def getBands(col, log=False):
    # alpha: 8-13hz
    # beta: 14-30hz
    # theta: 4-7hz
    # delta: 0.5-3hz
    # gamma: 31-50hz
    alpha = 0
    beta = 0
    theta = 0
    delta = 0
    gamma = 0

    num_alpha = 0
    num_beta = 0
    num_theta = 0
    num_delta = 0
    num_gamma = 0

    list_in = getLabeledFFT(col)
    freqs = list_in[0]
    amps = list_in[1]

    for i in range(len(freqs)):
        freq = freqs[i]
        if(freq > 0.5 and freq < 4):
            delta += amps[i]
            num_delta += 1
        elif(freq < 8):
            theta += amps[i]
            num_theta += 1
        elif(freq < 14):
            alpha += amps[i]
            num_alpha += 1
        elif(freq < 31):
            beta += amps[i]
            num_beta += 1
        elif(freq < 51):
            gamma += amps[i]
            num_gamma += 1

    ret_dict = {
        "alpha": (alpha/num_alpha),
        "beta": (beta/num_beta),
        "theta": (theta/num_theta),
        "delta": (delta/num_delta),
        "gamma": (gamma/num_gamma),
        "R": ((alpha/num_alpha)/(beta/num_beta))
    }

    '''
        In addition, according to previous research [23], definite interrelations exist between α and β activities.
        For example, α activity indicates that the brain is in a state of relaxation, whereas β activity is related
        to stimulation. In the study mentioned previously, to observe continuous changes in the mental state of the
        subjects, the ratio of α and β activities was used as the feature for assessing the level of mental
        attentiveness. This study produced the following feature value using the same principle:
    '''

    if(log):
        for key, value in ret_dict.items():
            ret_dict[key] = np.log(value)

    return ret_dict

def aggregate_all_bands(inp):
    dicts = [getBands(inp['eeg1']), getBands(inp['eeg2']), getBands(inp['eeg3']), getBands(inp['eeg4']), getBands(inp['eeg5(aux)'])]
    ret_dict = {"alpha": 0, "beta": 0, "theta": 0, "delta": 0, "gamma": 0, "R": 0}

    for i in dicts:
        ret_dict['alpha'] += (1/5) * i['alpha'];
        ret_dict['beta'] += (1/5) * i['beta'];
        ret_dict['gamma'] += (1/5) * i['gamma'];
        ret_dict['delta'] += (1/5) * i['delta'];
        ret_dict['theta'] += (1/5) * i['theta'];
        ret_dict['R'] += (1/5) * i['R'];

    return ret_dict

### TRANSMISSION AND PROCESSING FUNCTIONS ###


# from datetime import timezone

# myaddress = '00:55:DA:B5:0D:7A' #Tamer's Muse
csv = open("data/muse-recording_{0}.csv".format(datetime.now().strftime('%Y%m%dT%H%M%S')), 'w')
csv.write("timestamp,eeg1,eeg2,eeg3,eeg4,eeg5(aux)\n")

cnt = 0 # variable to keep track of how many samples have passed
        # since the last time we took the FFT (every 256 samples)
transient_matrix = [[], [], [], [], []]
for i in range(len(transient_matrix)):
    for j in range(512):
        transient_matrix[i] += [0]


largest_val = 0
counter =0

def eeg(data, time):

    global counter
    counter+=1
    cnt = 258
    for j in range(12):
        for i in range(len(transient_matrix)):
            transient_matrix[i].pop()

    eeg1 = data[0].tolist()
    eeg2 = data[1].tolist()
    eeg3 = data[2].tolist()
    eeg4 = data[3].tolist()
    eeg5 = data[4].tolist()

    transient_matrix[0] = eeg1 + transient_matrix[0]
    transient_matrix[1] = eeg2 + transient_matrix[1]
    transient_matrix[2] = eeg3 + transient_matrix[2]
    transient_matrix[3] = eeg4 + transient_matrix[3]
    transient_matrix[4] = eeg5 + transient_matrix[4]

    bands_0 = getBands(transient_matrix[0], log=True)
    bands_1 = getBands(transient_matrix[1], log=True)
    bands_2 = getBands(transient_matrix[2], log=True)
    bands_3 = getBands(transient_matrix[3], log=True)
    bands_4 = getBands(transient_matrix[4], log=True)

    # Testing motor control:
    largest_val = 8

    try:
        test_write_val = 1/bands_0['R']
    except:
        test_write_val = 0


    test_write_val /= largest_val

    test_write_val *= 160

    test_write_val = abs(test_write_val)

    print('Value written to servo: {}'.format(test_write_val))

    if counter%10==0:
        send_servo(test_write_val)


    timestamp = time[0]
    for i in range(12):
        csv.write("{0},{1},{2},{3},{4},{5}\n".format(timestamp, eeg1[i], eeg2[i], eeg3[i], eeg4[i], eeg5[i]))


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
muse = Muse(address="00:55:da:b5:0d:79",callback=eeg)
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
