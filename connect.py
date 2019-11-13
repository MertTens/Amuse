# Imports
import time
import bitstring
import numpy as np
from bluepy.btle import *
import delegate
import threading

'''
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
'''
# Constants
museAddress = '00:55:da:b5:0d:79'

print('Attempting to connect to Muse at address {}\n'.format(museAddress))

Muse_Peripheral = Peripheral()

Muse_Peripheral.connect(museAddress)

services = Muse_Peripheral.getServices()

# Services apparently come in as type `dict_values` so now I'm turning it into a list
services = list(services)

print('The services provided are as follows: \n{}\n\n'.format(services))


chars = []
# Now we get the characteristics for each (starting with the 0th service)
for num, i in enumerate(services):
	chars.append(i.getCharacteristics())

for num, j in enumerate(chars):
	print('Characteristic #{}: {}\n'.format(num, j))

# At this point chars is an array of arrays, where the sub-sub element is the actual characteristic

preset1 = bytearray([0x02, 0x64, 0x0a]) #this preset is for 4 channels and aux
preset2 = bytearray([0x04, 0x70, 0x32, 0x30, 0x0a])

for ind, i in enumerate(chars):
	for jind, j in enumerate(i):	
		if(j.supportsRead()):
			print('Service #{}, Characteristic #{} Value: {}'.format(ind, jind, j.read()))
		else:
			print('Service #{}, Characteristic #{} is NON-READ'.format(ind, jind))
		handle = j.getHandle()
		print('\tHandle: {}, Properties: {}'.format(handle, j.propertiesToString()))
		if handle == 14:
			j.write(preset2)
			j.write(preset1)
			print('\tWROTE PRESET TO GATT 14...')

# Creating delegate - may have to move before the above enumeration/activation.


def eeg(data,trash=True):
	# global callbackTime
	callbackTime=time.time()
	eeg1 = data[0]
	eeg2 = data[1]
	eeg3 = data[2]
	eeg4 = data[3]
	eeg5 = data[4]
	print(data)
	# for i in range(12):
		# print('{0}\n'.format(eeg5[i]))
		# processEEG( eeg1[i], eeg2[i], eeg3[i], eeg4[i], eeg5[i])





peri_delegate = delegate.PeripheralDelegate(eeg)
Muse_Peripheral.withDelegate(peri_delegate)

def runListener():
	while True:
		try:
			print(Muse_Peripheral.waitForNotifications(3.0))
			if Muse_Peripheral.waitForNotifications(3.0):
				print('passed')
				pass
			else:
				print('failed')
		except Exception as e:
			print(e)
			sys.exit(-1);

p1=threading.Thread(target=runListener).start()

'''
while True:
	time.sleep(1)
'''


'''
print('\nNow attempting to read Service 1 Characteristic 2 over time to observe changes:\n')
while True: 
	eeg_datum = chars[1][2].read()	
	print(eeg_datum)
	time.sleep(0.125)
	break

#sample are received in this order : 44, 41, 38, 32, 35 
#we send a byte code 1 to the characteristic ONE AFTER each eeg characteristic to enable notify
eegChannels = [44,41,38,32,35]
for i, channel in enumerate(eegChannels):
	#print("Setup notify on GATT {}".format(channel))
	try:
		Muse_Peripheral.writeCharacteristic(channel+1 , (1).to_bytes(2, byteorder='little'))
		print('Wrote characters to peripheral EEG ')
	except Exception:
		print("---E1---")
	finally:
		pass

print('Attempting to read data from channel again')
while True: 
	eeg_datum = chars[1][2].read()	
	print(eeg_datum)
	time.sleep(0.125)
'''





















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


