# Imports
import time
import bitstring
import numpy as np
from bluepy.btle import *

def _unpack_eeg_channel(packet):
    """Decode data packet of one eeg channel.

    Each packet is encoded with a 16bit timestamp followed by 12 time
    samples with a 12 bit resolution.
    """
    aa = bitstring.Bits(bytes=packet)
    pattern = "uint:16,uint:12,uint:12,uint:12,uint:12,uint:12,uint:12, \
               uint:12,uint:12,uint:12,uint:12,uint:12,uint:12"
    res = aa.unpack(pattern)
    packetIndex = res[0]
    data = res[1:]
    # 12 bits on a 2 mVpp range
    data = 0.48828125 * (np.array(data) - 2048)
    return packetIndex, data

# Constants
museAddress = '00:55:da:b5:0d:79'

print('Attempting to connect to Muse at address {}\n'.format(museAddress))

Muse_Peripheral = Peripheral()

Muse_Peripheral.connect(museAddress)

services = Muse_Peripheral.getServices()

# Services apparently come in as type `dict_values` so now I'm turning it into a list
services = list(services)

print('The services provided are as follows: \n{}\n\n'.format(services))



# Now we get the characteristics for each (starting with the 0th service)
chars = []

for num, i in enumerate(services):
	chars.append(i.getCharacteristics())

for num, j in enumerate(chars):
	print('Characteristic #{}: {}\n'.format(num, j))

# At this point chars is an array of arrays, where the sub-sub element is the actual characteristic

for ind, i in enumerate(chars):
	for jind, j in enumerate(i):
		if(j.supportsRead()):
			print('Service #{}, Characteristic #{} Value: {}'.format(ind, jind, j.read()))
		else:
			print('Service #{}, Characteristic #{} is NON-READ'.format(ind, jind))
print('\nNow attempting to read Service 1 Characteristic 2 over time to observe changes:\n')
while True: 
	eeg_datum = chars[1][2].read()	
	packetInd, dat = _unpack_eeg_channel(eeg_datum)
	print(dat)
	time.sleep(0.125)



























'''
print('Supports read: {}'.format(char_0.supportsRead()))

while True:
	time.sleep(1)
	print('The current reading of that characteristic is: {}'.format(char_0.read()))

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        print("  {} = {}".format(desc, value))

'''


